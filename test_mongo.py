"""Script para testar conexão com MongoDB Atlas"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carregar .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("❌ MONGO_URI não encontrada no arquivo .env")
    print("\n📝 Certifique-se que o arquivo .env existe com:")
    print("MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/...")
    exit(1)

# Mostrar URI (ocultando senha)
uri_parts = MONGO_URI.split("@")
if len(uri_parts) > 1:
    user_part = uri_parts[0].split("//")[1] if "//" in uri_parts[0] else uri_parts[0]
    username = user_part.split(":")[0] if ":" in user_part else user_part
    print(f"🔍 Testando conexão...")
    print(f"   Usuário: {username}")
    print(f"   Cluster: {uri_parts[1][:50]}...")
else:
    print(f"🔍 URI: {MONGO_URI[:50]}...")

print("\n⏳ Conectando ao MongoDB Atlas...")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Testar conexão
    client.admin.command('ping')
    
    print("✅ Conexão bem-sucedida!")
    
    # Listar databases
    dbs = client.list_database_names()
    print(f"\n📊 Databases disponíveis: {dbs}")
    
    # Testar database específico
    db = client["lat-long-superacao"]
    collections = db.list_collection_names()
    print(f"📁 Collections em 'lat-long-superacao': {collections if collections else '(vazio)'}")
    
    print("\n🎉 Tudo funcionando! Pode executar: python app-mongo.py")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\n🔧 Possíveis soluções:")
    print("1. Verifique a senha no MongoDB Atlas:")
    print("   https://cloud.mongodb.com → Database Access → EDIT user → Edit Password")
    print("\n2. Se a senha tem caracteres especiais (@#%/), use URL encoding:")
    print("   @ → %40,  # → %23,  % → %25,  / → %2F")
    print("\n3. Certifique-se que o IP está na whitelist:")
    print("   https://cloud.mongodb.com → Network Access → Add IP (0.0.0.0/0 para qualquer IP)")
    print("\n4. Atualize o arquivo .env com a nova senha")
