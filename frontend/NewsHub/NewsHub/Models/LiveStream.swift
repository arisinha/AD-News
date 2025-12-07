import Foundation

/// Represents a YouTube live stream from a news channel
struct LiveStream: Codable, Identifiable {
    let name: String
    let channelId: String
    let live: Bool
    let videoId: String?
    let title: String?
    let thumbnail: String?
    let updatedAt: String
    
    /// Use channelId as the unique identifier
    var id: String { channelId }
    
    /// Returns the YouTube embed URL for the live stream
    var embedURL: URL? {
        guard let videoId = videoId else { return nil }
        return URL(string: "https://www.youtube.com/embed/\(videoId)?autoplay=1&playsinline=1")
    }
    
    /// Returns the YouTube watch URL for the live stream
    var watchURL: URL? {
        guard let videoId = videoId else { return nil }
        return URL(string: "https://www.youtube.com/watch?v=\(videoId)")
    }
}

/// Response from the /youtube/lives endpoint
struct LiveStreamsResponse: Codable {
    let channels: [LiveStream]
    let total: Int
    let liveCount: Int
    let timestamp: String
}
