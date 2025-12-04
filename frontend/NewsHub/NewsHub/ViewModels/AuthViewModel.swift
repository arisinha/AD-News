import Foundation
import SwiftUI
import Combine

@MainActor
class AuthViewModel: ObservableObject {
    @Published var isAuthenticated = false
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var currentUser: User?
    
    private let authService = AuthService.shared
    
    init() {
        checkAuthStatus()
    }
    
    func checkAuthStatus() {
        isAuthenticated = authService.isAuthenticated()
        if isAuthenticated {
            currentUser = authService.getCurrentUser()
        }
    }
    
    func login(username: String, password: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            _ = try await authService.login(username: username, password: password)
            currentUser = authService.getCurrentUser()
            isAuthenticated = true
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func register(email: String, username: String, password: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let user = try await authService.register(
                email: email,
                username: username,
                password: password
            )
            
            // Después de registrar, hacer login automático
            _ = try await authService.login(username: username, password: password)
            
            currentUser = user
            isAuthenticated = true
        } catch {
            errorMessage = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func logout() {
        authService.logout()
        isAuthenticated = false
        currentUser = nil
    }
}
