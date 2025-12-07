import SwiftUI
import Combine

struct MainTabView: View {
    @EnvironmentObject private var tabManager: TabManager
    
    var body: some View {
        TabView(selection: $tabManager.selectedTab) {
            FeedView()
                .tabItem {
                    Label("Inicio", systemImage: "house.fill")
                }
                .tag(0)
            
            LiveListView()
                .tabItem {
                    Label("En Vivo", systemImage: "video.fill")
                }
                .tag(1)
            
            SearchView()
                .tabItem {
                    Label("Buscar", systemImage: "magnifyingglass")
                }
                .tag(2)
            
            FavoritesView()
                .tabItem {
                    Label("Guardados", systemImage: "bookmark.fill")
                }
                .tag(3)
            
            ProfileView()
                .tabItem {
                    Label("Perfil", systemImage: "person.fill")
                }
                .tag(4)
        }
    }
}
