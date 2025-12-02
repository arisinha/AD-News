import Foundation
import SwiftUI
import Combine

@MainActor
class ArticleViewModel: ObservableObject {
    @Published var article: Article?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let articleService = ArticleService.shared
    
    func loadArticle(id: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            article = try await articleService.getArticle(id: id)
        } catch {
            errorMessage = "Error al cargar el artículo: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
}
