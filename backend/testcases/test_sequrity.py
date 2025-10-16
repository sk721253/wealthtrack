# Create test file: backend/test_security.py

from app.utils.security import get_password_hash, verify_password

def test_password():
    password = "MySecurePassword123!"
    
    # Hash the password
    hashed = get_password_hash(password)
    print(f"Original: {password}")
    print(f"Hashed: {hashed}")
    
    # Verify correct password
    is_correct = verify_password(password, hashed)
    print(f"Correct password: {is_correct}")  # Should be True
    
    # Verify wrong password
    is_wrong = verify_password("WrongPassword", hashed)
    print(f"Wrong password: {is_wrong}")  # Should be False

if __name__ == "__main__":
    test_password()