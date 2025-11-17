"""
Test endpoints to verify JWT authentication works correctly
"""
import requests
import json

BASE_URL = "http://localhost:5010"

def test_login_and_endpoints():
    print("="*60)
    print("TESTING BACKEND ENDPOINTS")
    print("="*60)

    # Test 1: Login
    print("\n1. Testing login...")
    login_data = {
        "email": "customer@sealen.com",
        "password": "customer123"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"   ✓ Login successful")
            print(f"   Token: {token[:50]}..." if token else "   ✗ No token received")

            if not token:
                print("\n   ERROR: No access token in response")
                return

            # Test 2: Get robots for rental
            print("\n2. Testing GET /api/robots?for_rental=true...")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/api/robots?for_rental=true", headers=headers)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                robots = response.json().get('robots', [])
                print(f"   ✓ Found {len(robots)} robots available for rental")
                for robot in robots:
                    print(f"     - {robot.get('robot_name')} (ID: {robot.get('robot_id')})")
            else:
                print(f"   ✗ Error: {response.text}")

            # Test 3: Get bookings
            print("\n3. Testing GET /api/bookings?status=rental...")
            response = requests.get(f"{BASE_URL}/api/bookings?status=rental", headers=headers)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                bookings = response.json().get('bookings', [])
                print(f"   ✓ Found {len(bookings)} rental bookings")
            else:
                print(f"   ✗ Error: {response.text}")

            # Test 4: Get certification progress
            print("\n4. Testing GET /api/certification/progress...")
            response = requests.get(f"{BASE_URL}/api/certification/progress", headers=headers)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   ✓ Progress: {data.get('overall_progress')}%")
                print(f"   ✓ Completed: {data.get('completed_modules')}/{data.get('total_modules')} modules")
            else:
                print(f"   ✗ Error: {response.text}")

        else:
            print(f"   ✗ Login failed: {response.text}")

    except requests.exceptions.ConnectionError:
        print("   ✗ ERROR: Cannot connect to server")
        print("   Make sure the Flask server is running on port 5010")
    except Exception as e:
        print(f"   ✗ ERROR: {str(e)}")

    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_login_and_endpoints()
