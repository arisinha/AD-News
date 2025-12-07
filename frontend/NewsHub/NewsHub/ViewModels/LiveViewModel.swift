import Foundation
import SwiftUI
import Combine

/// ViewModel for managing YouTube live streams state
@MainActor
class LiveViewModel: ObservableObject {
    // MARK: - Published Properties
    
    @Published var liveStreams: [LiveStream] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var lastUpdated: Date?
    
    // MARK: - Computed Properties
    
    /// Returns only channels that are currently live
    var activeStreams: [LiveStream] {
        liveStreams.filter { $0.live }
    }
    
    /// Returns channels that are not currently live
    var offlineChannels: [LiveStream] {
        liveStreams.filter { !$0.live }
    }
    
    /// Number of channels currently live
    var liveCount: Int {
        activeStreams.count
    }
    
    /// Total number of tracked channels
    var totalChannels: Int {
        liveStreams.count
    }
    
    // MARK: - Private Properties
    
    private let liveService = LiveService.shared
    
    // MARK: - Public Methods
    
    /// Loads all live stream statuses from the backend
    /// - Parameter forceRefresh: If true, bypasses backend cache for fresh data
    func loadLiveStreams(forceRefresh: Bool = false) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let response = try await liveService.getLiveStreams(forceRefresh: forceRefresh)
            liveStreams = response.channels
            lastUpdated = Date()
        } catch let error as NetworkError {
            errorMessage = error.localizedDescription
        } catch {
            errorMessage = "Error al cargar transmisiones en vivo: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
    
    /// Refreshes the live stream data (forces cache bypass)
    func refresh() async {
        await loadLiveStreams(forceRefresh: true)
    }
    
    /// Returns a formatted string for the last update time
    func formatLastUpdated() -> String {
        guard let lastUpdated = lastUpdated else {
            return "Nunca actualizado"
        }
        
        let formatter = RelativeDateTimeFormatter()
        formatter.unitsStyle = .short
        formatter.locale = Locale(identifier: "es_ES")
        return "Actualizado \(formatter.localizedString(for: lastUpdated, relativeTo: Date()))"
    }
    
    /// Checks if a specific channel is live
    func isChannelLive(_ channelId: String) -> Bool {
        liveStreams.first { $0.channelId == channelId }?.live ?? false
    }
}
