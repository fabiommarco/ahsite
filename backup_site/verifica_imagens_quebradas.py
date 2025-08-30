import os
import psycopg2

# Configurações do banco
DB_NAME = 'ahsite'
DB_USER = 'postgres'
DB_PASSWORD = 'Deus@2025'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Caminho base das imagens
MEDIA_ROOT = os.path.join(os.getcwd(), 'media')

# Conectar ao banco
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

cur.execute("SELECT id, imagem FROM app_imagem;")
rows = cur.fetchall()

print('Imagens cadastradas que não existem fisicamente:')
for img_id, img_path in rows:
    if not img_path:
        continue
    full_path = os.path.join(MEDIA_ROOT, img_path.replace('/', os.sep))
    if not os.path.isfile(full_path):
        print(f"ID: {img_id} | Caminho: {img_path}")

cur.close()
conn.close() 