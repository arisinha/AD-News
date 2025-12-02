import SwiftUI
import Combine

struct ProfileView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    
    var body: some View {
        NavigationStack {
            List {
                Section {
                    HStack {
                        ZStack {
                            Circle()
                                .fill(Color.blue)
                                .frame(width: 60, height: 60)
                            
                            Text(authViewModel.currentUser?.email.prefix(1).uppercased() ?? "U")
                                .font(.title)
                                .fontWeight(.bold)
                                .foregroundColor(.white)
                        }
                        
                        VStack(alignment: .leading) {
                            Text(authViewModel.currentUser?.username ?? "Usuario")
                                .font(.headline)
                            Text(authViewModel.currentUser?.email ?? "usuario@ejemplo.com")
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
                    Button(action: {
                        authViewModel.logout()
                    }) {
                        Label("Cerrar Sesión", systemImage: "arrow.right.square")
                            .foregroundColor(.red)
                    }
                }
            }
            .navigationTitle("Perfil")
        }
    }
}
