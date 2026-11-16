import unittest

from index import Banco, Card, Mediator, PinPad, ValidadorLuhn


class MedFake(Mediator):
    def __init__(self):
        self.req = None

    def processar(self, cartao, valor):
        self.req = (cartao, valor)
        return True


class ValFake:
    def validar(self, numero):
        return False


class TestCartao(unittest.TestCase):
    def test_luhn(self):
        self.assertTrue(ValidadorLuhn().validar('4532015112830366'))
        self.assertFalse(ValidadorLuhn().validar('4532015112830367'))

    def test_cartao_novo_tem_numero_valido(self):
        cartao = Card('Ana')
        self.assertEqual(len(cartao.numero), 16)
        self.assertTrue(ValidadorLuhn().validar(cartao.numero))

    def test_pagamento_aprovado(self):
        banco = Banco()
        cartao = banco.criar_cartao('Ana', 100.00)

        self.assertTrue(banco.processar(cartao, 25.00))
        self.assertEqual(cartao.saldo, 75.00)

    def test_banco_aceita_validador_trocado(self):
        banco = Banco(validador=ValFake())
        cartao = Card('Ana', numero='4532015112830366')
        banco.cadastrar(cartao)

        self.assertFalse(banco.processar(cartao, 10.00))

    def test_pinpad_usa_o_mediator(self):
        med = MedFake()
        cartao = Card('Ana', numero='4532015112830366')

        self.assertTrue(PinPad(med).pagar(cartao, 10.00))
        self.assertEqual(med.req, (cartao, 10.00))


if __name__ == '__main__':
    unittest.main()
