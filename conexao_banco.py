import psycopg2

def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname="facial",
            user="postgres",
            password=123,
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
