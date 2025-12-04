import Foundation

struct FeedResponse: Codable {
    let items: [Article]
    let total: Int
    let page: Int
    let size: Int
    let pages: Int
}

class FeedService {
    static let shared = FeedService()
    private let networkManager = NetworkManager.shared
    
    private init() {}
    
    func getPersonalizedFeed(page: Int = 1, size: Int = 20) async throws -> FeedResponse {
        return try await networkManager.request(
            endpoint: "/articles/?limit=10&skip=0",
            method: "GET"
        )
    }
    
    func getTrendingArticles(page: Int = 1, size: Int = 20) async throws -> FeedResponse {
        return try await networkManager.request(
            endpoint: "/feed/trending?page=\(page)&size=\(size)",
            method: "GET"
        )
    }
    
    func getArticlesByCategory(category: String, page: Int = 1, size: Int = 20) async throws -> FeedResponse {
        return try await networkManager.request(
            endpoint: "/feed/category/\(category)?page=\(page)&size=\(size)",
            method: "GET"
        )
    }
}
