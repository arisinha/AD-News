import SwiftUI

struct ArticleDetailView: View {
    let article: Article
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject private var authViewModel: AuthViewModel
    @EnvironmentObject private var tabManager: TabManager
    @State private var isFavorite = false
    @State private var showLoginAlert = false
    @State private var showLoginSheet = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // Categoría
                Text(article.category)
                    .font(.caption)
                    .fontWeight(.semibold)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(Color.blue.opacity(0.1))
                    .foregroundColor(.blue)
                    .cornerRadius(12)
                
                // Título
                Text(article.title)
                    .font(.title)
                    .fontWeight(.bold)
                
                // Metadata
                HStack(spacing: 16) {
                    Label(formatDate(article.publishedAt), systemImage: "calendar")
                    Label(article.sourceName, systemImage: "tag")
                }
                .font(.caption)
                .foregroundColor(.secondary)
                
                // Imagen
                if let imageUrl = article.imageUrl, let url = URL(string: imageUrl) {
                    AsyncImage(url: url) { phase in
                        switch phase {
                        case .empty:
                            Rectangle()
                                .fill(Color.gray.opacity(0.2))
                                .frame(height: 250)
                                .overlay(ProgressView())
                        case .success(let image):
                            image
                                .resizable()
                                .aspectRatio(contentMode: .fill)
                                .frame(maxHeight: 300)
                                .clipped()
                                .cornerRadius(12)
                        case .failure:
                            Rectangle()
                                .fill(Color.gray.opacity(0.2))
                                .frame(height: 250)
                                .cornerRadius(12)
                        @unknown default:
                            EmptyView()
                        }
                    }
                }
                
                // Resumen AI (si existe)
                if let aiSummary = article.aiSummary {
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Image(systemName: "sparkles")
                                .foregroundColor(.blue)
                            Text("Resumen IA")
                                .font(.headline)
                                .foregroundColor(.blue)
                        }
                        Text(aiSummary)
                            .font(.body)
                    }
                    .padding()
                    .background(Color.blue.opacity(0.05))
                    .cornerRadius(12)
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(Color.blue, lineWidth: 2)
                    )
                }
                
                // Puntos Clave
                if !article.keyPoints.isEmpty {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Puntos Clave")
                            .font(.headline)
                            .padding(.bottom, 4)
                        
                        ForEach(article.keyPoints, id: \.self) { point in
                            HStack(alignment: .top, spacing: 8) {
                                Circle()
                                    .fill(Color.blue)
                                    .frame(width: 6, height: 6)
                                    .padding(.top, 6)
                                
                                Text(point)
                                    .font(.body)
                            }
                        }
                    }
                    .padding()
                    .background(Color.gray.opacity(0.05))
                    .cornerRadius(12)
                }

                // Botón para leer artículo completo
                if let url = URL(string: article.url) {
                    Link(destination: url) {
                        HStack {
                            Spacer()
                            Text("Leer Artículo Completo")
                                .font(.headline)
                            Image(systemName: "arrow.up.right")
                            Spacer()
                        }
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(12)
                    }
                }
            }
            .padding()
        }
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                HStack(spacing: 16) {
                    Button(action: {
                        // Compartir
                    }) {
                        Image(systemName: "square.and.arrow.up")
                    }
                    
                    Button(action: {
                        handleFavoriteAction()
                    }) {
                        Image(systemName: isFavorite ? "heart.fill" : "heart")
                            .foregroundColor(isFavorite ? .red : .primary)
                    }
                }
            }
        }
        #endif
        .task {
            await checkFavoriteStatus()
        }
        .alert("Iniciar Sesión Requerido", isPresented: $showLoginAlert) {
            Button("Iniciar Sesión") {
                showLoginSheet = true
            }
            Button("Cancelar", role: .cancel) { }
        } message: {
            Text("Para guardar artículos en favoritos necesitas crear una cuenta o iniciar sesión.")
        }
        .sheet(isPresented: $showLoginSheet) {
            NavigationStack {
                LoginView()
                    .navigationBarTitleDisplayMode(.inline)
                    .toolbar {
                        ToolbarItem(placement: .navigationBarLeading) {
                            Button("Cancelar") {
                                showLoginSheet = false
                            }
                        }
                    }
            }
        }
        .onChange(of: authViewModel.isAuthenticated) { _, isAuthenticated in
            if isAuthenticated && showLoginSheet {
                // Close sheet and go to home
                showLoginSheet = false
                dismiss()
                tabManager.goToHome()
            }
        }
    }
    
    private func formatDate(_ dateString: String) -> String {
        let formatter = ISO8601DateFormatter()
        guard let date = formatter.date(from: dateString) else {
            return dateString
        }
        
        let displayFormatter = DateFormatter()
        displayFormatter.dateStyle = .long
        displayFormatter.locale = Locale(identifier: "es_ES")
        return displayFormatter.string(from: date)
    }
    
    private func checkFavoriteStatus() async {
        // Only check if user is authenticated
        if authViewModel.isAuthenticated {
            isFavorite = await FavoriteService.shared.checkIfFavorite(articleId: article.id)
        }
    }
    
    private func handleFavoriteAction() {
        // Check if user is guest
        if authViewModel.isGuest {
            showLoginAlert = true
            return
        }
        
        // User is authenticated, proceed with favorite toggle
        Task {
            await toggleFavorite()
        }
    }
    
    private func toggleFavorite() async {
        let previousState = isFavorite
        isFavorite.toggle() // Optimistic update
        
        do {
            if isFavorite {
                try await FavoriteService.shared.addFavorite(articleId: article.id)
            } else {
                try await FavoriteService.shared.removeFavorite(articleId: article.id)
            }
        } catch {
            isFavorite = previousState // Revert on error
            print("Error toggling favorite: \(error)")
        }
    }
}

