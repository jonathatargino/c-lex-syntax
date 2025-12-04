from lexer.lexical_code_scanner import LexicalCodeScanner
import sys
import os

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
            with open(filepath, 'r') as f:
                codigo = f.read()
                sc = LexicalCodeScanner(codigo)
                sc.scan_all()
                sc.print_tokens()
                sc.print_symbol_table(sort_by_name=False)
        except FileNotFoundError:
            print(f"Erro: O arquivo '{filename}' não foi encontrado'.")
            sys.exit(1)