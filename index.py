import random
from abc import ABC, abstractmethod


class Mediator(ABC):
    @abstractmethod
    def validar_cartao(self, cartao: 'Card') -> bool:
        pass


class Card:
    def __init__(self, titular: str, saldo: float = 0.0, numero: str | None = None):
        self.titular = titular
        self.saldo = saldo
        self.numero = numero or self.gerar_numero()

    @staticmethod
    def gerar_numero() -> str:
        base = [random.randint(0, 9) for _ in range(15)]
        soma = 0

        for idx, dig in enumerate(reversed(base)):
            val = dig
            if idx % 2 == 0:
                val *= 2
                if val > 9:
                    val -= 9
            soma += val

        fim = (10 - soma % 10) % 10
        return ''.join(str(d) for d in base + [fim])




class ValidadorLuhn:
    def validar(self, numero: str) -> bool:
        digs = [int(d) for d in str(numero) if d.isdigit()]
        if len(digs) < 12:
            return False

        soma = 0
        for idx, dig in enumerate(reversed(digs)):
            val = dig
            if idx % 2 == 1:
                val *= 2
                if val > 9:
                    val -= 9
            soma += val

        return soma % 10 == 0


class Banco(Mediator):
    def __init__(self):
        self.cartoes = []

    def cadastrar(self, cartao: Card):
        self.cartoes.append(cartao)

    def criar_cartao(self, titular: str, saldo: float = 0.0) -> Card:
        cartao = Card(titular, saldo)
        self.cadastrar(cartao)
        return cartao

    def validar_cartao(self, cartao: Card) -> bool:
        if not ValidadorLuhn().validar(cartao.numero):
            print(f'Banco: cartão {cartao.numero} inválido.')
            return False

        if not any(c.numero == cartao.numero for c in self.cartoes):
            print(f'Banco: cartão {cartao.numero} não cadastrado.')
            return False

        return True

    def pagar(self, cartao: Card, valor: float) -> bool:
        if not self.validar_cartao(cartao):
            print('Banco: pagamento recusado.')
            return False

        if cartao.saldo < valor:
            print('Banco: saldo insuficiente.')
            return False

        cartao.saldo -= valor
        print(f'Banco: pagamento aprovado. Saldo: R$ {cartao.saldo:.2f}.')
        return True


class PinPad:
    def __init__(self, banco: Banco):
        self.banco = banco

    def pagar(self, cartao: Card, valor: float) -> bool:
        if not ValidadorLuhn().validar(cartao.numero):
            print('PinPad: cartão inválido.')
            return False

        return self.banco.pagar(cartao, valor)


class Cliente:
    def __init__(self, nome: str, banco: Banco):
        self.nome = nome
        self.banco = banco
        self.cartoes = []

    def criar_cartao(self, saldo: float = 0.0) -> Card:
        cartao = self.banco.criar_cartao(self.nome, saldo)
        self.cartoes.append(cartao)
        return cartao


if __name__ == '__main__':
    banco = Banco()
    pinpad = PinPad(banco)
    cliente = Cliente('Ana', banco)

    cartao = cliente.criar_cartao(500.00)
    print(f'Cartão: {cartao.numero} | Saldo: R$ {cartao.saldo:.2f}')
    pinpad.pagar(cartao, 120.50)
