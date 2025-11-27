//
//  ContentView.swift
//  NewsHub
//
//  Created by Carlos Eduardo Rios Cazares on 25/11/25.
//

struct ContentView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    
    var body: some View {
        Group {
            if authViewModel.isAuthenticated {
                MainTabView()
            } else {
                LoginView()
            }
        }
    }
}
