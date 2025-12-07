import SwiftUI

/// Full-screen view for playing a YouTube live stream
struct LivePlayerView: View {
    let liveStream: LiveStream
    @Environment(\.dismiss) private var dismiss
    @Environment(\.verticalSizeClass) private var verticalSizeClass
    @State private var isLoading = true
    @State private var showControls = true
    
    private var isLandscape: Bool {
        verticalSizeClass == .compact
    }
    
    var body: some View {
        ZStack {
            // Background
            Color.black.edgesIgnoringSafeArea(.all)
            
            if liveStream.live, let videoId = liveStream.videoId {
                // YouTube Player - Always fullscreen
                YouTubePlayerView(videoId: videoId)
                    .edgesIgnoringSafeArea(.all)
                    .onAppear {
                        DispatchQueue.main.asyncAfter(deadline: .now() + 2.5) {
                            isLoading = false
                        }
                    }
                
                // Overlay controls (tap to toggle)
                if showControls && !isLandscape {
                    VStack {
                        Spacer()
                        
                        // Bottom control bar
                        HStack(spacing: 20) {
                            // Live badge
                            HStack(spacing: 6) {
                                Circle()
                                    .fill(Color.red)
                                    .frame(width: 8, height: 8)
                                Text("EN VIVO")
                                    .font(.caption)
                                    .fontWeight(.bold)
                            }
                            .foregroundColor(.white)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(Color.red.opacity(0.8))
                            .cornerRadius(4)
                            
                            Text(liveStream.name)
                                .font(.subheadline)
                                .fontWeight(.semibold)
                                .foregroundColor(.white)
                            
                            Spacer()
                            
                            // Open in YouTube
                            if let watchURL = liveStream.watchURL {
                                Link(destination: watchURL) {
                                    Image(systemName: "arrow.up.right.square")
                                        .font(.title2)
                                        .foregroundColor(.white)
                                }
                            }
                        }
                        .padding()
                        .background(
                            LinearGradient(
                                colors: [.clear, .black.opacity(0.8)],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                    }
                    .transition(.opacity)
                }
                
                // Loading Overlay
                if isLoading {
                    Color.black
                        .edgesIgnoringSafeArea(.all)
                        .overlay(
                            VStack(spacing: 16) {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                    .scaleEffect(1.5)
                                Text("Cargando \(liveStream.name)...")
                                    .font(.subheadline)
                                    .foregroundColor(.gray)
                            }
                        )
                }
            } else {
                // Not live state
                VStack(spacing: 20) {
                    Image(systemName: "video.slash.fill")
                        .font(.system(size: 70))
                        .foregroundColor(.gray.opacity(0.5))
                    
                    Text("Sin transmisión activa")
                        .font(.title2)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                    
                    Text("\(liveStream.name) no está transmitiendo en vivo.")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 40)
                    
                    Button("Volver") { dismiss() }
                        .foregroundColor(.white)
                        .padding(.horizontal, 30)
                        .padding(.vertical, 12)
                        .background(Color.white.opacity(0.15))
                        .cornerRadius(10)
                }
            }
        }
        .onTapGesture {
            withAnimation(.easeInOut(duration: 0.2)) {
                showControls.toggle()
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .navigationBarHidden(isLandscape || !showControls)
        .toolbar {
            ToolbarItem(placement: .principal) {
                if !isLandscape && showControls {
                    Text(liveStream.name)
                        .font(.headline)
                        .foregroundColor(.white)
                }
            }
        }
        .toolbarBackground(.visible, for: .navigationBar)
        .toolbarBackground(Color.black.opacity(0.8), for: .navigationBar)
        .toolbarColorScheme(.dark, for: .navigationBar)
        .statusBarHidden(isLandscape || !showControls)
    }
}

#Preview {
    NavigationStack {
        LivePlayerView(liveStream: LiveStream(
            name: "CNN",
            channelId: "UCupvZG-5ko_eiXAupbDfxWw",
            live: true,
            videoId: "jfKfPfyJRdk",
            title: "CNN News Live - Breaking News Coverage",
            thumbnail: "https://i.ytimg.com/vi/jfKfPfyJRdk/hqdefault.jpg",
            updatedAt: "2024-01-15T10:30:00Z"
        ))
    }
}

#Preview {
    NavigationStack {
        LivePlayerView(liveStream: LiveStream(
            name: "CNN",
            channelId: "UCupvZG-5ko_eiXAupbDfxWw",
            live: true,
            videoId: "jfKfPfyJRdk",
            title: "CNN News Live - Breaking News Coverage",
            thumbnail: "https://i.ytimg.com/vi/jfKfPfyJRdk/hqdefault.jpg",
            updatedAt: "2024-01-15T10:30:00Z"
        ))
    }
}
