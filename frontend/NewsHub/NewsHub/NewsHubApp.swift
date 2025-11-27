//
//  NewsHubApp.swift
//  NewsHub
//
//  Created by Carlos Eduardo Rios Cazares on 25/11/25.
//

import SwiftUI

@main
struct NewsHubApp: App {
    @StateObject private var authViewModel = AuthViewModel()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authViewModel)
        }
    }
}
