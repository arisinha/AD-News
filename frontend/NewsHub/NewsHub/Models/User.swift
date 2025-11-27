import Foundation

struct UserPreferences: Codable {
    var categories: [String]?
    var regions: [String]?
    var language: String?
    var notificationsEnabled: Bool?
    var darkMode: Bool?
    
    enum CodingKeys: String, CodingKey {
        case categories, regions, language
        case notificationsEnabled = "notifications_enabled"
        case darkMode = "dark_mode"
    }
}

struct User: Codable, Identifiable {
    let id: String
    let email: String
    let username: String?
    let isActive: Bool
    let preferences: UserPreferences
    
    enum CodingKeys: String, CodingKey {
        case id, email, username, preferences
        case isActive = "is_active"
    }
}
