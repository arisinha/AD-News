import SwiftUI
import Combine

/// Manages app-wide theme settings (dark/light mode)
class ThemeManager: ObservableObject {
    /// Theme options: system, light, or dark
    enum Theme: String, CaseIterable {
        case system = "system"
        case light = "light"
        case dark = "dark"
        
        var displayName: String {
            switch self {
            case .system: return "Sistema"
            case .light: return "Claro"
            case .dark: return "Oscuro"
            }
        }
        
        var icon: String {
            switch self {
            case .system: return "circle.lefthalf.filled"
            case .light: return "sun.max.fill"
            case .dark: return "moon.fill"
            }
        }
        
        var colorScheme: ColorScheme? {
            switch self {
            case .system: return nil
            case .light: return .light
            case .dark: return .dark
            }
        }
    }
    
    @AppStorage("appTheme") private var storedTheme: String = Theme.system.rawValue
    
    @Published var currentTheme: Theme = .system {
        didSet {
            storedTheme = currentTheme.rawValue
        }
    }
    
    init() {
        // Load stored theme on init
        if let theme = Theme(rawValue: storedTheme) {
            currentTheme = theme
        }
    }
    
    /// Cycles through themes: system -> light -> dark -> system
    func cycleTheme() {
        switch currentTheme {
        case .system:
            currentTheme = .light
        case .light:
            currentTheme = .dark
        case .dark:
            currentTheme = .system
        }
    }
    
    /// Returns the appropriate ColorScheme for SwiftUI
    var preferredColorScheme: ColorScheme? {
        return currentTheme.colorScheme
    }
}
