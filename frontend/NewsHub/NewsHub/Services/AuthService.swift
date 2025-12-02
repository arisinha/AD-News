import Foundation

class AuthService {
    static let shared = AuthService()
    private let networkManager = NetworkManager.shared
    
    private let tokenKey = "auth_token"
    private let userKey = "current_user"
    
    private init() {}
    
    func isAuthenticated() -> Bool {
        return UserDefaults.standard.string(forKey: tokenKey) != nil
    }
    
    func login(email: String, password: String) async throws -> AuthResponse {
        let loginRequest = LoginRequest(username: email, password: password)
        
        let response: AuthResponse = try await networkManager.request(
            endpoint: "/auth/login",
            method: "POST",
            body: loginRequest,
            requiresAuth: false
        )
        
        // Save token
        UserDefaults.standard.set(response.accessToken, forKey: tokenKey)
        
        // Fetch and save user data
        try await fetchCurrentUser()
        
        return response
    }
    
    func register(email: String, username: String, password: String) async throws -> User {
        let registerRequest = RegisterRequest(
            email: email,
            username: username,
            password: password
        )
        
        let user: User = try await networkManager.request(
            endpoint: "/auth/register",
            method: "POST",
            body: registerRequest,
            requiresAuth: false
        )
        
        return user
    }
    
    func fetchCurrentUser() async throws {
        let user: User = try await networkManager.request(
            endpoint: "/users/me",
            method: "GET",
            requiresAuth: true
        )
        
        // Save user data
        if let encoded = try? JSONEncoder().encode(user) {
            UserDefaults.standard.set(encoded, forKey: userKey)
        }
    }
    
    func getCurrentUser() -> User? {
        guard let data = UserDefaults.standard.data(forKey: userKey) else {
            return nil
        }
        return try? JSONDecoder().decode(User.self, from: data)
    }
    
    func logout() {
        UserDefaults.standard.removeObject(forKey: tokenKey)
        UserDefaults.standard.removeObject(forKey: userKey)
    }
}
