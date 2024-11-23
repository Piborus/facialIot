import serial
import time

def enviar_comando_serial(comando):
    # Configurar a comunicação serial com o Arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Ajuste a porta conforme necessário
    time.sleep(2)  # Aguarda o Arduino inicializar
    
    if comando == "ACESSO_LIBERADO":
        ser.write(b'1')  # Envia o sinal de liberação
        print("Comando de liberação enviado ao Arduino.")
    elif comando == "ACESSO_NEGADO":
        ser.write(b'0')  # Envia o sinal de negação
        print("Comando de negação enviado ao Arduino.")
    
    ser.close()
