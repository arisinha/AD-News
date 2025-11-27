import requests
import sys

BASE_URL = "http://localhost:8000/v1"

def verify_favorites():
    # 1. Register a new user
    email = "test_favorite_user@example.com"
    username = "test_favorite_user"
    password = "password123"
    
    print(f"Registering user {email}...")
    register_data = {
        "email": email,
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 400 and "exists" in response.text:
        print("User already exists, proceeding to login.")
    elif response.status_code != 200:
        print(f"Registration failed: {response.text}")
        sys.exit(1)
    else:
        print("User registered successfully.")

    # 2. Login
    print("Logging in...")
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/auth/login/json", json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        sys.exit(1)
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Logged in successfully.")

    # 3. Create Favorite
    print("Creating favorite...")
    favorite_data = {
        "article_id": "test_article_123",
        "collection_name": "Read Later"
    }
    response = requests.post(f"{BASE_URL}/user/favorites/", json=favorite_data, headers=headers)
    if response.status_code != 200:
        print(f"Create favorite failed: {response.text}")
        sys.exit(1)
    
    favorite = response.json()
    favorite_id = favorite["id"]
    print(f"Favorite created: {favorite_id}")

    # 4. List Favorites
    print("Listing favorites...")
    response = requests.get(f"{BASE_URL}/user/favorites/", headers=headers)
    if response.status_code != 200:
        print(f"List favorites failed: {response.text}")
        sys.exit(1)
    
    favorites = response.json()
    print(f"Found {len(favorites)} favorites.")
    found = False
    for fav in favorites:
        if fav["id"] == favorite_id:
            found = True
            break
    
    if not found:
        print("Created favorite not found in list!")
        sys.exit(1)
    print("Favorite verified in list.")

    # 5. Delete Favorite
    print(f"Deleting favorite {favorite_id}...")
    response = requests.delete(f"{BASE_URL}/user/favorites/{favorite_id}", headers=headers)
    if response.status_code != 200:
        print(f"Delete favorite failed: {response.text}")
        sys.exit(1)
    
    print("Favorite deleted successfully.")
    
    # Verify deletion
    response = requests.get(f"{BASE_URL}/user/favorites/", headers=headers)
    favorites = response.json()
    for fav in favorites:
        if fav["id"] == favorite_id:
            print("Favorite still exists after deletion!")
            sys.exit(1)
            
    print("Verification passed!")

if __name__ == "__main__":
    verify_favorites()
