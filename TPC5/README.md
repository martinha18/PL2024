# TPC5: Máquina de Vending
## 2024-03-08

## Autor

- A100593
- Marta Sofia Matos Castela Queirós Gonçalves

## Resumo

Temos uma tabela com id, nome e preço de alguns produtos.

Os preços e outros valores monetários são expressos da seguinte forma: 2e 50c

O utilizador pode recorrer às seguintes operações:

- LISTAR
    - apresenta os produtos da lista

- MOEDA seguido de um conjunto de moedas separadas por vírgulas e terminadas em ponto final (1e, 20c, 10c.)
    - depósito do valor correspondente à soma das moedas
    - apresenta o valor do saldo atual

- SELECIONAR seguido do id de um produto
    - caso tenha saldo suficiente para a compra do produto selecionado, retira esse valor ao saldo e apresenta-o
    - caso contrário dá erro

- SAIR
    - apresenta o valor do troco (preferencialmente como uma lista de moedas)

### Funcionamento:

    maq: 2024-03-08, Stock carregado, Estado atualizado.
    maq: Bom dia. Estou disponível para atender o seu pedido.
    >> LISTAR
    maq:
    cod | nome | quantidade | preço
    ---------------------------------
    A23 água 0.5L 8 0.7
    ...
    >> MOEDA 1e, 20c, 5c, 5c .
    maq: Saldo = 1e30c
    >> SELECIONAR A23
    maq: Pode retirar o produto dispensado "água 0.5L"
    maq: Saldo = 60c
    >> SELECIONAR A23
    maq: Saldo insufuciente para satisfazer o seu pedido
    maq: Saldo = 60c; Pedido = 70c
    >> ...
    ...
    maq: Saldo = 74c
    >> SAIR
    maq: Pode retirar o troco: 1x 50c, 1x 20c e 2x 2c.
    maq: Até à próxima

