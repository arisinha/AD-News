# Endpoint Fixes Summary

## Changes Made

### 1. Backend Configuration
**File:** `backend/app/core/config.py`
- Changed `API_V1_STR` from `/v1` to `/api/v1`
- This ensures all endpoints are now prefixed with `/api/v1` instead of just `/v1`

### 2. Swift AuthService
**File:** `frontend/NewsHub/NewsHub/Services/AuthService.swift`
- Changed `/users/me` to `/user/me` to match backend router configuration

### 3. Articles Endpoints
**File:** `backend/app/api/v1/endpoints/articles.py`
- Updated `GET /articles/` to use `page` and `size` parameters instead of `skip` and `limit`
- Added `GET /articles/search` endpoint with `q`, `page`, and `size` parameters

### 4. Feed Endpoints
**File:** `backend/app/api/v1/endpoints/feed.py`
- Updated all endpoints to use `page` and `size` parameters
- Added `GET /feed/personalized` endpoint
- Added `GET /feed/trending` endpoint
- Updated `GET /feed/category/{category}` to use `page` and `size`

## Complete Endpoint Mapping

### Authentication Endpoints
| Swift Call | Backend Endpoint | Method | Auth Required |
|-----------|------------------|--------|---------------|
| `/auth/login` | `/api/v1/auth/login` | POST | No |
| `/auth/register` | `/api/v1/auth/register` | POST | No |

### User Endpoints
| Swift Call | Backend Endpoint | Method | Auth Required |
|-----------|------------------|--------|---------------|
| `/user/me` | `/api/v1/user/me` | GET | Yes |

### Article Endpoints
| Swift Call | Backend Endpoint | Method | Auth Required |
|-----------|------------------|--------|---------------|
| `/articles/?page=X&size=Y` | `/api/v1/articles/?page=X&size=Y` | GET | No |
| `/articles/{id}` | `/api/v1/articles/{id}` | GET | No |
| `/articles/search?q=X&page=Y&size=Z` | `/api/v1/articles/search?q=X&page=Y&size=Z` | GET | No |

### Feed Endpoints
| Swift Call | Backend Endpoint | Method | Auth Required |
|-----------|------------------|--------|---------------|
| `/feed/personalized?page=X&size=Y` | `/api/v1/feed/personalized?page=X&size=Y` | GET | Yes |
| `/feed/trending?page=X&size=Y` | `/api/v1/feed/trending?page=X&size=Y` | GET | No |
| `/feed/category/{cat}?page=X&size=Y` | `/api/v1/feed/category/{cat}?page=X&size=Y` | GET | Yes |

## Next Steps

1. **Restart the backend server** for changes to take effect:
   ```bash
   cd "backend"
   uvicorn app.main:app --reload
   ```

2. **Test the endpoints** using the Swift app or a tool like Postman

3. **Verify authentication** works correctly with the login endpoint

## Notes

- All endpoints now use consistent `page` and `size` pagination parameters
- Page numbers start at 1 (not 0)
- The conversion formula is: `skip = (page - 1) * size`
- Redis connection errors are non-critical and won't affect functionality
- The `/feed/trending` endpoint currently returns the same data as personalized feed but can be enhanced with popularity metrics later
