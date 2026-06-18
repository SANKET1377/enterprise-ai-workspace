from app.security.auth import hash_password

password = "Sanket123"

hashed = hash_password(password)

print("Password:", password)
print("Hash:", hashed)