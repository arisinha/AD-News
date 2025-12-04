import Foundation

struct FavoriteResponse: Codable {
    let id: String
    let userId: String
    let articleId: String
    let collectionName: String?
    let createdAt: String
    
    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case articleId = "article_id"
        case collectionName = "collection_name"
        case createdAt = "created_at"
    }
}

struct FavoritesResponse: Codable {
    let items: [Article]
    let total: Int
    let page: Int
    let size: Int
}
