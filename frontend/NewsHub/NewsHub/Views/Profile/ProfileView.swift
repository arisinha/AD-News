import SwiftUI
import Combine

struct ProfileView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @EnvironmentObject var tabManager: TabManager
    @State private var showLoginSheet = false
    
    var body: some View {
        NavigationStack {
            List {
                Section {
                    HStack {
                        ZStack {
                            Circle()
                                .fill(authViewModel.isGuest ? Color.gray : Color.blue)
                                .frame(width: 60, height: 60)
                            
                            Text(authViewModel.isGuest ? "?" : (authViewModel.currentUser?.email.prefix(1).uppercased() ?? "U"))
                                .font(.title)
                                .fontWeight(.bold)
                                .foregroundColor(.white)
                        }
                        
                        VStack(alignment: .leading) {
                            Text(authViewModel.isGuest ? "Invitado" : (authViewModel.currentUser?.username ?? "Usuario"))
                                .font(.headline)
                            Text(authViewModel.isGuest ? "Sin cuenta" : (authViewModel.currentUser?.email ?? "usuario@ejemplo.com"))
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                    .padding(.vertical, 8)
                }
                
                Section {
                    NavigationLink(destination: Text("Preferencias")) {
                        Label("Preferencias de Contenido", systemImage: "slider.horizontal.3")
                    }
                    
                    NavigationLink(destination: Text("Notificaciones")) {
                        Label("Notificaciones", systemImage: "bell")
                    }
                    
                    NavigationLink(destination: Text("Privacidad")) {
                        Label("Privacidad", systemImage: "lock")
                    }
                }
                
                Section {
                    if authViewModel.isGuest {
                        // Guest - show login button
                        Button(action: {
                            showLoginSheet = true
                        }) {
                            Label("Iniciar Sesión", systemImage: "arrow.right.square")
                                .foregroundColor(.blue)
                        }
                    } else {
                        // Authenticated - show logout button
                        Button(action: {
                            authViewModel.logout()
                        }) {
                            Label("Cerrar Sesión", systemImage: "arrow.right.square")
                                .foregroundColor(.red)
                        }
                    }
                }
            }
            .navigationTitle("Perfil")
            .sheet(isPresented: $showLoginSheet) {
                NavigationStack {
                    LoginView()
                        .navigationBarTitleDisplayMode(.inline)
                        .toolbar {
                            ToolbarItem(placement: .navigationBarLeading) {
                                Button("Cancelar") {
                                    showLoginSheet = false
                                }
                            }
                        }
                }
            }
            .onChange(of: authViewModel.isAuthenticated) { _, isAuthenticated in
                if isAuthenticated && showLoginSheet {
                    // Close sheet and go to home tab
                    showLoginSheet = false
                    tabManager.goToHome()
                }
            }
        }
    }
}
