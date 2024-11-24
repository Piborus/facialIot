import face_recognition
import cv2
import psycopg2
from conexao_banco import conectar_banco

def salvar_usuario(nome_usuario, codificacao):
    """
    Salva um novo usuário no banco de dados.
    """
    if codificacao is None:
        print("Erro: A codificação facial não foi gerada corretamente.")
        return

    conn = conectar_banco()
    cursor = conn.cursor()

    codificacao_bytes = psycopg2.Binary(codificacao)  # Converte a codificação para bytes
    cursor.execute("INSERT INTO facial_pessoa (nome, codificacao_facial) VALUES (%s, %s)",
                   (nome_usuario, codificacao_bytes))

    conn.commit()
    cursor.close()
    conn.close()


def capturar_foto_usuario(nome_usuario):
    """
    Captura uma foto usando a webcam e gera a codificação facial.
    """
    video_capture = cv2.VideoCapture(0)
    print(f"Capturando imagem para o usuário: {nome_usuario}...")
    input("Pressione Enter para capturar a imagem...")

    ret, frame = video_capture.read()

    if not ret:
        print("Erro ao capturar imagem da webcam.")
        video_capture.release()
        return None

    video_capture.release()

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)

    if len(face_locations) == 0:
        print("Nenhuma face detectada.")
        return None

    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    if len(face_encodings) > 0:
        return face_encodings[0]
    else:
        print("Erro ao gerar codificação facial.")
        return None
