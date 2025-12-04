from lexer.lexical_code_scanner import LexicalCodeScanner
from syntax.parser import Parser
from syntax.tree import draw_tree
import sys
import os

def parse_code_example_file(filename: str):
     with open(filename, 'r') as f:
        codigo = f.read()
        sc = LexicalCodeScanner(codigo)
        sc.scan_all()
        tokens = sc.get_tokens()

        parser = Parser(tokens)
        ast = parser.parse_program()

        if len(parser.errors) == 0:
            draw_tree(ast, filename + ".png")
            print(f"[{filename}] - OK — AST construída")
        else:
            print(f"[{filename}] - ERROS SINTÁTICOS")
        for error in parser.errors:
            print(f"  {error}")

SOURCE_DIR = "code_examples"

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Uso: python main.py <arquivo_fonte>")

        try:
            available_files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f))]
            
            if available_files:
                print(f"Arquivos disponíveis para análise léxica:")
                for file in available_files:
                    print(f"- {file}")
            else:
                print(f"Nenhum arquivo encontrado com esse nome.")
            
        except OSError as e:
            print(f"Erro ao listar arquivos': {e}")

        sys.exit(1)
    else:
        filename = sys.argv[1]
        filepath = os.path.join(SOURCE_DIR, filename)

        try:
            parse_code_example_file(filepath)
        except FileNotFoundError:
            print(f"Erro: O arquivo '{filename}' não foi encontrado'.")
            sys.exit(1)

