import SwiftUI

struct LoginView: View {
    @EnvironmentObject var viewModel: AuthViewModel
    @State private var username = ""
    @State private var password = ""
    @State private var showRegister = false
    

    var body: some View {
        NavigationStack {
            ZStack {
                VStack(spacing: 20) {
                    Spacer()
                    
                    Text("AD News")
                        .font(.system(size: 40, weight: .bold))
                        .foregroundColor(.black)
                    
                    Text("Tu fuente de noticias personalizada")
                        .foregroundColor(.black.opacity(0.9))
                        .padding(.bottom, 30)
                    
                    // Formularioc
                    VStack(spacing: 15) {
                        // Usuario
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Usuario")
                                .foregroundColor(.black.opacity(0.2))
                                .font(.subheadline)
                            
                            TextField("Usuario", text: $username)
                                .padding()
                                .background(Color(.systemGray6))
                                .cornerRadius(10)
                                .foregroundColor(.black)
                                .textInputAutocapitalization(.never)
                                
                        }
                        
                        // Contraseña
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Contraseña")
                                .foregroundColor(.black.opacity(0.9))
                                .font(.subheadline)
                                .autocorrectionDisabled()
                            
                            SecureField("••••••••", text: $password)
                                .padding()
                                .background(Color(.systemGray6))
                                .cornerRadius(8)
                                .foregroundColor(.black)
                        }
                        
                        // Error message
                        if let error = viewModel.errorMessage {
                            Text(error)
                                .foregroundColor(.red)
                                .font(.caption)
                                .padding(.horizontal)
                        }
                        
                        // Botón Login
                        Button(action: {
                            Task {
                                await viewModel.login(username: username, password: password)
                            }
                        }) {
                            if viewModel.isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            } else {
                                Text("Iniciar Sesión")
                                    .font(.headline)
                                    .foregroundColor(.white)
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.blue)
                        .cornerRadius(12)
                        .disabled(viewModel.isLoading)
                        
                        // Divisor
                        HStack {
                            Rectangle()
                                .fill(Color.black.opacity(0.3))
                                .frame(height: 1)
                            Text("o")
                                .foregroundColor(.black.opacity(0.7))
                            Rectangle()
                                .fill(Color.black.opacity(0.3))
                                .frame(height: 1)
                        }
                        .padding(.vertical, 10)
                        
                        // Botón Registro
                        Button(action: {
                            showRegister = true
                        }) {
                            Text("Crear Cuenta Nueva")
                                .font(.headline)
                                .foregroundColor(.black)
                        }
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.blue.opacity(0.2))
                        .cornerRadius(12)
                    }
                    .padding(.horizontal, 30)
                    Spacer()
                    Spacer()
                }
            }
            .navigationDestination(isPresented: $showRegister) {
                RegisterView()
            }
        }
    }
}
