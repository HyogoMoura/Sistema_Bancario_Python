from abc import ABC, abstractmethod
import datetime

formato_tempoBR="%d-%m-%Y %H:%M:%s"

class Cliente:
    def __init__(self, endereco:str) -> None:
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco: str) -> None:
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo=0
        self._numero=numero
        self._agencia="001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod    #recebe cliente e numero e retorna uma instancia de conta
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
      
    @property #normalmente utilizados para acessar atributos privados
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        exedeu_saldo = valor > saldo
        
        if exedeu_saldo:
            print("Operação Falhou! cliente nao possui saldo suficiente")

        elif valor > 0:
            self._saldo -=valor
            print("\t Saque realizado com sucesso")
            return True
        
        else:
            print("Operação falhou valor informado e invalido")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realziado com sucesso")
    
        else:
            print("Operação falhou valor informado invalido")
            return False
        
        return True
    
class Conta_Corrente(Conta):
    def __init__(self, numero, cliente, limite=500,limite_saque=3) -> None:
        super().__init__(numero, cliente)
        self.limite=limite
        self.limite_saque=limite_saque
    
    def sacar(self, valor): # sobrescrita de metodo
        numero_saques = len([transacao for transacao in self.historico.transacao if transacao["tipo"] == saque.__name__])
        excedeu_limite = valor > self.limite
        exedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print("\t Operação falhou, valor do saque excedeu limite")
        
        elif exedeu_saques:
            print("\t Operação falhou numero de saques exedeu maximo permitido por dia")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self) -> str:
        return f"""\
            Agencia : \t {self.agencia}
            C/C: \t\t{self.numero}
            Titular: \t{self.cliente.nome}
            """
            
class Historico:
    def __init__(self) -> None:
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacoes(self, transacoes):
        self._transacoes.append(
            {
                "Tipo": transacao.__class__.__name__,
                "Valor": transacao.valor,
                "data": datetime.now().strtime(formato_tempoBR)
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def regitrar(self,conta):
        pass

class Saque(Transacao):
    def __init__(self,valor) -> None:
        self._valor=valor
    
    @property
    def valor(self):
        return self._valor
    
    def regitrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor) -> None:
        self._valor=valor
    
    @property
    def valor(self):
        return self._valor
    
    def regitrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    =========================MENU========================
    [1]\t Depositar
    [2]\t Sacar
    [3]\t Extrato
    [4]\t Nova Conta
    [5]\t Listar Contas
    [6]\t Novo Usuario
    [7]\t Sair
    =====================================================
    """
    return input(textwrap.dedent(menu))

def filtrar_clientes(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.conta:
        print("\n Cliente nao possui conta")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    clientes = filtrar_clientes(cpf, clientes)
    
    if not clientes:
        print(" \n Cliente nao encontrado")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(Cliente)
    if not conta:
        return
    
    Cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print(" Cliente nao encontrado")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf= input("Informe cpf do cliente")
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print("Client enao encontrado")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("============Extrato=============")
    transacoes = conta.historico.trasacoes
    
    extrato= ""
    if not transacoes:
        extrato = "Nao foram realizados movimentacoes"
    else:
        for transacao in transacoes:
            extrato += f"\n {transacao['tipo']}: \n\tR$ {transacao['valor']:.2f}"
            
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=============================================")

def cria_cliente(clientes):
    cpf = input("Informe o CPF soente numeros")
    cliente = filtrar_clientes(cpf,clientes)
    
    if cliente:
        print("Ja existe cliente com esse CPF")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("informe a data de nascimento")
    endereco = input("Informe o endereço")
    
    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,endereco=endereco)
    
    clientes.append(cliente)
    
    print("Cliente criado com sucesso!")

def cria_conta(numero_conta, clientes, contas):
    cpf=input("Informe o cpd do cliente")
    cliente = filtrar_clientes(cpf,clientes)
    
    if not cliente:
        print("Cliente nao encontrados")
        return
    
    conta = Conta_Corrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("Conta criada com sucesso")

def listar_contas(contas):
    for conta in contas:
        print("=" + 100)
        print(textwrap.dedent(str(conta)))
    
def main():
    clientes =[]
    conta = []
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            depositar(clientes)
            
        elif opcao == "2":
            sacar(clientes)
            
        elif opcao == "3":
            exibir_extrato(clientes)
            
        elif opcao == "4":
            cria_cliente(clientes)
            
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
            
        elif opcao == "6":
            listar_contas(contas)
            
        elif opcao == "7":
            break        
        else:
            print("Operação invalida, selecione dentro dos numeros do menu")
    
main()