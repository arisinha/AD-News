"""
YouTube Live Streams Service
Handles communication with YouTube Data API to detect live streams.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional
import httpx
from app.core.config import settings
from app.db.mongodb import get_database

# Simple in-memory cache
_cache: dict = {}
_cache_expiry: dict = {}
CACHE_TTL_SECONDS = 180  # 3 minutes cache


class YouTubeService:
    """Service for interacting with YouTube Data API to detect live streams."""
    
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        
    async def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """Make a request to YouTube Data API."""
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not configured in environment")
        
        params["key"] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    raise ValueError("YouTube API quota exceeded or invalid API key")
                raise
            except httpx.RequestError as e:
                raise ConnectionError(f"Failed to connect to YouTube API: {str(e)}")
    
    async def search_live_streams(self, channel_id: str) -> Optional[dict]:
        """
        Search for active live streams on a specific channel.
        Returns the first live stream found or None.
        """
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "type": "video",
            "eventType": "live",
            "maxResults": 1
        }
        
        try:
            data = await self._make_request("search", params)
            if data and data.get("items"):
                return data["items"][0]
            return None
        except Exception:
            return None
    
    async def get_video_details(self, video_id: str) -> Optional[dict]:
        """Get detailed information about a video."""
        params = {
            "part": "snippet,liveStreamingDetails",
            "id": video_id
        }
        
        try:
            data = await self._make_request("videos", params)
            if data and data.get("items"):
                return data["items"][0]
            return None
        except Exception:
            return None
    
    async def check_channel_live_status(self, channel_name: str, channel_id: str) -> dict:
        """
        Check if a channel is currently live streaming.
        Returns a structured response with live stream info.
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
        
        try:
            # Search for live streams
            live_stream = await self.search_live_streams(channel_id)
            
            if live_stream:
                video_id = live_stream["id"]["videoId"]
                snippet = live_stream["snippet"]
                
                # Get high quality thumbnail
                thumbnails = snippet.get("thumbnails", {})
                thumbnail = (
                    thumbnails.get("high", {}).get("url") or
                    thumbnails.get("medium", {}).get("url") or
                    thumbnails.get("default", {}).get("url")
                )
                
                result.update({
                    "live": True,
                    "videoId": video_id,
                    "title": snippet.get("title"),
                    "thumbnail": thumbnail
                })
        except Exception as e:
            # Log error but don't fail - just return not live
            print(f"Error checking live status for {channel_name}: {str(e)}")
        
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
                channel.get("channelId")
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
