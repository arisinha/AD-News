from openai import AsyncOpenAI
from app.core.config import settings
from typing import List, Dict
import json

class SummaryService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    async def generate_summary(self, text: str) -> str:
        if not self.client:
            return "AI Summary not available (API Key missing)"
            
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful news assistant. Summarize the following article in Spanish, concise and neutral."},
                    {"role": "user", "content": text}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Error generating summary"

    async def extract_key_points(self, text: str) -> List[str]:
        """Extract 3-5 key points from the article"""
        if not self.client:
            return []
            
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful news assistant. Extract 3-5 key points from the following article in Spanish. Return ONLY a JSON array of strings, nothing else."},
                    {"role": "user", "content": text}
                ],
                max_tokens=200
            )
            content = response.choices[0].message.content.strip()
            # Try to parse as JSON
            try:
                key_points = json.loads(content)
                if isinstance(key_points, list):
                    return key_points[:5]  # Limit to 5 points
            except json.JSONDecodeError:
                # If not valid JSON, split by newlines and clean up
                points = [line.strip().lstrip('-•*').strip() for line in content.split('\n') if line.strip()]
                return points[:5]
            return []
        except Exception as e:
            print(f"Error extracting key points: {e}")
            return []

    async def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """Analyze sentiment of the article and return score and label"""
        if not self.client:
            return {"score": 0.0, "label": "neutral"}
            
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis assistant. Analyze the sentiment of the following article and respond with ONLY a JSON object with 'score' (float from -1.0 to 1.0) and 'label' (positive/negative/neutral). Example: {\"score\": 0.5, \"label\": \"positive\"}"},
                    {"role": "user", "content": text}
                ],
                max_tokens=50
            )
            content = response.choices[0].message.content.strip()
            try:
                sentiment = json.loads(content)
                return {
                    "score": float(sentiment.get("score", 0.0)),
                    "label": sentiment.get("label", "neutral")
                }
            except (json.JSONDecodeError, ValueError):
                return {"score": 0.0, "label": "neutral"}
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {"score": 0.0, "label": "neutral"}

    async def enrich_article(self, text: str) -> Dict[str, any]:
        """Generate summary, extract key points, and analyze sentiment in one call"""
        if not self.client:
            return {
                "summary": "AI Summary not available (API Key missing)",
                "key_points": [],
                "sentiment_score": 0.0,
                "sentiment_label": "neutral"
            }
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are a news analysis assistant. Analyze the following article and provide:
1. A concise summary in Spanish (2-3 sentences)
2. 3-5 key points in Spanish
3. Sentiment analysis (score from -1.0 to 1.0 and label: positive/negative/neutral)

Respond with ONLY a JSON object in this exact format:
{
  "summary": "...",
  "key_points": ["...", "...", "..."],
  "sentiment_score": 0.0,
  "sentiment_label": "neutral"
}"""},
                    {"role": "user", "content": text}
                ],
                max_tokens=400
            )
            content = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            result = json.loads(content)
            return {
                "summary": result.get("summary", ""),
                "key_points": result.get("key_points", [])[:5],
                "sentiment_score": float(result.get("sentiment_score", 0.0)),
                "sentiment_label": result.get("sentiment_label", "neutral")
            }
        except Exception as e:
            print(f"Error enriching article: {e}")
            return {
                "summary": "Error generating analysis",
                "key_points": [],
                "sentiment_score": 0.0,
                "sentiment_label": "neutral"
            }

    async def generate_unified_summary(self, articles_data: List[Dict[str, str]]) -> Dict[str, any]:
        """Generate a comprehensive unified summary from multiple article sources"""
        if not self.client:
            return {
                "unified_summary": "Resumen unificado no disponible (falta la clave API)",
                "sources_count": 0,
                "key_insights": [],
                "overall_sentiment": "neutral"
            }
        
        if not articles_data:
            return {
                "unified_summary": "No hay artículos disponibles para generar el resumen",
                "sources_count": 0,
                "key_insights": [],
                "overall_sentiment": "neutral"
            }
        
        try:
            # Prepare the articles text
            articles_text = ""
            for i, article in enumerate(articles_data, 1):
                articles_text += f"\n\n--- Fuente {i}: {article.get('source_name', 'Desconocida')} ---\n"
                articles_text += f"Título: {article.get('title', '')}\n"
                articles_text += f"Contenido: {article.get('content', article.get('description', ''))}\n"
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """Eres un asistente experto en análisis de noticias. Tu tarea es crear un resumen unificado y completo a partir de múltiples fuentes de noticias sobre el mismo tema.

Debes proporcionar:
1. Un resumen unificado extenso (4-6 párrafos) que integre la información de todas las fuentes, eliminando redundancias y destacando los puntos más importantes
2. Una lista de 5-8 insights clave que emergen del análisis conjunto de todas las fuentes
3. El sentimiento general (positive/negative/neutral)

Responde SOLO con un objeto JSON en este formato exacto:
{
  "unified_summary": "...",
  "key_insights": ["...", "...", "..."],
  "overall_sentiment": "neutral"
}

El resumen debe ser objetivo, informativo y en español."""},
                    {"role": "user", "content": f"Analiza estas {len(articles_data)} fuentes sobre el mismo tema y genera un resumen unificado:\n{articles_text}"}
                ],
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            result = json.loads(content)
            return {
                "unified_summary": result.get("unified_summary", ""),
                "sources_count": len(articles_data),
                "key_insights": result.get("key_insights", [])[:8],
                "overall_sentiment": result.get("overall_sentiment", "neutral")
            }
        except Exception as e:
            print(f"Error generating unified summary: {e}")
            return {
                "unified_summary": "Error al generar el resumen unificado",
                "sources_count": len(articles_data),
                "key_insights": [],
                "overall_sentiment": "neutral"
            }

summary_service = SummaryService()
