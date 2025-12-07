import Foundation

/// Service for fetching YouTube live streams from the backend
class LiveService {
    static let shared = LiveService()
    private let networkManager = NetworkManager.shared
    
    private init() {}
    
    /// Fetches all YouTube live stream statuses from configured news channels
    /// - Parameter forceRefresh: If true, bypasses backend cache for fresh data
    /// - Returns: LiveStreamsResponse containing all channels and their live status
    func getLiveStreams(forceRefresh: Bool = false) async throws -> LiveStreamsResponse {
        let endpoint = forceRefresh ? "/youtube/lives?force_refresh=true" : "/youtube/lives"
        return try await networkManager.request(
            endpoint: endpoint,
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
