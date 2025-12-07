import SwiftUI

/// Main view displaying list of YouTube live streams from news channels
struct LiveListView: View {
    @StateObject private var viewModel = LiveViewModel()
    
    var body: some View {
        NavigationStack {
            ZStack {
                // Background gradient
                LinearGradient(
                    gradient: Gradient(colors: [
                        Color(red: 0.1, green: 0.1, blue: 0.15),
                        Color(red: 0.05, green: 0.05, blue: 0.1)
                    ]),
                    startPoint: .top,
                    endPoint: .bottom
                )
                .edgesIgnoringSafeArea(.all)
                
                if viewModel.isLoading && viewModel.liveStreams.isEmpty {
                    // Loading State
                    VStack(spacing: 20) {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            .scaleEffect(1.5)
                        Text("Cargando canales...")
                            .font(.subheadline)
                            .foregroundColor(.gray)
                    }
                } else if let error = viewModel.errorMessage {
                    // Error State
                    VStack(spacing: 20) {
                        Image(systemName: "wifi.exclamationmark")
                            .font(.system(size: 60))
                            .foregroundColor(.orange)
                        Text("Error de conexión")
                            .font(.headline)
                            .foregroundColor(.white)
                        Text(error)
                            .font(.subheadline)
                            .foregroundColor(.gray)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal)
                        Button {
                            Task {
                                await viewModel.refresh()
                            }
                        } label: {
                            HStack {
                                Image(systemName: "arrow.clockwise")
                                Text("Reintentar")
                            }
                            .foregroundColor(.white)
                            .padding(.horizontal, 24)
                            .padding(.vertical, 12)
                            .background(Color.blue)
                            .cornerRadius(10)
                        }
                    }
                    .padding()
                } else if viewModel.liveStreams.isEmpty {
                    // Empty State
                    VStack(spacing: 20) {
                        Image(systemName: "tv.slash")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        Text("No hay canales configurados")
                            .font(.headline)
                            .foregroundColor(.white)
                        Text("Configura canales de noticias para ver transmisiones en vivo.")
                            .font(.subheadline)
                            .foregroundColor(.gray)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal)
                    }
                } else {
                    // Content
                    ScrollView {
                        VStack(spacing: 16) {
                            // Stats Header
                            HStack {
                                VStack(alignment: .leading, spacing: 4) {
                                    HStack(spacing: 8) {
                                        Circle()
                                            .fill(Color.red)
                                            .frame(width: 10, height: 10)
                                        Text("\(viewModel.liveCount) en vivo")
                                            .font(.headline)
                                            .foregroundColor(.white)
                                    }
                                    Text(viewModel.formatLastUpdated())
                                        .font(.caption)
                                        .foregroundColor(.gray)
                                }
                                
                                Spacer()
                                
                                Text("\(viewModel.totalChannels) canales")
                                    .font(.subheadline)
                                    .foregroundColor(.gray)
                            }
                            .padding(.horizontal)
                            .padding(.top, 8)
                            
                            // Live Streams Section
                            if !viewModel.activeStreams.isEmpty {
                                VStack(alignment: .leading, spacing: 12) {
                                    Text("Transmitiendo ahora")
                                        .font(.title3)
                                        .fontWeight(.bold)
                                        .foregroundColor(.white)
                                        .padding(.horizontal)
                                    
                                    ForEach(viewModel.activeStreams) { stream in
                                        NavigationLink(destination: LivePlayerView(liveStream: stream)) {
                                            LiveStreamCard(stream: stream, isLive: true)
                                        }
                                        .buttonStyle(.plain)
                                    }
                                }
                            }
                            
                            // Offline Channels Section
                            if !viewModel.offlineChannels.isEmpty {
                                VStack(alignment: .leading, spacing: 12) {
                                    Text("Canales disponibles")
                                        .font(.title3)
                                        .fontWeight(.bold)
                                        .foregroundColor(.white)
                                        .padding(.horizontal)
                                        .padding(.top, 8)
                                    
                                    ForEach(viewModel.offlineChannels) { stream in
                                        LiveStreamCard(stream: stream, isLive: false)
                                    }
                                }
                            }
                        }
                        .padding(.bottom, 20)
                    }
                    .refreshable {
                        await viewModel.refresh()
                    }
                }
            }
            .safeAreaInset(edge: .top) {
                // Fixed header that always shows
                VStack(alignment: .leading, spacing: 0) {
                    Text("En Vivo")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                        .padding(.horizontal)
                        .padding(.top, 8)
                        .padding(.bottom, 12)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(
                    Color(red: 0.1, green: 0.1, blue: 0.15)
                        .ignoresSafeArea(edges: .top)
                )
            }
            .navigationBarHidden(true)
        }
        .task {
            await viewModel.loadLiveStreams()
        }
    }
}

/// Card component for displaying a live stream
struct LiveStreamCard: View {
    let stream: LiveStream
    let isLive: Bool
    
    var body: some View {
        HStack(spacing: 12) {
            // Thumbnail
            AsyncImage(url: URL(string: stream.thumbnail ?? "")) { phase in
                switch phase {
                case .empty:
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.gray.opacity(0.3))
                        .frame(width: 120, height: 68)
                        .overlay(
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        )
                case .success(let image):
                    image
                        .resizable()
                        .aspectRatio(16/9, contentMode: .fill)
                        .frame(width: 120, height: 68)
                        .clipped()
                        .cornerRadius(8)
                        .overlay(
                            // Live badge overlay
                            Group {
                                if isLive {
                                    VStack {
                                        HStack {
                                            Spacer()
                                            HStack(spacing: 4) {
                                                Circle()
                                                    .fill(Color.white)
                                                    .frame(width: 6, height: 6)
                                                Text("EN VIVO")
                                                    .font(.system(size: 8, weight: .bold))
                                                    .foregroundColor(.white)
                                            }
                                            .padding(.horizontal, 6)
                                            .padding(.vertical, 3)
                                            .background(Color.red)
                                            .cornerRadius(4)
                                            .padding(4)
                                        }
                                        Spacer()
                                    }
                                }
                            }
                        )
                case .failure:
                    RoundedRectangle(cornerRadius: 8)
                        .fill(Color.gray.opacity(0.3))
                        .frame(width: 120, height: 68)
                        .overlay(
                            Image(systemName: "photo")
                                .foregroundColor(.gray)
                        )
                @unknown default:
                    EmptyView()
                }
            }
            
            // Info
            VStack(alignment: .leading, spacing: 6) {
                Text(stream.name)
                    .font(.headline)
                    .foregroundColor(.white)
                    .lineLimit(1)
                
                if let title = stream.title, isLive {
                    Text(title)
                        .font(.caption)
                        .foregroundColor(.gray)
                        .lineLimit(2)
                } else if !isLive {
                    Text("Sin transmisión activa")
                        .font(.caption)
                        .foregroundColor(.gray.opacity(0.7))
                        .italic()
                }
                
                // Status indicator
                HStack(spacing: 4) {
                    Circle()
                        .fill(isLive ? Color.red : Color.gray.opacity(0.5))
                        .frame(width: 6, height: 6)
                    Text(isLive ? "Transmitiendo" : "Offline")
                        .font(.caption2)
                        .foregroundColor(isLive ? .red : .gray)
                }
            }
            
            Spacer()
            
            // Play button for live streams
            if isLive {
                Image(systemName: "play.circle.fill")
                    .font(.system(size: 30))
                    .foregroundColor(.red)
            }
        }
        .padding(12)
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color.white.opacity(0.05))
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(isLive ? Color.red.opacity(0.3) : Color.white.opacity(0.1), lineWidth: 1)
                )
        )
        .padding(.horizontal)
    }
}

#Preview {
    LiveListView()
}
