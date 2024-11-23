import face_recognition
import cv2
import psycopg2
from conexao_banco import conectar_banco

# Função para salvar o usuário no banco de dados
def salvar_usuario(nome_usuario, codificacao):
    if codificacao is None:
        print("Erro: A codificação facial não foi gerada corretamente.")
        return

    conn = conectar_banco()  # Conectando ao banco de dados
    cursor = conn.cursor()

    # Converte a codificação de face para um formato adequado para o banco de dados (bytes)
    codificacao_bytes = psycopg2.Binary(codificacao)

    # Insere o usuário e sua codificação facial na tabela facial_pessoa
    cursor.execute("INSERT INTO facial_pessoa (nome, codificacao_facial) VALUES (%s, %s)",
                   (nome_usuario, codificacao_bytes))

    conn.commit()
    cursor.close()
    conn.close()


def capturar_foto_usuario(nome_usuario):
    # Captura de imagem usando a webcam
    video_capture = cv2.VideoCapture(0)
    print(f"Capturando imagem para o usuário: {nome_usuario}...")
    input("Pressione Enter para capturar a imagem...")

    # Captura um único quadro da câmera
    ret, frame = video_capture.read()

    if not ret:
        print("Erro ao capturar imagem da webcam.")
        video_capture.release()
        return None

    # Libera a webcam
    video_capture.release()

    # Converte a imagem de BGR (OpenCV) para RGB (face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detecta as localizações de faces
    face_locations = face_recognition.face_locations(rgb_frame)
    print(f"Faces detectadas: {len(face_locations)}")

    # Certifique-se de que pelo menos uma face foi detectada
    if len(face_locations) == 0:
        print("Nenhuma face detectada. Tente novamente com melhor iluminação ou posição.")
        return None

    try:
        # Gera a codificação facial da primeira face detectada
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if len(face_encodings) > 0:
            print("Codificação facial gerada com sucesso.")
            return face_encodings[0]
        else:
            print("Erro: Falha ao gerar codificação facial.")
            return None
    except Exception as e:
        print(f"Erro ao gerar codificação facial: {e}")
        return None