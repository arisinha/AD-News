# Resumen Unificado de Múltiples Fuentes

## Descripción

El endpoint `/v1/articles/{article_id}/unified-summary` genera un resumen extenso y completo combinando información de múltiples fuentes relacionadas sobre el mismo tema.

## Endpoint

```
GET /v1/articles/{article_id}/unified-summary
```

## Parámetros

- `article_id` (path parameter): ID del artículo principal

## Respuesta

```json
{
  "article": {
    // Información completa del artículo principal
    "id": "string",
    "title": "string",
    "description": "string",
    "content": "string",
    "author": "string",
    "url": "string",
    "image_url": "string",
    "source_name": "string",
    "published_at": "string",
    "category": "string",
    "region": "string",
    "sentiment_score": 0.0,
    "sentiment_label": "string",
    "ai_summary": "string",
    "key_points": ["string"],
    "created_at": "datetime"
  },
  "unified_summary": "string",  // Resumen extenso de 4-6 párrafos combinando todas las fuentes
  "key_insights": ["string"],   // 5-8 insights clave del análisis conjunto
  "overall_sentiment": "string", // Sentimiento general (positive/negative/neutral)
  "sources_analyzed": 0,         // Número de fuentes analizadas
  "related_articles": [          // Artículos relacionados usados en el resumen
    {
      "id": "string",
      "title": "string",
      "source_name": "string",
      "published_at": "string"
    }
  ]
}
```

## Funcionamiento

1. **Obtiene el artículo principal** usando el `article_id` proporcionado
2. **Busca artículos relacionados** de la misma categoría (hasta 4 artículos adicionales)
3. **Genera un resumen unificado** usando IA que:
   - Combina información de todas las fuentes
   - Elimina redundancias
   - Destaca los puntos más importantes
   - Proporciona un análisis completo de 4-6 párrafos
4. **Extrae insights clave** (5-8 puntos) del análisis conjunto
5. **Analiza el sentimiento general** del tema

## Ejemplo de Uso

### Request
```bash
curl http://localhost:8000/v1/articles/69275fa3c13072d7494b1f24/unified-summary
```

### Response (ejemplo simplificado)
```json
{
  "article": {
    "title": "Avances en Inteligencia Artificial transforman la industria tecnológica",
    "category": "technology",
    ...
  },
  "unified_summary": "En los últimos tiempos, la inteligencia artificial (IA) está revolucionando la industria tecnológica a un ritmo acelerado... [4-6 párrafos completos]",
  "key_insights": [
    "La inteligencia artificial está revolucionando la industria tecnológica",
    "Las energías renovables están alcanzando niveles récord de inversión",
    "Ambos sectores están alineados con las tendencias hacia la sostenibilidad",
    ...
  ],
  "overall_sentiment": "positive",
  "sources_analyzed": 2,
  "related_articles": [
    {
      "id": "69275fa5c13072d7494b1f29",
      "title": "Innovación en energías renovables alcanza récord histórico",
      "source_name": "Energía Verde"
    }
  ]
}
```

## Casos de Uso

### En la App Móvil

Cuando un usuario hace clic en una noticia:

1. **Vista inicial**: Muestra el artículo principal con su resumen corto (`ai_summary`)
2. **Botón "Ver análisis completo"**: Al hacer clic, carga el resumen unificado
3. **Sección de insights**: Muestra los puntos clave en formato de lista
4. **Fuentes relacionadas**: Lista de artículos relacionados que se usaron en el análisis
5. **Indicador de sentimiento**: Badge visual mostrando el sentimiento general

### Ventajas

- ✅ **Información completa**: El usuario obtiene una visión integral del tema
- ✅ **Múltiples perspectivas**: Combina información de diferentes fuentes
- ✅ **Ahorro de tiempo**: No necesita leer múltiples artículos
- ✅ **Insights valiosos**: Puntos clave extraídos automáticamente
- ✅ **Contexto amplio**: Entiende mejor el tema con información de varias fuentes

## Notas Técnicas

- El sistema busca hasta 5 artículos relacionados de la misma categoría
- Usa GPT-4o-mini para generar el resumen unificado
- El resumen es más extenso (4-6 párrafos) que el resumen individual
- Se generan entre 5-8 insights clave
- El análisis de sentimiento es general para todo el tema
