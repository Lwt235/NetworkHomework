#!/usr/bin/env python3
"""Simple test to verify backend functionality"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Device

def test_backend():
    """Test basic backend functionality"""
    print("Testing Network Monitoring Backend")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        # Check database
        print("\n1. Testing database connection...")
        try:
            db.create_all()
            print("✓ Database tables created successfully")
        except Exception as e:
            print(f"✗ Database error: {e}")
            return False
        
        # Test user creation
        print("\n2. Testing user model...")
        try:
            # Clean up test user if exists
            User.query.filter_by(username='testuser').delete()
            db.session.commit()
            
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpass123')
            db.session.add(user)
            db.session.commit()
            print(f"✓ User created: {user.username}")
            
            # Test password verification
            assert user.check_password('testpass123'), "Password check failed"
            print("✓ Password verification works")
            
        except Exception as e:
            print(f"✗ User model error: {e}")
            return False
        
        # Test device creation
        print("\n3. Testing device model...")
        try:
            device = Device(
                name='Test Router',
                ip_address='192.168.1.1',
                device_type='router',
                user_id=user.id
            )
            db.session.add(device)
            db.session.commit()
            print(f"✓ Device created: {device.name}")
        except Exception as e:
            print(f"✗ Device model error: {e}")
            return False
        
        # Test routes
        print("\n4. Testing API routes...")
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            assert response.status_code == 200, "Health check failed"
            print("✓ Health check endpoint works")
            
            # Test registration (user already exists)
            response = client.post('/api/auth/login', json={
                'username': 'testuser',
                'password': 'testpass123'
            })
            assert response.status_code == 200, "Login failed"
            data = response.get_json()
            token = data.get('access_token')
            print("✓ Login endpoint works")
            
            # Test authenticated endpoint
            headers = {'Authorization': f'Bearer {token}'}
            response = client.get('/api/devices', headers=headers)
            if response.status_code != 200:
                print(f"✗ Get devices failed with status {response.status_code}: {response.get_json()}")
            assert response.status_code == 200, "Get devices failed"
            devices_data = response.get_json()
            assert len(devices_data['devices']) > 0, "No devices returned"
            print(f"✓ Devices endpoint works (found {len(devices_data['devices'])} device(s))")
            
            # Test monitoring endpoints
            response = client.get('/api/monitoring/traffic', headers=headers)
            assert response.status_code == 200, "Get traffic failed"
            print("✓ Traffic monitoring endpoint works")
            
            response = client.get('/api/monitoring/system', headers=headers)
            assert response.status_code == 200, "Get system stats failed"
            print("✓ System stats endpoint works")
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    return True

if __name__ == '__main__':
    try:
        success = test_backend()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
