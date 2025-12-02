import SwiftUI

struct FeedView: View {
    @StateObject private var viewModel = FeedViewModel()
    @State private var selectedFilter: FeedFilter = .personalized
    
    enum FeedFilter: String, CaseIterable {
        case personalized = "Para Ti"
        case trending = "Tendencias"
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Filter Picker
                Picker("Feed Type", selection: $selectedFilter) {
                    ForEach(FeedFilter.allCases, id: \.self) { filter in
                        Text(filter.rawValue).tag(filter)
                    }
                }
                .pickerStyle(.segmented)
                .padding()
                
                // Articles List
                if viewModel.isLoading && viewModel.articles.isEmpty {
                    Spacer()
                    ProgressView()
                    Spacer()
                } else if let error = viewModel.errorMessage {
                    Spacer()
                    VStack(spacing: 16) {
                        Image(systemName: "exclamationmark.triangle")
                            .font(.system(size: 50))
                            .foregroundColor(.orange)
                        Text(error)
                            .multilineTextAlignment(.center)
                            .foregroundColor(.secondary)
                        Button("Reintentar") {
                            Task {
                                await viewModel.loadFeed(filter: selectedFilter == .personalized ? .personalized : .trending)
                            }
                        }
                        .buttonStyle(.bordered)
                    }
                    .padding()
                    Spacer()
                } else if viewModel.articles.isEmpty {
                    Spacer()
                    VStack(spacing: 16) {
                        Image(systemName: "newspaper")
                            .font(.system(size: 50))
                            .foregroundColor(.gray)
                        Text("No hay artículos disponibles")
                            .foregroundColor(.secondary)
                    }
                    Spacer()
                } else {
                    ScrollView {
                        LazyVStack(spacing: 16) {
                            ForEach(viewModel.articles) { article in
                                NavigationLink(destination: ArticleDetailView(article: article)) {
                                    ArticleCardView(article: article)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding()
                    }
                    .refreshable {
                        await viewModel.loadFeed(filter: selectedFilter == .personalized ? .personalized : .trending)
                    }
                }
            }
            .navigationTitle("NewsHub")
            .navigationBarTitleDisplayMode(.large)
        }
        .task {
            await viewModel.loadFeed(filter: .personalized)
        }
        .onChange(of: selectedFilter) { _, newValue in
            Task {
                await viewModel.loadFeed(filter: newValue == .personalized ? .personalized : .trending)
            }
        }
    }
}

struct ArticleCardView: View {
    let article: Article
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Image
            if let imageUrl = article.imageUrl, let url = URL(string: imageUrl) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .empty:
                        Rectangle()
                            .fill(Color.gray.opacity(0.2))
                            .frame(height: 200)
                            .overlay(ProgressView())
                    case .success(let image):
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                            .frame(height: 200)
                            .clipped()
                    case .failure:
                        Rectangle()
                            .fill(Color.gray.opacity(0.2))
                            .frame(height: 200)
                            .overlay(
                                Image(systemName: "photo")
                                    .foregroundColor(.gray)
                            )
                    @unknown default:
                        EmptyView()
                    }
                }
                .cornerRadius(12)
            }
            
            // Category and Source
            HStack {
                Text(article.category.uppercased())
                    .font(.caption)
                    .fontWeight(.semibold)
                    .foregroundColor(.blue)
                
                Spacer()
                
                Text(article.sourceName)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            // Title
            Text(article.title)
                .font(.headline)
                .foregroundColor(.primary)
                .lineLimit(3)
            
            // Description
            if let description = article.description {
                Text(description)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            
            // Metadata
            HStack {
                // Sentiment indicator
                HStack(spacing: 4) {
                    Image(systemName: sentimentIcon)
                        .foregroundColor(sentimentColor)
                    Text(article.sentimentLabel)
                        .font(.caption)
                        .foregroundColor(sentimentColor)
                }
                
                Spacer()
                
                // Published date
                Text(formatDate(article.publishedAt))
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
    
    private var sentimentIcon: String {
        switch article.sentimentLabel.lowercased() {
        case "positive": return "arrow.up.circle.fill"
        case "negative": return "arrow.down.circle.fill"
        default: return "minus.circle.fill"
        }
    }
    
    private var sentimentColor: Color {
        switch article.sentimentLabel.lowercased() {
        case "positive": return .green
        case "negative": return .red
        default: return .gray
        }
    }
    
    private func formatDate(_ dateString: String) -> String {
        let formatter = ISO8601DateFormatter()
        if let date = formatter.date(from: dateString) {
            let displayFormatter = RelativeDateTimeFormatter()
            displayFormatter.unitsStyle = .short
            return displayFormatter.localizedString(for: date, relativeTo: Date())
        }
        return dateString
    }
}
