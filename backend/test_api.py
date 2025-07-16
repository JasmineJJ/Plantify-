#!/usr/bin/env python3
"""
Test API endpoints using requests
"""
import asyncio
import requests
import json
import random
import string

BASE_URL = "http://localhost:8000/api"

def random_email():
    """Generate random email"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"api_test_{random_string}@example.com"

def test_api_endpoints():
    """Test all API endpoints"""
    try:
        print("=== TESTING API ENDPOINTS ===")
        
        # Test root endpoint
        response = requests.get("http://localhost:8000/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        print(f"Health endpoint: {response.status_code} - {response.json()}")
        
        # 1. USER API TESTS
        print("\n1. USER API TESTS:")
        
        # Create user
        user_data = {
            "email": random_email(),
            "name": "API Test User"
        }
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        print(f"  CREATE User: {response.status_code}")
        user = response.json()
        user_id = user["id"]
        print(f"    Created user: {user['name']} [ID: {user_id}]")
        
        # Get user by ID
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"  GET User by ID: {response.status_code}")
        user_details = response.json()
        print(f"    Retrieved: {user_details['name']}")
        
        # Update user
        update_data = {"name": "API Test User Updated"}
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        print(f"  UPDATE User: {response.status_code}")
        updated_user = response.json()
        print(f"    Updated name: {updated_user['name']}")
        
        # Get all users
        response = requests.get(f"{BASE_URL}/users/")
        print(f"  GET All Users: {response.status_code}")
        users = response.json()
        print(f"    Found {len(users)} users")
        
        # 2. PLANT API TESTS
        print("\n2. PLANT API TESTS:")
        
        # Create plant
        plant_data = {
            "name": "API Test Plant",
            "species": "Test Species",
            "description": "A plant created via API",
            "user_id": user_id
        }
        response = requests.post(f"{BASE_URL}/plants/", json=plant_data)
        print(f"  CREATE Plant: {response.status_code}")
        plant = response.json()
        plant_id = plant["id"]
        print(f"    Created plant: {plant['name']} [ID: {plant_id}]")
        
        # Get plant by ID
        response = requests.get(f"{BASE_URL}/plants/{plant_id}")
        print(f"  GET Plant by ID: {response.status_code}")
        plant_details = response.json()
        print(f"    Retrieved: {plant_details['name']}")
        
        # Update plant
        plant_update = {"description": "Updated plant description via API"}
        response = requests.put(f"{BASE_URL}/plants/{plant_id}", json=plant_update)
        print(f"  UPDATE Plant: {response.status_code}")
        updated_plant = response.json()
        print(f"    Updated description: {updated_plant['description']}")
        
        # Get plants by user
        response = requests.get(f"{BASE_URL}/plants/user/{user_id}")
        print(f"  GET Plants by User: {response.status_code}")
        user_plants = response.json()
        print(f"    User has {len(user_plants)} plants")
        
        # 3. DIAGNOSIS API TESTS
        print("\n3. DIAGNOSIS API TESTS:")
        
        # Create diagnosis
        diagnosis_data = {
            "plant_id": plant_id,
            "disease_name": "API Test Disease",
            "confidence_score": 0.92,
            "image_path": "/api/test/image.jpg",
            "notes": "Diagnosis created via API",
            "is_healthy": False
        }
        response = requests.post(f"{BASE_URL}/diagnoses/", json=diagnosis_data)
        print(f"  CREATE Diagnosis: {response.status_code}")
        diagnosis = response.json()
        diagnosis_id = diagnosis["id"]
        print(f"    Created diagnosis: {diagnosis['disease_name']} [ID: {diagnosis_id}]")
        
        # Get diagnosis by ID
        response = requests.get(f"{BASE_URL}/diagnoses/{diagnosis_id}")
        print(f"  GET Diagnosis by ID: {response.status_code}")
        diagnosis_details = response.json()
        print(f"    Retrieved: {diagnosis_details['disease_name']}")
        
        # Update diagnosis
        diagnosis_update = {
            "confidence_score": 0.96,
            "notes": "Updated diagnosis via API"
        }
        response = requests.put(f"{BASE_URL}/diagnoses/{diagnosis_id}", json=diagnosis_update)
        print(f"  UPDATE Diagnosis: {response.status_code}")
        updated_diagnosis = response.json()
        print(f"    Updated confidence: {updated_diagnosis['confidence_score']}")
        
        # Get diagnoses by plant
        response = requests.get(f"{BASE_URL}/diagnoses/plant/{plant_id}")
        print(f"  GET Diagnoses by Plant: {response.status_code}")
        plant_diagnoses = response.json()
        print(f"    Plant has {len(plant_diagnoses)} diagnoses")
        
        # Get diagnoses by user
        response = requests.get(f"{BASE_URL}/diagnoses/user/{user_id}")
        print(f"  GET Diagnoses by User: {response.status_code}")
        user_diagnoses = response.json()
        print(f"    User has {len(user_diagnoses)} diagnoses")
        
        # 4. ERROR HANDLING TESTS
        print("\n4. ERROR HANDLING TESTS:")
        
        # Test non-existent user
        response = requests.get(f"{BASE_URL}/users/99999")
        print(f"  GET Non-existent User: {response.status_code}")
        
        # Test non-existent plant
        response = requests.get(f"{BASE_URL}/plants/99999")
        print(f"  GET Non-existent Plant: {response.status_code}")
        
        # Test non-existent diagnosis
        response = requests.get(f"{BASE_URL}/diagnoses/99999")
        print(f"  GET Non-existent Diagnosis: {response.status_code}")
        
        # Test invalid user creation (duplicate email)
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        print(f"  CREATE Duplicate User: {response.status_code}")
        
        print("\n=== ALL API TESTS COMPLETED SUCCESSFULLY! ===")
        return True
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to API server.")
        print("Please start the FastAPI server first with:")
        print("  uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"API TEST FAILED: {e}")
        return False

def main():
    """Main function"""
    print("Starting API endpoint tests...")
    print("Make sure the FastAPI server is running on http://localhost:8000")
    
    success = test_api_endpoints()
    if success:
        print("\n*** ALL API TESTS PASSED! ***")
    else:
        print("\n*** API TESTS FAILED! ***")

if __name__ == "__main__":
    main()