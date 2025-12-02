import SwiftUI

struct SearchView: View {
    @State private var searchText = ""
    @State private var searchResults: [Article] = []
    @State private var isSearching = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationStack {
            VStack {
                if isSearching {
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
                    }
                    .padding()
                } else if searchResults.isEmpty && !searchText.isEmpty {
                    VStack(spacing: 16) {
                        Image(systemName: "magnifyingglass")
                            .font(.system(size: 50))
                            .foregroundColor(.gray)
                        Text("No se encontraron resultados")
                            .foregroundColor(.secondary)
                    }
                    .padding()
                } else if searchResults.isEmpty {
                    VStack(spacing: 16) {
                        Image(systemName: "magnifyingglass")
                            .font(.system(size: 50))
                            .foregroundColor(.gray)
                        Text("Busca noticias por título, descripción o contenido")
                            .multilineTextAlignment(.center)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                } else {
                    ScrollView {
                        LazyVStack(spacing: 16) {
                            ForEach(searchResults) { article in
                                NavigationLink(destination: ArticleDetailView(article: article)) {
                                    ArticleCardView(article: article)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding()
                    }
                }
            }
            .navigationTitle("Buscar")
            .searchable(text: $searchText, prompt: "Buscar noticias...")
            .onChange(of: searchText) { _, newValue in
                Task {
                    await performSearch(query: newValue)
                }
            }
        }
    }
    
    private func performSearch(query: String) async {
        guard !query.isEmpty else {
            searchResults = []
            return
        }
        
        // Debounce search
        try? await Task.sleep(nanoseconds: 500_000_000) // 0.5 seconds
        
        guard searchText == query else { return }
        
        isSearching = true
        errorMessage = nil
        
        do {
            let response: ArticlesResponse = try await ArticleService.shared.searchArticles(query: query)
            searchResults = response.items
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isSearching = false
    }
}
