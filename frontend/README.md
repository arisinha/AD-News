# NewsHub iOS Frontend

## Overview
NewsHub is an iOS application for personalized news aggregation with AI-powered summaries and sentiment analysis.

## Recent Fixes

### ✅ Services Implementation
- **NetworkManager**: Complete HTTP client with error handling, authentication, and JSON encoding/decoding
- **AuthService**: User authentication (login, register, logout) with token management
- **ArticleService**: Article fetching and search functionality
- **FeedService**: Personalized and trending feed support

### ✅ Views Implementation
- **FeedView**: Main feed with personalized/trending toggle, article cards, pull-to-refresh
- **SearchView**: Search functionality with debouncing and result display
- **FavoritesView**: Saved articles management
- **ArticleDetailView**: Full article view with AI summaries, key points, and sentiment

### ✅ Features
- ✨ Beautiful UI with gradient backgrounds and modern design
- 🔐 Complete authentication flow (login/register)
- 📰 Personalized and trending news feeds
- 🔍 Search functionality
- ⭐ Favorites/bookmarks support
- 🤖 AI-generated summaries and key points
- 📊 Sentiment analysis indicators
- 🖼️ Async image loading
- ♻️ Pull-to-refresh
- 🎨 Custom article cards with metadata

## Configuration

### Backend URL
Update the backend URL in `Utils/AppConfig.swift`:

```swift
static let baseURL = "http://localhost:8000/api/v1"  // For local development
// or
static let baseURL = "https://your-backend.com/api/v1"  // For production
```

### App Settings
You can also configure:
- `defaultPageSize`: Number of articles per page (default: 20)
- `maxCachedArticles`: Maximum cached articles (default: 100)
- `debugMode`: Enable debug logging (default: true)

## Project Structure

```
NewsHub/
├── Models/
│   ├── User.swift              # User and preferences models
│   ├── Article.swift           # Article model
│   └── AuthResponse.swift      # Auth request/response models
├── Services/
│   ├── NetworkManager.swift    # HTTP client
│   ├── AuthService.swift       # Authentication service
│   ├── ArticleService.swift    # Article fetching
│   └── FeedService.swift       # Feed management
├── ViewModels/
│   ├── AuthViewModel.swift     # Auth state management
│   ├── FeedViewModel.swift     # Feed state management
│   └── ArticleViewModel.swift  # Article state management
├── Views/
│   ├── Auth/
│   │   ├── LoginView.swift     # Login screen
│   │   └── RegisterView.swift  # Registration screen
│   ├── Feed/
│   │   ├── FeedView.swift      # Main feed
│   │   ├── SearchView.swift    # Search screen
│   │   └── FavoritesView.swift # Saved articles
│   ├── Article/
│   │   └── ArticleDetailView.swift  # Article details
│   ├── Profile/
│   │   └── ProfileView.swift   # User profile
│   └── MainTabView.swift       # Tab navigation
├── Utils/
│   └── AppConfig.swift         # App configuration
├── ContentView.swift           # Root view
└── NewsHubApp.swift           # App entry point
```

## Running the App

### Prerequisites
1. Xcode 14.0 or later
2. iOS 16.0 or later
3. Backend server running (see backend README)

### Steps
1. Open `NewsHub.xcodeproj` in Xcode
2. Update the backend URL in `Utils/AppConfig.swift`
3. Select a simulator or device
4. Press `Cmd + R` to build and run

### Testing with Backend
Make sure your backend is running:
```bash
cd backend
uvicorn app.main:app --reload
```

The app will connect to the backend at the URL specified in `AppConfig.swift`.

## API Integration

### Authentication
- **Login**: `POST /auth/login`
- **Register**: `POST /auth/register`
- **Get User**: `GET /users/me`

### Articles
- **Get Articles**: `GET /articles/`
- **Search**: `GET /articles/search?q={query}`
- **Get by ID**: `GET /articles/{id}`

### Feed
- **Personalized**: `GET /feed/personalized`
- **Trending**: `GET /feed/trending`
- **By Category**: `GET /feed/category/{category}`

### Favorites
- **List**: `GET /favorites/`
- **Add**: `POST /favorites/{article_id}`
- **Remove**: `DELETE /favorites/{article_id}`

## Features in Detail

### Authentication
- Secure token-based authentication
- Automatic token storage in UserDefaults
- Token injection in API requests
- Auto-logout on 401 responses

### Feed System
- Toggle between personalized and trending feeds
- Category filtering
- Infinite scroll support (ready for pagination)
- Pull-to-refresh

### Article Cards
- Article image with fallback
- Category badge
- Source name
- Title and description
- Sentiment indicator (positive/negative/neutral)
- Relative timestamps

### Article Detail
- Full article content
- AI-generated summary (if available)
- Key points extraction
- Sentiment analysis
- Link to original article
- Bookmark functionality

### Search
- Real-time search with debouncing
- Search by title, description, or content
- Same article card UI as feed

### Favorites
- Save articles for later
- Same browsing experience as feed
- Pull-to-refresh

## Troubleshooting

### Connection Issues
- Verify backend is running
- Check `AppConfig.baseURL` matches your backend
- For iOS Simulator with localhost, use `http://localhost:8000`
- For physical device, use your computer's IP address

### Build Errors
- Clean build folder: `Cmd + Shift + K`
- Delete derived data
- Restart Xcode

### Authentication Issues
- Clear app data (delete and reinstall)
- Check backend logs for errors
- Verify API endpoints are correct

## Next Steps

### Potential Enhancements
- [ ] Implement favorites add/remove functionality
- [ ] Add share functionality
- [ ] Implement pagination for infinite scroll
- [ ] Add offline support with local caching
- [ ] Push notifications for breaking news
- [ ] Dark mode support
- [ ] Preferences customization UI
- [ ] Article reading history
- [ ] Social sharing
- [ ] Accessibility improvements

## Support
For issues or questions, please check the backend documentation or create an issue in the repository.
