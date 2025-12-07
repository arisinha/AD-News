import Foundation

enum AppConfig {
    // MARK: - API Configuration

    static let baseURL = "https://ad-news-wdp3.vercel.app/v1"
    
    // MARK: - App Settings
    
    /// Default number of articles to fetch per page
    static let defaultPageSize = 20
    
    /// Maximum number of articles to cache
    static let maxCachedArticles = 100
    
    /// Enable debug logging
    static let debugMode = true
}
