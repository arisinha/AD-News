import SwiftUI

struct FavoritesView: View {
    @EnvironmentObject private var authViewModel: AuthViewModel
    @EnvironmentObject private var tabManager: TabManager
    @State private var favorites: [Article] = []
    @State private var isLoading = false
    @State private var errorMessage: String?
    @State private var showLoginSheet = false
    
    var body: some View {
        NavigationStack {
            VStack {
                // Check if user is guest
                if authViewModel.isGuest {
                    // Guest mode - show login prompt
                    VStack(spacing: 20) {
                        Image(systemName: "person.crop.circle.badge.questionmark")
                            .font(.system(size: 60))
                            .foregroundColor(.blue)
                        
                        Text("Inicia sesión para guardar artículos")
                            .font(.headline)
                            .foregroundColor(.primary)
                        
                        Text("Crea una cuenta o inicia sesión para guardar tus artículos favoritos y acceder a ellos desde cualquier dispositivo.")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal)
                        
                        Button {
                            showLoginSheet = true
                        } label: {
                            Text("Iniciar Sesión")
                                .font(.headline)
                                .foregroundColor(.white)
                                .padding(.horizontal, 40)
                                .padding(.vertical, 14)
                                .background(Color.blue)
                                .cornerRadius(12)
                        }
                        .padding(.top, 8)
                    }
                    .padding()
                } else if isLoading {
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
                if authViewModel.isAuthenticated {
                    await loadFavorites()
                }
            }
            .onChange(of: authViewModel.isAuthenticated) { _, isAuthenticated in
                if isAuthenticated {
                    // Close sheet and go to home if sheet was open
                    if showLoginSheet {
                        showLoginSheet = false
                        tabManager.goToHome()
                    } else {
                        Task {
                            await loadFavorites()
                        }
                    }
                }
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
