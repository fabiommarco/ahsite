#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def reset_admin_password():
    """Redefine a senha do admin"""
    
    print("🔍 Verificando usuários existentes...")
    
    # Lista todos os usuários
    users = User.objects.all()
    if not users.exists():
        print("❌ Nenhum usuário encontrado no banco de dados.")
        return
    
    print(f"\n📋 Usuários encontrados ({users.count()}):")
    for user in users:
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Is Staff: {user.is_staff}")
        print(f"  Is Superuser: {user.is_superuser}")
        print(f"  Is Active: {user.is_active}")
        print("  ---")
    
    # Procura por usuários admin
    admin_users = User.objects.filter(is_superuser=True)
    if admin_users.exists():
        print(f"\n👑 Usuários administradores encontrados ({admin_users.count()}):")
        for user in admin_users:
            print(f"  - {user.username} ({user.email})")
        
        # Redefine senha para o primeiro admin
        admin_user = admin_users.first()
        new_password = "admin123"
        
        print(f"\n🔄 Redefinindo senha para: {admin_user.username}")
        admin_user.password = make_password(new_password)
        admin_user.save()
        
        print(f"✅ Senha redefinida com sucesso!")
        print(f"👤 Usuário: {admin_user.username}")
        print(f"🔑 Nova senha: {new_password}")
        print(f"📧 Email: {admin_user.email}")
        
    else:
        # Cria um novo usuário admin
        print("\n❌ Nenhum usuário administrador encontrado.")
        print("🆕 Criando novo usuário administrador...")
        
        username = "admin"
        email = "admin@ah.agr.br"
        password = "admin123"
        
        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.password = make_password(password)
            user.save()
            print(f"✅ Usuário {username} atualizado como administrador!")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_superuser=True,
                is_staff=True
            )
            print(f"✅ Novo usuário administrador criado!")
        
        print(f"👤 Usuário: {username}")
        print(f"🔑 Senha: {password}")
        print(f"📧 Email: {email}")
    
    print(f"\n🌐 Acesse: http://localhost:8000/admin/")
    print(f"⚠️  IMPORTANTE: Altere a senha após o primeiro login!")

if __name__ == "__main__":
    print("🚀 Redefinindo senha do administrador...")
    reset_admin_password()
    print("✅ Concluído!") 