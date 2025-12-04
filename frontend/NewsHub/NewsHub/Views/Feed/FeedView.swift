import SwiftUI

struct FeedView: View {
    @StateObject private var viewModel = FeedViewModel()
    @State private var selectedFilter: FeedFilter = .trending
    
    enum FeedFilter: String, CaseIterable {
        case trending = "Tendencias"
        case categories = "Categorías"
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
                
                // Category chips (only show when Categories tab is selected)
                if selectedFilter == .categories {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 10) {
                            ForEach(viewModel.categories, id: \.self) { category in
                                CategoryChipView(
                                    title: category,
                                    isSelected: viewModel.selectedCategory == category
                                ) {
                                    viewModel.selectCategory(category)
                                }
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.bottom, 8)
                }
                
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
                                await loadCurrentFeed()
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
                        await loadCurrentFeed()
                    }
                }
            }
            .navigationTitle("AD News")
            .navigationBarTitleDisplayMode(.large)
        }
        .task {
            await viewModel.loadFeed(filter: .trending)
        }
        .onChange(of: selectedFilter) { _, newValue in
            Task {
                if newValue == .trending {
                    await viewModel.loadFeed(filter: .trending)
                } else {
                    await viewModel.loadFeed(filter: .category(viewModel.selectedCategory))
                }
            }
        }
    }
    
    private func loadCurrentFeed() async {
        if selectedFilter == .trending {
            await viewModel.loadFeed(filter: .trending)
        } else {
            await viewModel.loadFeed(filter: .category(viewModel.selectedCategory))
        }
    }
}

// Category chip component
struct CategoryChipView: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .fontWeight(isSelected ? .semibold : .regular)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(isSelected ? Color.blue : Color.gray.opacity(0.15))
                .foregroundColor(isSelected ? .white : .primary)
                .cornerRadius(20)
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
