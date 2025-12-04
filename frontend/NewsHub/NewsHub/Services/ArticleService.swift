import Foundation

struct ArticlesResponse: Codable {
    let items: [Article]
    let total: Int
    let page: Int
    let size: Int
    let pages: Int
}

class ArticleService {
    static let shared = ArticleService()
    private let networkManager = NetworkManager.shared
    
    private init() {}
    
    func getArticles(page: Int = 1, size: Int = 20) async throws -> ArticlesResponse {
        return try await networkManager.request(
            endpoint: "/articles?limit=\(page)&size=\(size)",
            method: "GET"
        )
    }
    
    func getArticleById(_ id: String) async throws -> Article {
        return try await networkManager.request(
            endpoint: "/articles/\(id)",
            method: "GET"
        )
    }
    
    func searchArticles(query: String, page: Int = 1, size: Int = 20) async throws -> ArticlesResponse {
        let encodedQuery = query.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? query
        return try await networkManager.request(
            endpoint: "/articles/search?q=\(encodedQuery)&page=\(page)&size=\(size)",
            method: "GET"
        )
    }
}
