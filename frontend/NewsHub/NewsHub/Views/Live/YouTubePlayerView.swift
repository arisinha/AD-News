import SwiftUI
import WebKit

/// A SwiftUI wrapper for WKWebView to display YouTube videos
/// Uses the full YouTube mobile site instead of embed to bypass embedding restrictions
/// Injects CSS to hide YouTube chrome for a cleaner video-focused experience
struct YouTubePlayerView: UIViewRepresentable {
    let videoId: String
    
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }
    
    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        configuration.allowsInlineMediaPlayback = true
        configuration.mediaTypesRequiringUserActionForPlayback = []
        
        let preferences = WKWebpagePreferences()
        preferences.allowsContentJavaScript = true
        configuration.defaultWebpagePreferences = preferences
        
        // Inject CSS to hide YouTube chrome
        let hideUIScript = WKUserScript(
            source: """
                var style = document.createElement('style');
                style.textContent = `
                    /* Hide header */
                    ytm-mobile-topbar-renderer,
                    header,
                    .mobile-topbar-header-content,
                    .ytm-autonav-bar,
                    #masthead-container,
                    ytm-pivot-bar-renderer,
                    .player-controls-top,
                    
                    /* Hide title/description below video */
                    ytm-slim-video-metadata-section-renderer,
                    .slim-video-metadata-header,
                    ytm-video-description-header-renderer,
                    .video-secondary-info-renderer,
                    
                    /* Hide comments and suggestions */
                    ytm-comments-entry-point-header-renderer,
                    ytm-item-section-renderer,
                    ytm-single-column-watch-next-results-renderer > .rich-grid-renderer,
                    ytm-compact-video-renderer,
                    ytm-rich-item-renderer,
                    
                    /* Hide engagement buttons */
                    ytm-slim-video-action-bar-renderer,
                    
                    /* Hide Open App button */
                    .ytm-autonav-toggle-button-container,
                    c3-toast,
                    
                    /* Hide bottom bar */
                    ytm-pivot-bar-renderer,
                    ytm-app-header-renderer {
                        display: none !important;
                    }
                    
                    /* Make player fullscreen */
                    ytm-player-microformat-renderer,
                    .player-container,
                    .html5-video-player,
                    video {
                        position: fixed !important;
                        top: 0 !important;
                        left: 0 !important;
                        width: 100vw !important;
                        height: 100vh !important;
                        max-height: none !important;
                        object-fit: contain !important;
                        background: #000 !important;
                    }
                    
                    body {
                        background: #000 !important;
                        overflow: hidden !important;
                    }
                    
                    #player {
                        position: fixed !important;
                        top: 0 !important;
                        left: 0 !important;
                        width: 100% !important;
                        height: 100% !important;
                        z-index: 9999 !important;
                    }
                `;
                document.head.appendChild(style);
                
                // Re-apply after dynamic content loads
                setTimeout(function() {
                    document.head.appendChild(style.cloneNode(true));
                }, 1000);
                setTimeout(function() {
                    document.head.appendChild(style.cloneNode(true));
                }, 3000);
            """,
            injectionTime: .atDocumentEnd,
            forMainFrameOnly: false
        )
        configuration.userContentController.addUserScript(hideUIScript)
        
        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.scrollView.isScrollEnabled = false
        webView.scrollView.bounces = false
        webView.backgroundColor = .black
        webView.isOpaque = false
        webView.customUserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        
        context.coordinator.webView = webView
        
        // Load URL only once on creation
        if let url = URL(string: "https://m.youtube.com/watch?v=\(videoId)") {
            let request = URLRequest(url: url)
            webView.load(request)
        }
        
        return webView
    }
    
    func updateUIView(_ webView: WKWebView, context: Context) {
        // Don't reload on rotation - just let it resize naturally
    }
    
    class Coordinator {
        var webView: WKWebView?
    }
}

#Preview {
    YouTubePlayerView(videoId: "jfKfPfyJRdk")
        .frame(height: 300)
}
