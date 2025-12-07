from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.crud.article import article as article_crud
from app.schemas.article import ArticleCreate
from app.db.mongodb import get_database
from datetime import datetime, timedelta
from bson import ObjectId

router = APIRouter()

@router.post("/articles")
async def seed_articles(
    db=Depends(get_database),
) -> Any:
    """Seed the database with sample articles"""
    
    sample_articles = [
        ArticleCreate(
            title="Avances en Inteligencia Artificial transforman la industria tecnológica",
            description="Las nuevas tecnologías de IA están revolucionando diversos sectores",
            content="La inteligencia artificial continúa avanzando a pasos agigantados, transformando industrias completas...",
            author="María González",
            url="https://example.com/article1",
            image_url="https://picsum.photos/800/600?random=1",
            source_name="Tech News MX",
            published_at=(datetime.utcnow() - timedelta(hours=2)).isoformat(),
            category="technology",
            region="mx",
        ),
        ArticleCreate(
            title="Nuevo descubrimiento científico podría cambiar la medicina moderna",
            description="Investigadores encuentran una nueva forma de tratar enfermedades crónicas",
            content="Un equipo de científicos ha descubierto un método revolucionario que podría transformar el tratamiento...",
            author="Dr. Carlos Ramírez",
            url="https://example.com/article2",
            image_url="https://picsum.photos/800/600?random=2",
            source_name="Ciencia Hoy",
            published_at=(datetime.utcnow() - timedelta(hours=5)).isoformat(),
            category="science",
            region="mx",
        ),
        ArticleCreate(
            title="Economía mexicana muestra signos de recuperación",
            description="Los indicadores económicos muestran tendencias positivas",
            content="Los últimos datos económicos revelan una recuperación gradual en diversos sectores...",
            author="Ana Martínez",
            url="https://example.com/article3",
            image_url="https://picsum.photos/800/600?random=3",
            source_name="Economía al Día",
            published_at=(datetime.utcnow() - timedelta(hours=8)).isoformat(),
            category="business",
            region="mx",
        ),
        ArticleCreate(
            title="Deportes: México clasifica a la final del torneo internacional",
            description="La selección nacional logra una victoria histórica",
            content="En un partido emocionante, la selección mexicana logró clasificar a la final...",
            author="Roberto Sánchez",
            url="https://example.com/article4",
            image_url="https://picsum.photos/800/600?random=4",
            source_name="Deportes MX",
            published_at=(datetime.utcnow() - timedelta(hours=12)).isoformat(),
            category="sports",
            region="mx",
        ),
        ArticleCreate(
            title="Cambio climático: Nuevas políticas ambientales entran en vigor",
            description="Gobierno implementa medidas para combatir el cambio climático",
            content="Las nuevas regulaciones ambientales buscan reducir las emisiones de carbono...",
            author="Laura Fernández",
            url="https://example.com/article5",
            image_url="https://picsum.photos/800/600?random=5",
            source_name="Medio Ambiente Hoy",
            published_at=(datetime.utcnow() - timedelta(days=1)).isoformat(),
            category="environment",
            region="mx",
        ),
        ArticleCreate(
            title="Innovación en energías renovables alcanza récord histórico",
            description="La producción de energía solar y eólica supera expectativas",
            content="Las inversiones en energías limpias están dando resultados extraordinarios...",
            author="Pedro Jiménez",
            url="https://example.com/article6",
            image_url="https://picsum.photos/800/600?random=6",
            source_name="Energía Verde",
            published_at=(datetime.utcnow() - timedelta(days=1, hours=6)).isoformat(),
            category="technology",
            region="mx",
        ),
        ArticleCreate(
            title="Educación digital: Nuevas plataformas transforman el aprendizaje",
            description="La tecnología educativa mejora el acceso a la educación",
            content="Las plataformas de aprendizaje en línea están democratizando la educación...",
            author="Sofia Torres",
            url="https://example.com/article7",
            image_url="https://picsum.photos/800/600?random=7",
            source_name="Educación MX",
            published_at=(datetime.utcnow() - timedelta(days=2)).isoformat(),
            category="education",
            region="mx",
        ),
        ArticleCreate(
            title="Salud pública: Campaña de vacunación alcanza el 80% de cobertura",
            description="Autoridades celebran el éxito de la campaña nacional",
            content="La campaña de vacunación ha superado las metas establecidas...",
            author="Dr. Miguel Ángel López",
            url="https://example.com/article8",
            image_url="https://picsum.photos/800/600?random=8",
            source_name="Salud al Día",
            published_at=(datetime.utcnow() - timedelta(days=2, hours=12)).isoformat(),
            category="health",
            region="mx",
        ),
        ArticleCreate(
            title="Cultura: Festival internacional de cine abre sus puertas",
            description="Cineastas de todo el mundo se reúnen en México",
            content="El festival de cine más importante de Latinoamérica da inicio con grandes expectativas...",
            author="Carmen Ruiz",
            url="https://example.com/article9",
            image_url="https://picsum.photos/800/600?random=9",
            source_name="Cultura y Arte",
            published_at=(datetime.utcnow() - timedelta(days=3)).isoformat(),
            category="entertainment",
            region="mx",
        ),
        ArticleCreate(
            title="Tecnología blockchain revoluciona el sector financiero",
            description="Bancos adoptan nuevas tecnologías para mejorar servicios",
            content="La tecnología blockchain está transformando la forma en que operan las instituciones financieras...",
            author="Jorge Mendoza",
            url="https://example.com/article10",
            image_url="https://picsum.photos/800/600?random=10",
            source_name="Finanzas Tech",
            published_at=(datetime.utcnow() - timedelta(days=3, hours=8)).isoformat(),
            category="business",
            region="mx",
        ),
    ]
    
    created_articles = []
    for article_data in sample_articles:
        article = await article_crud.create(db, obj_in=article_data)
        created_articles.append(article)
    
    return {
        "message": f"Successfully seeded {len(created_articles)} articles",
        "count": len(created_articles)
    }


@router.post("/channels")
async def seed_channels(
    db=Depends(get_database),
) -> Any:
    """Seed the database with YouTube news channels for live stream detection"""
    
    from data.seed_channels import seed_channels as run_seed
    
    result = await run_seed()
    
    return {
        "message": f"Successfully seeded channels: {result['inserted']} inserted, {result['updated']} updated, {result.get('deleted', 0)} deleted",
        "inserted": result["inserted"],
        "updated": result["updated"],
        "deleted": result.get("deleted", 0),
        "total": result["total"]
    }


@router.post("/newsapi")
async def seed_from_newsapi(
    country: str = "mx",
    category: str = None,
    all_categories: bool = False,
    page_size: int = 20,
    db=Depends(get_database),
) -> Any:
    """
    Fetch real news from NewsAPI and store in database.
    
    Args:
        country: 2-letter country code (default: 'mx' for Mexico)
        category: Optional category filter (business, entertainment, general, health, science, sports, technology)
        all_categories: If True, fetch from all categories (overrides category param)
        page_size: Number of articles per request (max 100)
    
    Returns:
        Summary of inserted and skipped articles
    """
    from app.services.news_aggregation import news_service
    
    try:
        # Fetch articles from NewsAPI
        if all_categories:
            articles = await news_service.fetch_all_categories(
                country=country,
                articles_per_category=page_size
            )
        else:
            articles = await news_service.fetch_top_headlines(
                country=country,
                category=category,
                page_size=page_size
            )
        
        if not articles:
            return {
                "message": "No articles fetched from NewsAPI",
                "inserted": 0,
                "skipped": 0,
                "total_fetched": 0
            }
        
        # Get existing URLs to avoid duplicates
        existing_urls = set()
        cursor = db["articles"].find({}, {"url": 1})
        async for doc in cursor:
            existing_urls.add(doc.get("url"))
        
        # Insert new articles
        inserted_count = 0
        skipped_count = 0
        
        for article_data in articles:
            if article_data.url in existing_urls:
                skipped_count += 1
                continue
            
            # Create article in database
            article = await article_crud.create(db, obj_in=article_data)
            inserted_count += 1
            existing_urls.add(article_data.url)  # Add to set to prevent duplicates within same batch
        
        return {
            "message": f"Successfully fetched news from NewsAPI",
            "inserted": inserted_count,
            "skipped": skipped_count,
            "total_fetched": len(articles)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


@router.delete("/articles")
async def clear_articles(
    db=Depends(get_database),
) -> Any:
    """Clear all articles from the database"""
    result = await db["articles"].delete_many({})
    return {
        "message": f"Deleted {result.deleted_count} articles",
        "deleted_count": result.deleted_count
    }


@router.post("/spanish")
async def seed_spanish_news(
    articles_per_category: int = 15,
    enrich: bool = True,
    db=Depends(get_database),
) -> Any:
    """
    Fetch Spanish language news for Mexican market and optionally enrich with AI summaries.
    
    Args:
        articles_per_category: Number of articles per category (default: 15)
        enrich: If True, generate AI summaries for new articles (default: True)
    
    Returns:
        Summary of inserted, skipped, and enriched articles
    """
    from app.services.news_aggregation import news_service
    from app.services.summary_service import summary_service
    
    try:
        # Fetch Spanish language articles
        articles = await news_service.fetch_spanish_news(
            articles_per_category=articles_per_category,
            region="mx"
        )
        
        if not articles:
            return {
                "message": "No Spanish articles fetched from NewsAPI",
                "inserted": 0,
                "skipped": 0,
                "enriched": 0,
                "total_fetched": 0
            }
        
        # Get existing URLs to avoid duplicates
        existing_urls = set()
        cursor = db["articles"].find({}, {"url": 1})
        async for doc in cursor:
            existing_urls.add(doc.get("url"))
        
        # Insert new articles
        inserted_count = 0
        skipped_count = 0
        enriched_count = 0
        inserted_ids = []
        
        for article_data in articles:
            if article_data.url in existing_urls:
                skipped_count += 1
                continue
            
            # Create article in database
            article = await article_crud.create(db, obj_in=article_data)
            inserted_count += 1
            inserted_ids.append(article.id)
            existing_urls.add(article_data.url)
        
        # Enrich new articles with AI summaries
        if enrich and inserted_ids:
            collection = db["articles"]
            for article_id in inserted_ids:
                try:
                    # Get the article
                    article = await article_crud.get(db, id=str(article_id))
                    if not article:
                        continue
                    
                    # Generate enrichment data
                    text = f"{article.title}. {article.description or ''}. {article.content or ''}"
                    enrichment = await summary_service.enrich_article(text)
                    
                    # Update the article (convert string ID to ObjectId)
                    await collection.update_one(
                        {"_id": ObjectId(article_id)},
                        {"$set": {
                            "ai_summary": enrichment["summary"],
                            "key_points": enrichment["key_points"],
                            "sentiment_score": enrichment["sentiment_score"],
                            "sentiment_label": enrichment["sentiment_label"]
                        }}
                    )
                    enriched_count += 1
                except Exception as e:
                    print(f"Error enriching article {article_id}: {e}")
                    continue
        
        return {
            "message": f"Successfully fetched Spanish news for Mexican market",
            "inserted": inserted_count,
            "skipped": skipped_count,
            "enriched": enriched_count,
            "total_fetched": len(articles)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch Spanish news: {str(e)}")
