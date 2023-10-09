import bcrypt

admin_password = 'enteradminpasswordhere'
hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
print(hashed_password)
