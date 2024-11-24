import face_recognition
import cv2
import psycopg2
from conexao_banco import conectar_banco
from comunicacao_arduino import enviar_comando_esp8266
import numpy as np

def verificar_usuario():
    """
    Captura o rosto do usuário via webcam e retorna a codificação facial.
    """
    video_capture = cv2.VideoCapture(0)
    print("Aguardando captura do rosto...")

    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            video_capture.release()
            cv2.destroyAllWindows()
            return face_encodings[0]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return None


def autenticar_usuario(codificacao_usuario):
    """Autentica o usuário comparando a codificação facial com os dados no banco."""
    conn = conectar_banco()  # Função para conectar ao banco de dados
    cur = conn.cursor()

    try:
        # Consulta as codificações de todos os usuários cadastrados
        cur.execute("SELECT id, nome, codificacao_facial FROM facial_pessoa")
        usuarios = cur.fetchall()

        for usuario in usuarios:
            id, nome, codificacao_banco = usuario

            # Convertendo a codificação facial armazenada no banco de dados para um array numpy
            codificacao_banco = np.frombuffer(codificacao_banco, dtype=np.float64)

            # A função compare_faces aceita uma lista de codificações faciais para comparação
            resultado_comparacao = face_recognition.compare_faces(
                [codificacao_banco],  # Usando a codificação diretamente aqui
                codificacao_usuario
            )

            # Se encontrar um rosto correspondente, autoriza o acesso
            if resultado_comparacao[0]:
                print(f"Acesso permitido! Bem-vindo, {nome}.")
                # Envia o comando ao ESP8266
                enviar_comando_esp8266("ACESSO_LIBERADO")
                return nome  # Retorna o nome do usuário autenticado

        # Se nenhuma correspondência for encontrada, nega o acesso
        print("Acesso negado! Rosto não encontrado no banco de dados.")
        # Envia o comando de acesso negado ao ESP8266
        enviar_comando_esp8266("ACESSO_NEGADO")
        return None  # Retorna None quando o acesso é negado
    except Exception as e:
        print(f"Erro na autenticação: {e}")
    finally:
        cur.close()
        conn.close()