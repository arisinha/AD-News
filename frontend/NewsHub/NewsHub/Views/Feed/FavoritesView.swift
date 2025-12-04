import SwiftUI

struct FavoritesView: View {
    @State private var favorites: [Article] = []
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationStack {
            VStack {
                if isLoading {
                    ProgressView()
                        .padding()
                } else if let error = errorMessage {
                    VStack(spacing: 16) {
                        Image(systemName: "exclamationmark.triangle")
                            .font(.system(size: 50))
                            .foregroundColor(.orange)
                        Text(error)
                            .multilineTextAlignment(.center)
                            .foregroundColor(.secondary)
                        Button("Reintentar") {
                            Task {
                                await loadFavorites()
                            }
                        }
                        .buttonStyle(.bordered)
                    }
                    .padding()
                } else if favorites.isEmpty {
                    VStack(spacing: 16) {
                        Image(systemName: "bookmark")
                            .font(.system(size: 50))
                            .foregroundColor(.gray)
                        Text("No tienes artículos guardados")
                            .foregroundColor(.secondary)
                        Text("Guarda artículos para leerlos más tarde")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                } else {
                    ScrollView {
                        LazyVStack(spacing: 16) {
                            ForEach(favorites) { article in
                                NavigationLink(destination: ArticleDetailView(article: article)) {
                                    ArticleCardView(article: article)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding()
                    }
                    .refreshable {
                        await loadFavorites()
                    }
                }
            }
            .navigationTitle("Guardados")
            .task {
                await loadFavorites()
            }
        }
    }
    
    private func loadFavorites() async {
        isLoading = true
        errorMessage = nil
        
        do {
            let response = try await FavoriteService.shared.getFavorites()
            favorites = response.items
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
}

