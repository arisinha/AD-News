"""
YouTube Live Streams API Router
Provides endpoints to get live stream statuses from news channels.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.services.youtube_service import youtube_service

router = APIRouter()


class LiveStreamResponse(BaseModel):
    """Response model for a single channel's live status."""
    name: str
    channelId: str
    live: bool
    videoId: Optional[str] = None
    title: Optional[str] = None
    thumbnail: Optional[str] = None
    updatedAt: str


class LiveStreamsListResponse(BaseModel):
    """Response model for the list of all channels' live statuses."""
    channels: list[LiveStreamResponse]
    total: int
    liveCount: int
    timestamp: str


@router.get("/lives", response_model=LiveStreamsListResponse)
async def get_youtube_lives(force_refresh: bool = False):
    """
    Get live stream status for all configured news channels.
    
    Returns a list of channels with their current live streaming status.
    Live channels are sorted first, followed by offline channels.
    
    Args:
        force_refresh: If true, bypasses cache and fetches fresh data from YouTube API.
    
    Responses are cached for 1 minute to respect YouTube API quotas.
    """
    try:
        # Clear cache if force_refresh is requested
        if force_refresh:
            from app.services.youtube_service import _cache, _cache_expiry
            _cache.clear()
            _cache_expiry.clear()
        
        live_statuses = await youtube_service.get_all_live_channels()
        
        live_count = sum(1 for channel in live_statuses if channel.get("live", False))
        
        return LiveStreamsListResponse(
            channels=[LiveStreamResponse(**status) for status in live_statuses],
            total=len(live_statuses),
            liveCount=live_count,
            timestamp=datetime.utcnow().isoformat()
        )
    except ValueError as e:
        # Configuration or API key errors
        raise HTTPException(status_code=503, detail=str(e))
    except ConnectionError as e:
        # Network errors
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(status_code=500, detail=f"Failed to fetch live streams: {str(e)}")


@router.get("/lives/{channel_id}", response_model=LiveStreamResponse)
async def get_channel_live_status(channel_id: str):
    """
    Get live stream status for a specific channel by its YouTube channel ID.
    
    Args:
        channel_id: The YouTube channel ID (e.g., UCupvZG-5ko_eiXAupbDfxWw)
    
    Returns:
        The channel's current live streaming status.
    """
    try:
        # Get channel name from database or use "Unknown"
        from app.db.mongodb import get_database
        db = await get_database()
        channel = await db.channels.find_one({"channelId": channel_id})
        
        channel_name = channel.get("name", "Unknown") if channel else "Unknown"
        
        status = await youtube_service.check_channel_live_status(channel_name, channel_id)
        return LiveStreamResponse(**status)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch live status: {str(e)}")
