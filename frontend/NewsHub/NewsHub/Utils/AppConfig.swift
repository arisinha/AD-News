import Foundation

enum AppConfig {
    // MARK: - API Configuration
    
    /// Base URL for the backend API
    /// Change this to match your backend server URL
    /// Examples:
    /// - Local development: "http://localhost:8000/api/v1"
    /// - Production: "https://your-backend.com/api/v1"
    static let baseURL = "http://localhost:8000/api/v1"
    
    // MARK: - App Settings
    
    /// Default number of articles to fetch per page
    static let defaultPageSize = 20
    
    /// Maximum number of articles to cache
    static let maxCachedArticles = 100
    
    /// Enable debug logging
    static let debugMode = true
}
