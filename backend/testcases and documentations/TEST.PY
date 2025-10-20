import bcrypt

BCRYPT_MAX_LEN = 72  # bcrypt limit in bytes

# Example long password (> 72 bytes)
password = b"A"*100  # 100 bytes of letter "A"

# Check length before hashing
if len(password) > BCRYPT_MAX_LEN:
    print(f"Warning: password is longer than {BCRYPT_MAX_LEN} bytes, truncating.")
    password = password[:BCRYPT_MAX_LEN]

# Generate salt and hash
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print("Hashed:", hashed)

# Verify (truncate if necessary)
password_to_check = b"A"*100
if len(password_to_check) > BCRYPT_MAX_LEN:
    print(f"Warning: password to verify is longer than {BCRYPT_MAX_LEN} bytes, truncating.")
    password_to_check = password_to_check[:BCRYPT_MAX_LEN]

is_correct = bcrypt.checkpw(password_to_check, hashed)
print("Verify:", is_correct)
