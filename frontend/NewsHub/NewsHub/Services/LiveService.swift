import Foundation

/// Service for fetching YouTube live streams from the backend
class LiveService {
    static let shared = LiveService()
    private let networkManager = NetworkManager.shared
    
    private init() {}
    
    /// Fetches all YouTube live stream statuses from configured news channels
    /// - Returns: LiveStreamsResponse containing all channels and their live status
    func getLiveStreams() async throws -> LiveStreamsResponse {
        return try await networkManager.request(
            endpoint: "/youtube/lives",
            method: "GET",
            requiresAuth: false
        )
    }
    
    /// Fetches live status for a specific channel
    /// - Parameter channelId: The YouTube channel ID
    /// - Returns: LiveStream object with the channel's current status
    func getChannelLiveStatus(channelId: String) async throws -> LiveStream {
        return try await networkManager.request(
            endpoint: "/youtube/lives/\(channelId)",
            method: "GET",
            requiresAuth: false
        )
    }
}
