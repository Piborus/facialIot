from registro_usuario import salvar_usuario, capturar_foto_usuario
from verificacao_acesso import verificar_usuario, autenticar_usuario

def menu():
    print("1. Registrar novo usuário")
    print("2. Verificar acesso")
    escolha = input("Escolha uma opção: ")
    
    if escolha == "1":
        nome_usuario = input("Digite o nome do usuário para registro: ")
        codificacao = capturar_foto_usuario(nome_usuario)
        salvar_usuario(nome_usuario, codificacao)
    elif escolha == "2":
        codificacao_usuario = verificar_usuario()
        autenticar_usuario(codificacao_usuario)
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    menu()
