import face_recognition
import cv2
import psycopg2
from conexao_banco import conectar_banco
from comunicacao_arduino import enviar_comando_serial
import numpy as np

def verificar_usuario():
    """Captura o rosto do usuário via webcam e retorna a codificação facial."""
    # Inicializa a webcam
    video_capture = cv2.VideoCapture(0)
    print("Aguardando captura do rosto...")

    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte para RGB
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')  # Detecta rostos

        if len(face_locations) > 0:  # Verifica se um rosto foi detectado
            print("Rosto detectado! Processando codificação facial...")
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if face_encodings:
                # Retorna a codificação do primeiro rosto detectado
                video_capture.release()
                cv2.destroyAllWindows()
                return face_encodings[0]
            else:
                print("Não foi possível codificar o rosto. Tente novamente.")

        # Mostra a imagem capturada ao vivo
        cv2.imshow("Pressione 'q' para sair", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a câmera e fecha as janelas
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
                enviar_comando_serial("ACESSO_LIBERADO")
                return True

        # Se nenhuma correspondência for encontrada, nega o acesso
        print("Acesso negado! Rosto não encontrado no banco de dados.")
        enviar_comando_serial("ACESSO_NEGADO")
        return False
    except Exception as e:
        print(f"Erro na autenticação: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    try:
        # Captura a codificação facial do usuário
        codificacao_usuario = verificar_usuario()

        if codificacao_usuario is not None:
            # Autentica o usuário comparando com o banco de dados
            autenticar_usuario(codificacao_usuario)
        else:
            print("Nenhum rosto detectado ou erro ao capturar codificação facial.")
    except Exception as e:
        print(f"Erro no processo principal: {e}")
