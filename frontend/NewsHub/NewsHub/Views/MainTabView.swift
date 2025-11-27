struct MainTabView: View {
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            FeedView()
                .tabItem {
                    Label("Inicio", systemImage: "house.fill")
                }
                .tag(0)
            
            SearchPlaceholderView()
                .tabItem {
                    Label("Buscar", systemImage: "magnifyingglass")
                }
                .tag(1)
            
            FavoritesPlaceholderView()
                .tabItem {
                    Label("Guardados", systemImage: "bookmark.fill")
                }
                .tag(2)
            
            ProfileView()
                .tabItem {
                    Label("Perfil", systemImage: "person.fill")
                }
                .tag(3)
        }
    }
}
