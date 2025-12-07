import SwiftUI
import Combine

/// Manages the selected tab across the app
class TabManager: ObservableObject {
    @Published var selectedTab: Int = 0
    
    func goToHome() {
        selectedTab = 0
    }
    
    func goToLive() {
        selectedTab = 1
    }
    
    func goToSearch() {
        selectedTab = 2
    }
    
    func goToFavorites() {
        selectedTab = 3
    }
    
    func goToProfile() {
        selectedTab = 4
    }
}
