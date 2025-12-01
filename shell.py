import importlib
import bat
import inspect

importlib.reload(bat)

def _conta_chaves(texto):
    return texto.count('{') - texto.count('}')

def iniciar_repl():
   
    print("Bem-vindo ao REPL da Linguagem bat.")
    print("Digite 'SAIR' ou 'EXIT' para terminar.")
    print("Para blocos: digite a linha com '{' e depois finalize com '}' em outra(s) linha(s).")

    buffer = []
    balance = 0

    while True:
        try:
            prompt = ">>> " if balance == 0 else "... "
            linha = input(prompt)

            # possibilita usar comandos internos quando não estiver dentro de bloco
            if balance == 0 and linha is not None and linha.strip().startswith(':'):
                cmd = linha.strip().lower()
                if cmd == ':reload':
                    try:
                        importlib.reload(bat)
                        print("nodlehs recarregado a partir de:", bat.__file__)
                    except Exception as e:
                        print("Erro ao recarregar nodlehs:", e)
                    continue
                if cmd == ':where':
                    try:
                        print("nodlehs carregado de:", bat.__file__)
                    except Exception as e:
                        print("Erro:", e)
                    continue
                if cmd == ':ifsrc':
                    try:
                        print(inspect.getsource(bat.Parser.ifexpr))
                    except Exception as e:
                        print("Não foi possível obter o source de ifexpr:", e)
                    continue

            if linha is None:
                continue

            # Comandos de saída (quando estiver em buffer vazio)
            if balance == 0 and linha.strip().upper() in ('SAIR', 'EXIT'):
                break

            # Ignora linhas vazias (quando não estamos dentro de um bloco)
            if balance == 0 and not linha.strip():
                continue

            # Acumula linhas
            buffer.append(linha)
            balance += _conta_chaves(linha)

            # Detecta excesso de '}' (balance negativo) e reseta com aviso
            if balance < 0:
                print("Erro de sintaxe: '}' sem correspondente '{'. Buffer descartado.")
                buffer = []
                balance = 0
                continue

            # Se o balanceamento for positivo, ainda falta fechar '}' -> continuar lendo
            if balance > 0:
                continue

            # Se balance == 0: temos um comando completo
            texto = '\n'.join(buffer).strip()
            buffer = []
            balance = 0

            if not texto:
                continue

            # Executa (REPL deve manter variáveis)
            resultado, erro = bat.run("<stdin>", texto, reset_vars=False)

            if erro:
                if hasattr(erro, 'printDoErro'):
                    try:
                        print('--- ERRO ---')
                        print(erro.printDoErro())
                        print('------------')
                    except Exception:
                        print('Erro:', erro)
                else:
                    print('Erro:', erro)
            else:
                if resultado is not None:
                    print(resultado)

        except KeyboardInterrupt:
            print("\nSaindo do REPL.")
            break
        except EOFError:
            print("\nSaindo do REPL.")
            break
        except Exception as e:
            print(f"Erro interno do REPL: {e}")

if __name__ == '__main__':
    iniciar_repl()
