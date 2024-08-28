from datetime import date, datetime, timedelta

menu = """

Digite [1] para Depositar
Digite [2] para Sacar
Digite [3] para Extrato
Digite [4] para Sair

=> """
saldo = 0
limite = 500
extrato = ""
data_hora_atual = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            data_hora_atual = datetime.now()
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f} --- {data_hora_atual.strftime("%d/%m/%Y %H:%M")}\n "

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES



        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            data_hora_atual = datetime.now()
            extrato += f"Saque: R$ {valor:.2f}----- {data_hora_atual.strftime("%d/%m/%Y %H:%M")}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "3":
        print("\n================ EXTRATO ================")
        print(f"\n================{data_hora_atual.now().date()}================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "4":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")