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
    @StateObject private var themeManager = ThemeManager()
    @StateObject private var tabManager = TabManager()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authViewModel)
                .environmentObject(themeManager)
                .environmentObject(tabManager)
                .preferredColorScheme(themeManager.preferredColorScheme)
        }
    }
}
