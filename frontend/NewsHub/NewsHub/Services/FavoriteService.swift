import Foundation

class FavoriteService {
    static let shared = FavoriteService()
    private let networkManager = NetworkManager.shared
    
    private init() {}
    
    func getFavorites(page: Int = 1, size: Int = 20) async throws -> FavoritesResponse {
        return try await networkManager.request(
            endpoint: "/user/favorites/?page=\(page)&size=\(size)",
            method: "GET"
        )
    }
    
    func addFavorite(articleId: String) async throws {
        let body = ["article_id": articleId]
        let _: FavoriteResponse = try await networkManager.request(
            endpoint: "/user/favorites/",
            method: "POST",
            body: body
        )
    }
    
    func removeFavorite(articleId: String) async throws {
        let _: FavoriteResponse = try await networkManager.request(
            endpoint: "/user/favorites/article/\(articleId)",
            method: "DELETE"
        )
    }
    
    func checkIfFavorite(articleId: String) async -> Bool {
        // This is a bit inefficient, but without a specific endpoint, we check the list.
        // Ideally we should have an endpoint HEAD /user/favorites/article/{id}
        do {
            let response = try await getFavorites(size: 100)
            return response.items.contains(where: { $0.id == articleId })
        } catch {
            return false
        }
    }
}
