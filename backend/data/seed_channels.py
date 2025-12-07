"""
Seed script for YouTube channels collection.
Contains Spanish-language news channels, primarily from Mexico.
"""

# Spanish-language news channels with their YouTube channel IDs
NEWS_CHANNELS = [
    # Mexican News Channels
    {
        "name": "Milenio",
        "channelId": "UCFxH2jxHQPz2OaA-gvSRIzg",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "Imagen Noticias",
        "channelId": "UCq7xKqfSPBTe8rFcEITfS0w",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "Televisa Noticias",
        "channelId": "UCHq9DoL9ONG4LCAmXMR1bTg",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "N+ Noticias",
        "channelId": "UC8yvDroqvTz0qnKlKPUEXog",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "Foro TV",
        "channelId": "UCnPLGBjP90UYV4c10xnA_TQ",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "ADN 40",
        "channelId": "UCbFiNkmAkh9VWqBjvZ-K2PQ",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "Excélsior TV",
        "channelId": "UClqo4ZAAZ01HQdCTlovwY6g",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "El Universal",
        "channelId": "UCHhGLdVcVJHMN34vKBa7dNA",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "TV Azteca Noticias",
        "channelId": "UCxFLeXd7-OrcPD2s00xxRjQ",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    {
        "name": "Once Noticias",
        "channelId": "UChG6tArNrVTMPwfvKIBvlXA",
        "category": "news",
        "language": "es",
        "region": "MX"
    },
    # Latin American/International Spanish Channels
    {
        "name": "CNN en Español",
        "channelId": "UCK3PcpioUREFnBYLDuh2DxQ",
        "category": "news",
        "language": "es",
        "region": "US"
    },
    {
        "name": "Telemundo",
        "channelId": "UCRwA1NTjGOP1RkYoP4wRCmw",
        "category": "news",
        "language": "es",
        "region": "US"
    },
    {
        "name": "NTN24",
        "channelId": "UCBhlvKZfJPexg7BuR5d0tRA",
        "category": "news",
        "language": "es",
        "region": "CO"
    },
    {
        "name": "DW Español",
        "channelId": "UCT2VMLy-rU1bgkB1FXkMV5g",
        "category": "news",
        "language": "es",
        "region": "DE"
    },
    {
        "name": "FRANCE 24 Español",
        "channelId": "UCUdOoVWuWmgo1wByzcsyKDQ",
        "category": "news",
        "language": "es",
        "region": "FR"
    },
]


async def seed_channels():
    """
    Seed the channels collection with news channels.
    Deletes channels not in the current list and upserts the rest.
    """
    from app.db.mongodb import get_database
    from datetime import datetime
    
    db = await get_database()
    channels_collection = db.channels
    
    # Create index on channelId for fast lookups
    await channels_collection.create_index("channelId", unique=True)
    
    # Get list of channel IDs we want to keep
    valid_channel_ids = [ch["channelId"] for ch in NEWS_CHANNELS]
    
    # Delete channels not in the current list
    delete_result = await channels_collection.delete_many({
        "channelId": {"$nin": valid_channel_ids}
    })
    deleted = delete_result.deleted_count
    
    inserted = 0
    updated = 0
    
    for channel in NEWS_CHANNELS:
        channel_data = {
            **channel,
            "updatedAt": datetime.utcnow()
        }
        
        result = await channels_collection.update_one(
            {"channelId": channel["channelId"]},
            {
                "$set": channel_data,
                "$setOnInsert": {"createdAt": datetime.utcnow()}
            },
            upsert=True
        )
        
        if result.upserted_id:
            inserted += 1
        elif result.modified_count > 0:
            updated += 1
    
    return {
        "inserted": inserted,
        "updated": updated,
        "deleted": deleted,
        "total": len(NEWS_CHANNELS)
    }
