import SwiftUI

struct LoginView: View {
    @StateObject private var viewModel = AuthViewModel()
    @State private var email = ""
    @State private var password = ""
    @State private var showRegister = false
    
    var body: some View {
        NavigationStack {
            ZStack {
                // Fondo degradado
                LinearGradient(
                    colors: [Color.blue, Color.purple],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                VStack(spacing: 20) {
                    Spacer()
                    
                    // Logo
                    ZStack {
                        Circle()
                            .fill(Color.white.opacity(0.2))
                            .frame(width: 120, height: 120)
                        
                        Circle()
                            .fill(Color.blue)
                            .frame(width: 100, height: 100)
                        
                        Text("N")
                            .font(.system(size: 50, weight: .bold))
                            .foregroundColor(.white)
                    }
                    
                    Text("NewsHub")
                        .font(.system(size: 40, weight: .bold))
                        .foregroundColor(.white)
                    
                    Text("Tu fuente de noticias personalizada")
                        .foregroundColor(.white.opacity(0.9))
                        .padding(.bottom, 30)
                    
                    // Formulario
                    VStack(spacing: 15) {
                        // Email
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Email")
                                .foregroundColor(.white.opacity(0.9))
                                .font(.subheadline)
                            
                            TextField("tu@email.com", text: $email)
                                .textFieldStyle(RoundedTextFieldStyle())
                                .textInputAutocapitalization(.never)
                                .keyboardType(.emailAddress)
                        }
                        
                        // Contraseña
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Contraseña")
                                .foregroundColor(.white.opacity(0.9))
                                .font(.subheadline)
                            
                            SecureField("••••••••", text: $password)
                                .textFieldStyle(RoundedTextFieldStyle())
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
                                await viewModel.login(email: email, password: password)
                            }
                        }) {
                            if viewModel.isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            } else {
                                Text("Iniciar Sesión")
                                    .font(.headline)
                                    .foregroundColor(.blue)
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.white)
                        .cornerRadius(12)
                        .disabled(viewModel.isLoading)
                        
                        // Divisor
                        HStack {
                            Rectangle()
                                .fill(Color.white.opacity(0.3))
                                .frame(height: 1)
                            Text("o")
                                .foregroundColor(.white.opacity(0.7))
                            Rectangle()
                                .fill(Color.white.opacity(0.3))
                                .frame(height: 1)
                        }
                        .padding(.vertical, 10)
                        
                        // Botón Registro
                        Button(action: {
                            showRegister = true
                        }) {
                            Text("Crear Cuenta Nueva")
                                .font(.headline)
                                .foregroundColor(.white)
                        }
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.white.opacity(0.2))
                        .cornerRadius(12)
                    }
                    .padding(.horizontal, 30)
                    
                    Spacer()
                }
            }
            .navigationDestination(isPresented: $showRegister) {
                RegisterView()
            }
        }
    }
}
