import Foundation

struct Article: Codable, Identifiable {
    let id: String
    let title: String
    let description: String?
    let content: String?
    let author: String?
    let url: String
    let imageUrl: String?
    let sourceName: String
    let publishedAt: String
    let category: String
    let region: String?
    let sentimentScore: Double
    let sentimentLabel: String
    let relevanceScore: Double
    let aiSummary: String?
    let keyPoints: [String]
    let topicId: String?
    let createdAt: String
    
    enum CodingKeys: String, CodingKey {
        case id, title, description, content, author, url, category, region
        case imageUrl = "image_url"
        case sourceName = "source_name"
        case publishedAt = "published_at"
        case sentimentScore = "sentiment_score"
        case sentimentLabel = "sentiment_label"
        case relevanceScore = "relevance_score"
        case aiSummary = "ai_summary"
        case keyPoints = "key_points"
        case topicId = "topic_id"
        case createdAt = "created_at"
    }
}
