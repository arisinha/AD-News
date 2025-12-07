"""
YouTube Live Streams Service
Handles detection of YouTube live streams using web scraping (no quota limits)
with fallback to YouTube Data API when available.
"""

import asyncio
import re
from datetime import datetime, timedelta
from typing import Optional
import httpx
from app.core.config import settings
from app.db.mongodb import get_database

# Simple in-memory cache
_cache: dict = {}
_cache_expiry: dict = {}
CACHE_TTL_SECONDS = 120  # 2 minutes cache


class YouTubeService:
    """Service for detecting YouTube live streams."""
    
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
    
    async def _check_video_is_live(self, client: httpx.AsyncClient, video_id: str) -> bool:
        """Check if a specific video ID is currently live."""
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            response = await client.get(video_url, headers=self.headers)
            content = response.text
            return (
                '"isLive":true' in content or 
                '"isLiveNow":true' in content or
                '"isLiveContent":true' in content
            )
        except Exception:
            return False
    
    async def _scrape_live_by_handle(self, handle: str) -> Optional[dict]:
        """
        Check if a channel is live using its @handle.
        This works better than channel ID for live detection.
        """
        if not handle:
            return None
            
        live_url = f"https://www.youtube.com/{handle}/live"
        
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            try:
                response = await client.get(live_url, headers=self.headers)
                final_url = str(response.url)
                content = response.text
                
                # Method 1: Check if redirected to a video (direct live)
                if "/watch?v=" in final_url:
                    video_id_match = re.search(r'watch\?v=([a-zA-Z0-9_-]+)', final_url)
                    if video_id_match:
                        video_id = video_id_match.group(1)
                        is_live = await self._check_video_is_live(client, video_id)
                        
                        if is_live:
                            return await self._extract_video_info(content, video_id)
                
                # Method 2: Check videos on the live page for any with live badge
                video_ids = list(set(re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', content)))
                
                for video_id in video_ids[:5]:  # Check first 5 videos
                    is_live = await self._check_video_is_live(client, video_id)
                    if is_live:
                        # Fetch video page for details
                        video_response = await client.get(
                            f"https://www.youtube.com/watch?v={video_id}", 
                            headers=self.headers
                        )
                        return await self._extract_video_info(video_response.text, video_id)
                
                return None
                
            except Exception as e:
                print(f"Scrape error for handle {handle}: {str(e)}")
                return None
    
    async def _scrape_live_by_channel_id(self, channel_id: str) -> Optional[dict]:
        """
        Scrape YouTube channel's /live page using channel ID.
        """
        live_url = f"https://www.youtube.com/channel/{channel_id}/live"
        
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            try:
                response = await client.get(live_url, headers=self.headers)
                final_url = str(response.url)
                content = response.text
                
                if "/watch?v=" in final_url:
                    video_id_match = re.search(r'watch\?v=([a-zA-Z0-9_-]+)', final_url)
                    if video_id_match:
                        video_id = video_id_match.group(1)
                        is_live = await self._check_video_is_live(client, video_id)
                        
                        if is_live:
                            return await self._extract_video_info(content, video_id)
                
                return None
                
            except Exception as e:
                print(f"Scrape error for channel {channel_id}: {str(e)}")
                return None
    
    async def _extract_video_info(self, content: str, video_id: str) -> dict:
        """Extract title and thumbnail from video page content."""
        # Extract title
        title = None
        title_patterns = [
            r'"title":\{"runs":\[\{"text":"([^"]+)"',
            r'"title":"([^"]+)"',
            r'<title>([^<]+)</title>'
        ]
        for pattern in title_patterns:
            match = re.search(pattern, content)
            if match:
                title = match.group(1)
                if " - YouTube" in title:
                    title = title.replace(" - YouTube", "")
                break
        
        # Extract thumbnail
        thumbnail = None
        thumb_patterns = [
            r'"thumbnail":\{"thumbnails":\[.*?"url":"(https://i\.ytimg\.com/[^"]+)"',
            r'"thumbnails":\[\{"url":"(https://[^"]+)"'
        ]
        for pattern in thumb_patterns:
            match = re.search(pattern, content)
            if match:
                thumbnail = match.group(1)
                break
        
        # Fallback thumbnail
        if not thumbnail and video_id:
            thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        
        return {
            "live": True,
            "videoId": video_id,
            "title": title,
            "thumbnail": thumbnail
        }
    
    async def _api_search_live(self, channel_id: str) -> Optional[dict]:
        """
        Search for live streams using YouTube Data API.
        This method consumes API quota.
        """
        if not self.api_key:
            return None
        
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "type": "video",
            "eventType": "live",
            "maxResults": 1,
            "key": self.api_key
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                url = f"{self.BASE_URL}/search"
                response = await client.get(url, params=params)
                
                if response.status_code == 403:
                    # Quota exceeded - don't use API
                    return None
                
                response.raise_for_status()
                data = response.json()
                
                if data and data.get("items"):
                    item = data["items"][0]
                    snippet = item.get("snippet", {})
                    thumbnails = snippet.get("thumbnails", {})
                    
                    return {
                        "live": True,
                        "videoId": item["id"]["videoId"],
                        "title": snippet.get("title"),
                        "thumbnail": (
                            thumbnails.get("high", {}).get("url") or
                            thumbnails.get("medium", {}).get("url") or
                            thumbnails.get("default", {}).get("url")
                        )
                    }
                return None
                
            except Exception as e:
                print(f"API search error for channel {channel_id}: {str(e)}")
                return None
    
    async def check_channel_live_status(
        self, 
        channel_name: str, 
        channel_id: str, 
        handle: str = None
    ) -> dict:
        """
        Check if a channel is currently live streaming.
        Uses web scraping first (no quota), falls back to API if needed.
        """
        # Check cache first
        cache_key = f"live_{channel_id}"
        now = datetime.utcnow()
        
        if cache_key in _cache and cache_key in _cache_expiry:
            if _cache_expiry[cache_key] > now:
                return _cache[cache_key]
        
        result = {
            "name": channel_name,
            "channelId": channel_id,
            "live": False,
            "videoId": None,
            "title": None,
            "thumbnail": None,
            "updatedAt": now.isoformat()
        }
        
        # Method 1: Try scraping with @handle (most reliable)
        if handle:
            scrape_result = await self._scrape_live_by_handle(handle)
            if scrape_result and scrape_result.get("live"):
                result.update(scrape_result)
                _cache[cache_key] = result
                _cache_expiry[cache_key] = now + timedelta(seconds=CACHE_TTL_SECONDS)
                return result
        
        # Method 2: Try scraping with channel ID
        scrape_result = await self._scrape_live_by_channel_id(channel_id)
        if scrape_result and scrape_result.get("live"):
            result.update(scrape_result)
            _cache[cache_key] = result
            _cache_expiry[cache_key] = now + timedelta(seconds=CACHE_TTL_SECONDS)
            return result
        
        # Method 3: Fallback to API (if quota available)
        api_result = await self._api_search_live(channel_id)
        if api_result and api_result.get("live"):
            result.update(api_result)
        
        # Cache the result
        _cache[cache_key] = result
        _cache_expiry[cache_key] = now + timedelta(seconds=CACHE_TTL_SECONDS)
        
        return result
    
    async def get_all_live_channels(self) -> list[dict]:
        """
        Get live status for all channels in the database.
        Returns a list of channel live statuses.
        """
        db = await get_database()
        channels_collection = db.channels
        
        # Get all channels from database
        channels = await channels_collection.find({}).to_list(length=100)
        
        if not channels:
            return []
        
        # Check live status for all channels concurrently
        tasks = [
            self.check_channel_live_status(
                channel.get("name", "Unknown"),
                channel.get("channelId"),
                channel.get("handle")  # Pass the handle if available
            )
            for channel in channels
            if channel.get("channelId")
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        live_statuses = []
        for result in results:
            if isinstance(result, dict):
                live_statuses.append(result)
        
        # Sort: live channels first, then by name
        live_statuses.sort(key=lambda x: (not x["live"], x["name"].lower()))
        
        return live_statuses


# Singleton instance
youtube_service = YouTubeService()
