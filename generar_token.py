from nexus.security import create_access_token

# Generamos un token para el usuario 'admin_raul'
token = create_access_token({"sub": "admin_raul"})

print("-" * 30)
print("TU TOKEN DE ACCESO ES:")
print(token)
print("-" * 30)
