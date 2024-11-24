from flask import Flask, jsonify, request
from registro_usuario import capturar_foto_usuario, salvar_usuario
from verificacao_acesso import verificar_usuario, autenticar_usuario

app = Flask(__name__)

@app.route("/registro", methods=["GET"])
def registrar_usuario():
    """
    Endpoint para registrar um novo usuário.
    """
    nome_usuario = request.args.get("nome")  # Nome enviado pelo ESP8266 na URL
    if not nome_usuario:
        return jsonify({"erro": "Nome do usuário não fornecido"}), 400

    codificacao = capturar_foto_usuario(nome_usuario)  # Captura a imagem e gera a codificação facial
    if codificacao:
        salvar_usuario(nome_usuario, codificacao)
        return jsonify({"mensagem": "Usuário registrado com sucesso!"}), 200
    return jsonify({"erro": "Erro ao capturar rosto ou gerar codificação facial"}), 500


@app.route('/verificar', methods=['GET'])
def verificar_acesso():
    # Captura a codificação facial do usuário
    codificacao_usuario = verificar_usuario()

    # Verifica se a codificação foi gerada com sucesso
    if codificacao_usuario is not None and len(codificacao_usuario) > 0:
        # Autentica o usuário comparando com o banco de dados
        nome = autenticar_usuario(codificacao_usuario)

        if nome:  # Se nome não for None, o acesso foi liberado
            return jsonify({"mensagem": f"Acesso liberado! Bem-vindo, {nome}."}), 200
        else:
            return jsonify({"mensagem": "Acesso negado!"}), 403
    else:
        return jsonify({"erro": "Nenhuma codificação facial detectada ou erro ao capturar."}), 400



if __name__ == "__main__":
    app.run(debug=True)  # Isso inicia o servidor Flask