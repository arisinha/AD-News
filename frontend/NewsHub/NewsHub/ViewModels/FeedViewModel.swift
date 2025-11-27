import Foundation
import SwiftUI

@MainActor
class FeedViewModel: ObservableObject {
    @Published var articles: [Article] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var selectedCategory = "Todos"
    
    private let feedService = FeedService.shared
    
    let categories = ["Todos", "Tecnología", "Ciencia", "Economía", "Deportes", "Entretenimiento"]
    
    func loadArticles() async {
        isLoading = true
        errorMessage = nil
        
        do {
            if selectedCategory == "Todos" {
                articles = try await feedService.getFeed()
            } else {
                articles = try await feedService.getFeedByCategory(category: selectedCategory)
            }
        } catch {
            errorMessage = "Error al cargar noticias: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    func selectCategory(_ category: String) {
        selectedCategory = category
        Task {
            await loadArticles()
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
