from openai import AsyncOpenAI
from app.core.config import settings

class SummaryService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_summary(self, text: str) -> str:
        if not settings.OPENAI_API_KEY:
            return "AI Summary not available (API Key missing)"
            
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
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

summary_service = SummaryService()
