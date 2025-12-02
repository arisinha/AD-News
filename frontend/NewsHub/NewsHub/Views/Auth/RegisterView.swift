import SwiftUI

struct RegisterView: View {
    @StateObject private var viewModel = AuthViewModel()
    @Environment(\.dismiss) private var dismiss
    
    @State private var email = ""
    @State private var username = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var showError = false
    @State private var localError = ""
    
    var body: some View {
        ZStack {
            // Fondo degradado
            LinearGradient(
                colors: [Color.blue, Color.purple],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 20) {
                    // Logo
                    ZStack {
                        Circle()
                            .fill(Color.white.opacity(0.2))
                            .frame(width: 100, height: 100)
                        
                        Circle()
                            .fill(Color.blue)
                            .frame(width: 80, height: 80)
                        
                        Text("N")
                            .font(.system(size: 40, weight: .bold))
                            .foregroundColor(.white)
                    }
                    .padding(.top, 50)
                    
                    Text("Crear Cuenta")
                        .font(.system(size: 32, weight: .bold))
                        .foregroundColor(.white)
                    
                    Text("Únete a NewsHub")
                        .foregroundColor(.white.opacity(0.9))
                        .padding(.bottom, 20)
                    
                    // Formulario
                    VStack(spacing: 15) {
                        // Email
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Email")
                                .foregroundColor(.white.opacity(0.9))
                                .font(.subheadline)
                            
                            TextField("tu@email.com", text: $email)
                                .textFieldStyle(RoundedTextFieldStyle())
                                .keyboardType(.emailAddress)
                                .textInputAutocapitalization(.never)
                        }
                        
                        // Username
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Nombre de Usuario")
                                .foregroundColor(.white.opacity(0.9))
                                .font(.subheadline)
                            
                            TextField("tu_usuario", text: $username)
                                .textFieldStyle(RoundedTextFieldStyle())
                                .textInputAutocapitalization(.never)
                        }
                        
                        // Password
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Contraseña")
                                .foregroundColor(.white.opacity(0.9))
                                .font(.subheadline)
                            
                            SecureField("••••••••", text: $password)
                                .textFieldStyle(RoundedTextFieldStyle())
                        }
                        
                        // Confirm Password
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Confirmar Contraseña")
                                .foregroundColor(.white.opacity(0.9))
                                .font(.subheadline)
                            
                            SecureField("••••••••", text: $confirmPassword)
                                .textFieldStyle(RoundedTextFieldStyle())
                        }
                        
                        // Error messages
                        if showError || viewModel.errorMessage != nil {
                            Text(localError.isEmpty ? (viewModel.errorMessage ?? "") : localError)
                                .foregroundColor(.red)
                                .font(.caption)
                                .padding(.horizontal)
                        }
                        
                        // Botón Registro
                        Button(action: handleRegister) {
                            if viewModel.isLoading {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            } else {
                                Text("Crear Cuenta")
                                    .font(.headline)
                                    .foregroundColor(.blue)
                            }
                        }
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.white)
                        .cornerRadius(12)
                        .disabled(viewModel.isLoading)
                        
                        Button(action: { dismiss() }) {
                            Text("¿Ya tienes cuenta? Inicia sesión")
                                .foregroundColor(.white)
                                .underline()
                        }
                        .padding(.top, 10)
                    }
                    .padding(.horizontal, 30)
                }
            }
        }
        .navigationBarBackButtonHidden(true)
        .toolbar {
            ToolbarItem(placement: .navigationBarLeading) {
                Button(action: { dismiss() }) {
                    Image(systemName: "chevron.left")
                        .foregroundColor(.white)
                }
            }
        }
    }
    
    private func handleRegister() {
        localError = ""
        showError = false
        
        if password != confirmPassword {
            localError = "Las contraseñas no coinciden"
            showError = true
            return
        }
        
        if password.count < 6 {
            localError = "La contraseña debe tener al menos 6 caracteres"
            showError = true
            return
        }
        
        Task {
            await viewModel.register(email: email, username: username, password: password)
            if viewModel.isAuthenticated {
                dismiss()
            }
        }
    }
}

struct RoundedTextFieldStyle: TextFieldStyle {
    func _body(configuration: TextField<Self._Label>) -> some View {
        configuration
            .padding()
            .background(Color.white)
            .cornerRadius(10)
    }
}
