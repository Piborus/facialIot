import requests

def enviar_comando_esp8266(comando):
    """
    Envia um comando para o ESP8266.
    """
    url = f"http://<IP_DO_ESP8266>:<PORTA>/{comando}"  # Substitua pelo IP e porta do ESP8266
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Comando '{comando}' enviado com sucesso!")
        else:
            print(f"Erro ao enviar comando: {response.status_code}")
    except Exception as e:
        print(f"Erro de comunicação com o ESP8266: {e}")
