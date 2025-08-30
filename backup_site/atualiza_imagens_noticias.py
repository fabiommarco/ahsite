import psycopg2

# Configurações do banco
DB_NAME = 'ahsite'
DB_USER = 'postgres'
DB_PASSWORD = 'Deus@2025'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Lista de pares (object_id_antigo, id_noticia_novo)
# Exemplo: [(15, 161), (20, 170)]
PAIRES = [
    (15, 161),
    # Adicione outros pares conforme necessário
]

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

for antigo, novo in PAIRES:
    print(f"Atualizando imagens de object_id={antigo} para object_id={novo}...")
    cur.execute(
        """
        UPDATE app_imagem
        SET object_id = %s
        WHERE content_type_id = 15 AND object_id = %s;
        """,
        (novo, antigo)
    )
    print(f"Linhas afetadas: {cur.rowcount}")

conn.commit()
cur.close()
conn.close()
print("Atualização concluída!") 