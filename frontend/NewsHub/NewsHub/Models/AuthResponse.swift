import Foundation

struct AuthResponse: Codable {
    let accessToken: String
    let tokenType: String
    
    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case tokenType = "token_type"
    }
}

struct LoginRequest: Codable {
    let username: String  
    let password: String
}

struct RegisterRequest: Codable {
    let email: String
    let username: String
    let password: String
}
