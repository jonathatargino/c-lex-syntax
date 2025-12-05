## Descrição do Projeto
Analisador léxico e sintático para a linguagem de programação C

### Analisador léxico
O scanner é responsável por varrer o texto e produzir uma sequência de tokens classificados. Para cada token, o scanner normalmente registra:
- tipo (p.ex. ID, NUM, operadores, delimitadores),
- lexema (a sequência de caracteres),
- posição (linha e coluna) — útil para mensagens de erro e mapeamento na AST.
No projeto, os tokens são instanciados como objetos (classe Token) e utilizados pelos testes de unidade para garantir que a tokenização de trechos de código produza a sequência esperada.

### Analisador sintático
O parser consome a sequência de tokens e aplica regras gramaticais para construir nós de AST. Uma abordagem típica para implementações didáticas é o recursive-descent parsing com funções para cada construçãao sintática (expressões, fatores, declaracões, blocos, comandos de controle).

### Output
O output são imagens de AST construídas de acordo com o código de exemplo

## Setup do projeto

### Requisitos
- Python na versão 3.12 ou superior

### Passo-a-Passo

#### Ativação do ambiente virtual

```bash
python3 -m venv venv
```

```bash
# Windows
venv\Scripts\activate.bat

# Unix
source venv/bin/activate
```

Para mais referências, consulte a <a href='https://docs.python.org/pt-br/3/library/venv.html'>documentação oficial</a>

#### Instalação das dependências

Neste projetos, optamos por utilizar o <a href="https://python-poetry.org/">Poetry</a> como gerenciador de dependências.

```bash
pipx install poetry
```

```bash
poetry install
```

### Execução do projeto
Uma vez que as dependências foram instaladas, para executar o projeto você deve rodar 

```bash
python3 main.py iteration.c
```

O projeto possui vários exemplos na pasta `/code_examples` disponíveis para serem utilizados na execução.

#### Exemplos corretos lexicamente e sintaticamente
- conditional.c
- let_assign.c
- let_assign_expression.c
- indexation.c
- arithmetic_expression.c

Todos examplos acima devem criar uma imagem png na pasta `/code_examples` com o respectivo nome do exemplo.

<img width="1584" height="1104" alt="image" src="https://github.com/user-attachments/assets/81db9cfc-f821-4800-b748-1bcd01af5a83" />


#### Exemplos incorretos
- invalid_arithmetic_expression.c
  - Output esperado: [ERRO] Esperado RPAREN, obtido TokenType.SEMI na linha 1
- invalid_indexation.c
  - Output esperado: [ERRO] Esperado RBRACK, obtido TokenType.SEMI na linha 1
- invalid_conditional.c
  - Output esperado: [ERRO] 'else' sem 'if' correspondente na linha 1 
- invalid_while.c
  - Output esperado:  [ERRO] Esperado RPAREN, obtido TokenType.LBRACE na linha 1
- invalid_let.c
  - Ouput esperado: [ERRO] Esperado TokenType.ASSIGN, obtido TokenType.NUM na linha 1 

