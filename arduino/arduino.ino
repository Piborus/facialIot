#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Servo.h>

// Informações de conexão Wi-Fi
const char* ssid = "seu_wifi";               // Substitua com o nome da sua rede Wi-Fi
const char* password = "senha_wifi";         // Substitua com a senha da sua rede Wi-Fi
const char* server = "http://<IP_PYTHON_SERVER>:<PORTA>/verificar"; // Endereço do servidor Python

// Pinos
const int buttonPin = D2;                    // Pino do botão
const int ledAmareloPin = D5;                // Pino do LED amarelo
const int ledVerdePin = D6;                  // Pino do LED verde
const int ledVermelhoPin = D7;               // Pino do LED vermelho
const int servoPin = D4;                    // Pino do servo motor

Servo servoMotor;                            // Servo motor

void setup() {
  // Inicializa os pinos
  pinMode(buttonPin, INPUT_PULLUP);          // Configura o pino do botão como entrada com pull-up
  pinMode(ledAmareloPin, OUTPUT);            // Configura o LED amarelo como saída
  pinMode(ledVerdePin, OUTPUT);              // Configura o LED verde como saída
  pinMode(ledVermelhoPin, OUTPUT);           // Configura o LED vermelho como saída
  servoMotor.attach(servoPin);               // Configura o pino do servo motor

  // Inicializa o Serial Monitor
  Serial.begin(115200);

  // Conecta-se ao Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado ao Wi-Fi");
}

void loop() {
  // Verifica se o botão foi pressionado
  if (digitalRead(buttonPin) == LOW) {      // Se o botão for pressionado
    digitalWrite(ledAmareloPin, HIGH);      // Liga o LED amarelo
    delay(200);                             // Espera um pouco para garantir que o botão foi pressionado
    verificarAcesso();                      // Chama a função para verificar o acesso
    digitalWrite(ledAmareloPin, LOW);       // Desliga o LED amarelo
  }
  delay(100);
}

void verificarAcesso() {
  WiFiClient client;

  if (client.connect(server, 80)) {         // Conecta-se ao servidor Python
    Serial.println("Enviando requisição para o servidor...");

    // Envia a requisição para o servidor
    client.print(String("GET /verificar HTTP/1.1\r\n") +
                 "Host: " + server + "\r\n" +
                 "Connection: close\r\n\r\n");

    unsigned long timeout = millis();
    while (client.available() == 0) {
      if (millis() - timeout > 5000) {     // Timeout de 5 segundos
        Serial.println("Erro na comunicação com o servidor.");
        return;
      }
    }

    // Lê a resposta do servidor
    String resposta = client.readString();
    Serial.println("Resposta recebida do servidor: " + resposta);

    // Verifica a resposta do servidor
    if (resposta.indexOf("Acesso liberado") >= 0) {
      // Se o acesso for liberado
      digitalWrite(ledVerdePin, HIGH);      // Acende o LED verde
      digitalWrite(ledVermelhoPin, LOW);    // Desliga o LED vermelho
      servoMotor.write(90);                 // Ativa o servo motor (90 graus)
      delay(5000);                          // Aguarda por 5 segundos
      servoMotor.write(0);                  // Retorna o servo à posição inicial
    } else {
      // Se o acesso for negado
      digitalWrite(ledVerdePin, LOW);       // Desliga o LED verde
      digitalWrite(ledVermelhoPin, HIGH);   // Acende o LED vermelho
      servoMotor.write(0);                  // Não ativa o servo motor
    }
  } else {
    Serial.println("Falha na conexão com o servidor.");
  }

  client.stop();
}
