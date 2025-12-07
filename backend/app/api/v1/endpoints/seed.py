from typing import Any
from fastapi import APIRouter, Depends
from app.crud.article import article as article_crud
from app.schemas.article import ArticleCreate
from app.db.mongodb import get_database
from datetime import datetime, timedelta

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

