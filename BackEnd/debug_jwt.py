"""
Debug JWT token generation and validation
"""
from app import create_app, db
from app.config import Config
from flask_jwt_extended import create_access_token
import jwt as pyjwt

app = create_app(Config)

with app.app_context():
    print("="*60)
    print("JWT DEBUG - Token Generation & Validation")
    print("="*60)

    # Check config
    print(f"\nJWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}")
    print(f"JWT_ACCESS_TOKEN_EXPIRES: {app.config['JWT_ACCESS_TOKEN_EXPIRES']} seconds")

    # Generate test token
    print("\n" + "="*60)
    print("Generating test token for user_id=3 (customer)...")
    print("="*60)

    test_user_id = 3
    token = create_access_token(identity=str(test_user_id))  # Must be string

    print(f"\nGenerated Token (first 100 chars):")
    print(token[:100] + "...")

    # Decode token to see payload
    try:
        decoded = pyjwt.decode(
            token,
            app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        print(f"\nDecoded Token Payload:")
        print(f"  - sub (user_id): {decoded.get('sub')}")
        print(f"  - exp (expires): {decoded.get('exp')}")
        print(f"  - iat (issued at): {decoded.get('iat')}")
        print(f"  - type: {decoded.get('type')}")

        print("\n✓ Token is VALID and can be decoded!")

    except Exception as e:
        print(f"\n✗ Error decoding token: {e}")

    # Test with frontend-like request
    print("\n" + "="*60)
    print("Testing token with actual Flask request...")
    print("="*60)

    with app.test_client() as client:
        # Test protected endpoint
        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = client.get('/api/robots?for_rental=true', headers=headers)
        print(f"\nGET /api/robots?for_rental=true")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json
            print(f"✓ SUCCESS! Found {len(data.get('robots', []))} robots")
            for robot in data.get('robots', []):
                print(f"  - {robot.get('robot_name')} (ID: {robot.get('robot_id')})")
        else:
            print(f"✗ Error: {response.json}")

        # Test certification progress
        response = client.get('/api/certification/progress', headers=headers)
        print(f"\nGET /api/certification/progress")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json
            print(f"✓ SUCCESS! Progress: {data.get('overall_progress')}%")
        else:
            print(f"✗ Error: {response.json}")

        # Test bookings
        response = client.get('/api/bookings?status=rental', headers=headers)
        print(f"\nGET /api/bookings?status=rental")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json
            print(f"✓ SUCCESS! Found {len(data.get('bookings', []))} bookings")
        else:
            print(f"✗ Error: {response.json}")

    print("\n" + "="*60)
    print("DEBUG COMPLETE")
    print("="*60)
