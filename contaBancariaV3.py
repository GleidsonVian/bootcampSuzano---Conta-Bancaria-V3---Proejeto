from datetime import datetime, date

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[q] Sair

=> """

usuarios = []
contas = []

# Função para verificar se ainda está no mesmo dia
def verificar_dia(dia_atual, transacoes_realizadas):
    hoje = date.today()
    if dia_atual != hoje:
        dia_atual = hoje
        transacoes_realizadas = 0
    return dia_atual, transacoes_realizadas

# ---------------- CADASTRAR USUÁRIO ----------------
def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = next((u for u in usuarios if u["cpf"] == cpf), None)
    
    if usuario_existente:
        print("❌ Já existe um usuário com esse CPF.")
        return usuarios

    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nasc": data_nasc,
        "endereco": endereco
    })

    print("✅ Usuário cadastrado com sucesso!")
    return usuarios

# ---------------- CADASTRAR CONTA ----------------
def cadastrar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do titular: ")
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    
    if usuario:
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        })
        print("✅ Conta criada com sucesso!")
    else:
        print("❌ Usuário não encontrado. Cadastre o usuário antes.")

# ---------------- OPERAÇÕES BANCÁRIAS ----------------
def depositar_dinheiro(saldo, historico_de_extrato):
    dinheiro_para_depositar = int(input('Quanto você deseja depositar? '))
    saldo += dinheiro_para_depositar
    historico_de_extrato += f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Depositado R$ {dinheiro_para_depositar}\n"
    print(f"Depositado {dinheiro_para_depositar}")
    return saldo, historico_de_extrato

def sacar_dinheiro(saldo, quantidade_de_saques, historico_de_extrato, limite_de_saque=500):
    dinheiro_para_sacar = int(input('Quanto você deseja sacar? '))
    if quantidade_de_saques <= 0:
        print("Limite diário de saques atingido")
    elif saldo <= 0:
        print("Não será possível sacar o dinheiro por falta de saldo")
    elif dinheiro_para_sacar > limite_de_saque:
        print(f"Limite de saque é R$ {limite_de_saque}")
    elif dinheiro_para_sacar > saldo:
        print("Não será possível sacar o dinheiro por falta de saldo")
    else:
        saldo -= dinheiro_para_sacar
        quantidade_de_saques -= 1
        print(f"Saque de R$ {dinheiro_para_sacar} realizado com sucesso")
        historico_de_extrato += f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Saque de R$ {dinheiro_para_sacar}\n"
    return saldo, quantidade_de_saques, historico_de_extrato

def mostrar_extrato(saldo, historico_de_extrato):
    print("\n=== Extrato ===")
    print(historico_de_extrato if historico_de_extrato else "Nenhuma transação realizada.")
    print(f"Você possui R${saldo:.2f} na conta")
    print("================\n")

# ---------------- VARIÁVEIS PRINCIPAIS ----------------
saldo = 0
quantidade_de_saques = 3
historico_de_extrato = ""
limite_transacoes = 10
transacoes_realizadas = 0
dia_atual = date.today()
AGENCIA = "0001"
numero_conta = 1

# ---------------- LOOP PRINCIPAL ----------------
while True:
    dia_atual, transacoes_realizadas = verificar_dia(dia_atual, transacoes_realizadas)
    opcao = input(menu)

    if opcao in ['d', 's']:
        if transacoes_realizadas >= limite_transacoes:
            print("Você excedeu o número de transações permitidas para hoje (10).")
            continue

    if opcao == 'd':
        saldo, historico_de_extrato = depositar_dinheiro(saldo, historico_de_extrato)
        transacoes_realizadas += 1

    elif opcao == 's':
        saldo, quantidade_de_saques, historico_de_extrato = sacar_dinheiro(saldo, quantidade_de_saques, historico_de_extrato)
        transacoes_realizadas += 1

    elif opcao == 'e':
        mostrar_extrato(saldo, historico_de_extrato)

    elif opcao == 'nu':
        usuarios = cadastrar_usuario(usuarios)

    elif opcao == 'nc':
        cadastrar_conta(AGENCIA, numero_conta, usuarios)
        numero_conta += 1

    elif opcao == 'q':
        print('Obrigado por usar nosso programa, até breve')
        break

    else:
        print('Operação inválida, por favor selecione novamente a operação desejada')
