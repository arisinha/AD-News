import aiohttp
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.core.config import settings
from app.schemas.article import ArticleCreate


class NewsAggregationService:
    """Service to fetch real news from NewsAPI.org"""
    
    # Map NewsAPI categories to internal categories
    CATEGORY_MAP = {
        "business": "business",
        "entertainment": "entertainment",
        "general": "general",
        "health": "health",
        "science": "science",
        "sports": "sports",
        "technology": "technology",
    }
    
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"

    async def fetch_top_headlines(
        self, 
        country: str = "mx", 
        category: Optional[str] = None,
        page_size: int = 20
    ) -> List[ArticleCreate]:
        """
        Fetch top headlines from NewsAPI.
        
        Args:
            country: 2-letter ISO 3166-1 country code (e.g., 'mx', 'us')
            category: Category filter (business, entertainment, general, health, science, sports, technology)
            page_size: Number of articles to fetch (max 100 for free tier)
        
        Returns:
            List of ArticleCreate objects ready to be stored in database
        """
        if not self.api_key:
            raise ValueError("NEWS_API_KEY is not configured in environment variables")
        
        params = {
            "country": country,
            "apiKey": self.api_key,
            "pageSize": min(page_size, 100),  # NewsAPI max is 100
        }
        
        if category and category in self.CATEGORY_MAP:
            params["category"] = category
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/top-headlines", params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"NewsAPI error ({response.status}): {error_text}")
                
                data = await response.json()
                
                if data.get("status") != "ok":
                    raise Exception(f"NewsAPI returned error: {data.get('message', 'Unknown error')}")
                
                articles = data.get("articles", [])
                return self._parse_articles(articles, category or "general", country)

    async def fetch_everything(
        self,
        query: str,
        language: str = "es",
        sort_by: str = "publishedAt",
        page_size: int = 20
    ) -> List[ArticleCreate]:
        """
        Search all articles matching a query.
        
        Args:
            query: Keywords or phrases to search for
            language: Language code (e.g., 'es', 'en')
            sort_by: Sort order (relevancy, popularity, publishedAt)
            page_size: Number of articles to fetch
        
        Returns:
            List of ArticleCreate objects
        """
        if not self.api_key:
            raise ValueError("NEWS_API_KEY is not configured in environment variables")
        
        params = {
            "q": query,
            "language": language,
            "sortBy": sort_by,
            "apiKey": self.api_key,
            "pageSize": min(page_size, 100),
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/everything", params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"NewsAPI error ({response.status}): {error_text}")
                
                data = await response.json()
                
                if data.get("status") != "ok":
                    raise Exception(f"NewsAPI returned error: {data.get('message', 'Unknown error')}")
                
                articles = data.get("articles", [])
                return self._parse_articles(articles, "general", None)

    async def fetch_all_categories(
        self,
        country: str = "mx",
        articles_per_category: int = 10
    ) -> List[ArticleCreate]:
        """
        Fetch articles from all available categories.
        
        Args:
            country: 2-letter ISO 3166-1 country code
            articles_per_category: Number of articles to fetch per category
        
        Returns:
            Combined list of articles from all categories
        """
        all_articles = []
        
        for category in self.CATEGORY_MAP.keys():
            try:
                articles = await self.fetch_top_headlines(
                    country=country,
                    category=category,
                    page_size=articles_per_category
                )
                all_articles.extend(articles)
            except Exception as e:
                print(f"Error fetching {category} news: {e}")
                continue
        
        return all_articles

    async def fetch_spanish_news(
        self,
        articles_per_category: int = 15,
        region: str = "mx"
    ) -> List[ArticleCreate]:
        """
        Fetch Spanish language news using category-based keyword searches.
        This uses the /everything endpoint with Spanish language filter.
        
        Args:
            articles_per_category: Number of articles to fetch per category
            region: Region code to assign to articles
        
        Returns:
            List of Spanish language articles across all categories
        """
        if not self.api_key:
            raise ValueError("NEWS_API_KEY is not configured in environment variables")
        
        # Spanish keywords for each category
        category_queries = {
            "business": "negocios OR economía OR finanzas OR empresas OR bolsa",
            "entertainment": "entretenimiento OR celebridades OR cine OR música OR televisión",
            "general": "noticias OR México OR Latinoamérica OR actualidad",
            "health": "salud OR medicina OR bienestar OR hospital OR enfermedad",
            "science": "ciencia OR investigación OR descubrimiento OR tecnología científica",
            "sports": "deportes OR fútbol OR béisbol OR atletas OR Liga MX",
            "technology": "tecnología OR innovación OR inteligencia artificial OR apps OR startups",
        }
        
        all_articles = []
        
        async with aiohttp.ClientSession() as session:
            for category, query in category_queries.items():
                try:
                    params = {
                        "q": query,
                        "language": "es",
                        "sortBy": "publishedAt",
                        "apiKey": self.api_key,
                        "pageSize": min(articles_per_category, 100),
                    }
                    
                    async with session.get(f"{self.base_url}/everything", params=params) as response:
                        if response.status != 200:
                            print(f"Error fetching {category}: {response.status}")
                            continue
                        
                        data = await response.json()
                        
                        if data.get("status") != "ok":
                            print(f"API error for {category}: {data.get('message')}")
                            continue
                        
                        articles = data.get("articles", [])
                        parsed = self._parse_articles(articles, category, region)
                        all_articles.extend(parsed)
                        
                except Exception as e:
                    print(f"Error fetching {category} Spanish news: {e}")
                    continue
        
        return all_articles

    def _parse_articles(
        self, 
        raw_articles: List[Dict[str, Any]], 
        default_category: str,
        region: Optional[str]
    ) -> List[ArticleCreate]:
        """
        Parse NewsAPI articles into ArticleCreate objects.
        
        Args:
            raw_articles: List of article dicts from NewsAPI response
            default_category: Category to assign to articles
            region: Region/country code
        
        Returns:
            List of ArticleCreate objects
        """
        articles = []
        
        for raw in raw_articles:
            # Skip articles with missing essential data
            if not raw.get("title") or not raw.get("url"):
                continue
            
            # Skip "[Removed]" placeholder articles
            if raw.get("title") == "[Removed]" or raw.get("content") == "[Removed]":
                continue
            
            # Parse published date
            published_at = raw.get("publishedAt", datetime.utcnow().isoformat())
            
            # Get source name
            source = raw.get("source", {})
            source_name = source.get("name", "Unknown Source") if isinstance(source, dict) else str(source)
            
            # Get image URL - use the urlToImage from NewsAPI
            image_url = raw.get("urlToImage")
            
            # Create article
            article = ArticleCreate(
                title=raw.get("title", "").strip(),
                description=raw.get("description", "").strip() if raw.get("description") else None,
                content=raw.get("content", "").strip() if raw.get("content") else None,
                author=raw.get("author", "").strip() if raw.get("author") else None,
                url=raw.get("url"),
                image_url=image_url,
                source_name=source_name,
                published_at=published_at,
                category=default_category,
                region=region,
            )
            
            articles.append(article)
        
        return articles


news_service = NewsAggregationService()
