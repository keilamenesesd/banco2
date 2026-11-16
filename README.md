# Banco 2

Exemplo simples de cartão de crédito com o padrão Mediator.

O código foi refeito a partir da primeira versão de `kyaraauruda/index.py`, sem colocar muitas regras ou bibliotecas.

## Rodar o exemplo

```bash
python3 index.py
```

## Rodar os testes

```bash
python3 -m unittest -v
```

## Partes principais

- `Card`: guarda o titular, o saldo e o número.
- `ValidadorLuhn`: confere se o número é válido.
- `GeradorNumero`: cria números novos.
- `Banco`: cadastra cartões e processa pagamentos.
- `PinPad`: pede o pagamento ao `Mediator`.
- `Cliente`: cria cartões para a pessoa.

As mudanças foram feitas em commits pequenos para facilitar a leitura da evolução do código.
