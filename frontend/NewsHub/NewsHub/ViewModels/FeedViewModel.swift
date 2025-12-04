import Foundation
import SwiftUI
import Combine

@MainActor
class FeedViewModel: ObservableObject {
    @Published var articles: [Article] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var selectedCategory = "Todos"
    
    private let feedService = FeedService.shared
    
    // Display names for UI
    let categories = ["Todos", "Tecnología", "Ciencia", "Negocios", "Deportes", "Entretenimiento", "Salud", "Educación"]
    
    // Mapping from Spanish display names to English API values
    private let categoryMapping: [String: String] = [
        "Todos": "all",
        "Tecnología": "technology",
        "Ciencia": "science",
        "Negocios": "business",
        "Deportes": "sports",
        "Entretenimiento": "entertainment",
        "Salud": "health",
        "Educación": "education"
    ]
    
    enum FeedType {
        case personalized
        case trending
        case category(String)
    }
    
    func loadFeed(filter: FeedType = .personalized) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let response: FeedResponse
            switch filter {
            case .personalized:
                response = try await feedService.getPersonalizedFeed()
            case .trending:
                response = try await feedService.getTrendingArticles()
            case .category(let category):
                // Map Spanish category name to English API value
                let apiCategory = categoryMapping[category] ?? category.lowercased()
                response = try await feedService.getArticlesByCategory(category: apiCategory)
            }
            articles = response.items
        } catch {
            errorMessage = "Error al cargar noticias: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    func selectCategory(_ category: String) {
        selectedCategory = category
        Task {
            await loadFeed(filter: .category(category))
        }
    }
    
    func formatDate(_ dateString: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: dateString) else {
            return dateString
        }
        
        let now = Date()
        let diffComponents = Calendar.current.dateComponents([.hour, .day], from: date, to: now)
        
        if let hours = diffComponents.hour, hours < 24 {
            if hours == 0 {
                return "Hace unos minutos"
            }
            return "Hace \(hours) hora\(hours > 1 ? "s" : "")"
        }
        
        if let days = diffComponents.day, days < 7 {
            return "Hace \(days) día\(days > 1 ? "s" : "")"
        }
        
        let displayFormatter = DateFormatter()
        displayFormatter.dateStyle = .medium
        displayFormatter.locale = Locale(identifier: "es_ES")
        return displayFormatter.string(from: date)
    }
}
