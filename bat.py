# --- tokens ---
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_SUM = 'SUM'
TT_MINUS = 'MINUS'
TT_MULT = 'MULT'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'
TT_EQ = 'EQ'
TT_ID = 'ID'

TT_IF = 'IF'
TT_ELSE = 'ELSE'
TT_MAIOR = 'MAIOR'
TT_MENOR = 'MENOR'
TT_MAIOR_IGUAL = 'MAIOR_IGUAL'
TT_MENOR_IGUAL = 'MENOR_IGUAL'
TT_DIFERENTE = 'DIFERENTE'
TT_ABRE_CHAVE = 'ABRE_CHAVE'
TT_FECHA_CHAVE = 'FECHA_CHAVE'




# --- Erros ---
class Erro(Exception):
    def __init__(self, posInicio, posFinal, nomeDoErro, detalheDoErro):
        super().__init__(f'{nomeDoErro}: {detalheDoErro}')
        self.posInicio = posInicio
        self.posFinal = posFinal
        self.nomeDoErro = nomeDoErro
        self.detalhedoErro = detalheDoErro

    def printDoErro(self):
        resultado = f'{self.nomeDoErro}: {self.detalhedoErro}\n'
        resultado += f'Posicao do Erro -> Linha: {self.posInicio.linha}, Coluna: {self.posInicio.coluna}\n'
        resultado += f'Arquivo: {self.posInicio.nomeArquivo}'
        return resultado


class ErroCaractereInvalido(Erro):
    def __init__(self, posInicio, posFinal, detalheDoErro):
        super().__init__(posInicio, posFinal, 'Erro de Caractere Inválido', detalheDoErro)


class ErroSintaxeInvalida(Erro):
    def __init__(self, detalheDoErro, posErro=None):
        # Assumindo que posErro é um objeto Posicao
        if posErro is None:
            posErro = Posicao(0, 0, 0, 'Desconhecido')
        super().__init__(posErro, posErro, 'Erro de Sintaxe', detalheDoErro)


class ErroExecucao(Erro):
    def __init__(self, detalheDoErro, posErro=None):
        if posErro is None:
            posErro = Posicao(0, 0, 0, 'Execução')
        super().__init__(posErro, posErro, 'Erro de Execução', detalheDoErro)


class Posicao:
    def __init__(self, indice, linha, coluna, nomeArquivo):
        self.indice = indice
        self.linha = linha
        self.coluna = coluna
        self.nomeArquivo = nomeArquivo

    def avancar(self, atual=None):
        self.indice += 1
        self.coluna += 1

        if atual == '\n':
            self.coluna = 0
            self.linha += 1

        return self

    def copia(self):
        return Posicao(self.indice, self.linha, self.coluna, self.nomeArquivo)


class Token:
    def __init__(self, tipo, valor=None, posInicio=None, posFinal=None):
        self.tipo = tipo
        self.valor = valor

        # Adicionado posições ao Token
        if posInicio:
            self.posInicio = posInicio.copia()
            self.posFinal = posFinal.copia()

    def __repr__(self):
        if self.valor is not None:
            return f'{self.tipo}: {self.valor}'
        return f'{self.tipo}'



class IfNode:
    def __init__(self, condicaoNode, corpoNode, elseNode=None):
        self.condicaoNode = condicaoNode
        self.corpoNode = corpoNode
        self.elseNode = elseNode


class BlocoNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f'<Bloco: {self.statements}>'


class NumberNode:
    def __init__(self, token):
        self.token = token


class OpBinario:
    def __init__(self, left, operadorToken, right):
        self.left = left
        self.operadorToken = operadorToken
        self.right = right


class VarAcessNode:
    def __init__(self, token):
        self.token = token


class VarAssignNode:
    def __init__(self, token, valorNode):
        self.token = token
        self.valorNode = valorNode


class PrintNode:
    def __init__(self, valorNode):
        self.valorNode = valorNode


class Lexer:
    def __init__(self, nomeArquivo, texto):
        self.texto = texto
        self.pos = Posicao(-1, 0, -1, nomeArquivo)
        self.atual = None
        self.avancar()

    def avancar(self):
        self.pos.avancar(self.atual)
        if self.pos.indice < len(self.texto):
            self.atual = self.texto[self.pos.indice]
        else:
            self.atual = None

    def makeToken(self):
        tokens = []

        while self.atual is not None:
            posInicio = self.pos.copia()

            if self.atual.isspace():
                self.avancar()

            elif self.atual.isdigit():
                tokens.append(self.floatOrInt(posInicio))

            elif self.atual.isalpha() or self.atual == '_':
                tokens.append(self.makeID(posInicio))

            elif self.atual == '+':
                self.avancar()
                tokens.append(Token(TT_SUM, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '-':
                self.avancar()
                tokens.append(Token(TT_MINUS, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '*':
                self.avancar()
                tokens.append(Token(TT_MULT, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '/':
                self.avancar()
                tokens.append(Token(TT_DIV, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '(':
                self.avancar()
                tokens.append(Token(TT_LPAREN, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == ')':
                self.avancar()
                tokens.append(Token(TT_RPAREN, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '{':
                self.avancar()
                tokens.append(Token(TT_ABRE_CHAVE, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '}':
                self.avancar()
                tokens.append(Token(TT_FECHA_CHAVE, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '=':
                self.avancar()
                tokens.append(Token(TT_EQ, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '>':
                self.avancar()
                if self.atual == '=':
                    self.avancar()
                    tokens.append(Token(TT_MAIOR_IGUAL, posInicio=posInicio, posFinal=self.pos.copia()))
                else:
                    tokens.append(Token(TT_MAIOR, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '<':
                self.avancar()
                if self.atual == '=':
                    self.avancar()
                    tokens.append(Token(TT_MENOR_IGUAL, posInicio=posInicio, posFinal=self.pos.copia()))
                else:
                    tokens.append(Token(TT_MENOR, posInicio=posInicio, posFinal=self.pos.copia()))

            elif self.atual == '!':
                self.avancar()
                if self.atual == '=':
                    self.avancar()
                    tokens.append(Token(TT_DIFERENTE, posInicio=posInicio, posFinal=self.pos.copia()))
                else:
                    return [], ErroCaractereInvalido(
                        posInicio,
                        self.pos,
                        "'!' inválido. Esperava '=' após '!'."
                    )

            else:
                char = self.atual
                self.avancar()
                return [], ErroCaractereInvalido(posInicio, self.pos, char)

        tokens.append(Token(TT_EOF, posInicio=self.pos.copia(), posFinal=self.pos.copia()))
        return tokens, None

    def floatOrInt(self, posInicio):
        contadorDePontos = 0
        numStr = ''

        while self.atual is not None and (self.atual.isdigit() or self.atual == '.'):
            if self.atual == '.':
                if contadorDePontos == 1:
                    break
                contadorDePontos += 1
                numStr += self.atual
            else:
                numStr += self.atual
            self.avancar()

        posFinal = self.pos.copia()
        if contadorDePontos == 1:
            return Token(TT_FLOAT, float(numStr), posInicio, posFinal)
        else:
            return Token(TT_INT, int(numStr), posInicio, posFinal)

    def makeID(self, posInicio):
        idString = ''

        while self.atual is not None and (self.atual.isalpha() or self.atual.isdigit() or self.atual == '_'):
            idString += self.atual
            self.avancar()

        posFinal = self.pos.copia()
        up = idString.upper()

        if up == 'IF':
            return Token(TT_IF, posInicio=posInicio, posFinal=posFinal)
        if up == 'ELSE':
            return Token(TT_ELSE, posInicio=posInicio, posFinal=posFinal)

        return Token(TT_ID, idString, posInicio, posFinal)



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenIndex = -1
        self.tokenAtual = None
        self.avancar()

    def avancar(self):
        self.tokenIndex += 1
        if self.tokenIndex < len(self.tokens):
            self.tokenAtual = self.tokens[self.tokenIndex]
        else:
            # Cria um EOF token com posições válidas (baseado no último token, se existir)
            if len(self.tokens) > 0 and hasattr(self.tokens[-1], 'posFinal'):
                pos = self.tokens[-1].posFinal.copia()
            else:
                pos = Posicao(0, 0, 0, '<stdin>')
            self.tokenAtual = Token(TT_EOF, posInicio=pos, posFinal=pos)
        return self.tokenAtual

    def voltar(self):
        self.tokenIndex -= 1
        self.tokenAtual = self.tokens[self.tokenIndex]

    def factor(self):
        tok = self.tokenAtual

        if tok.tipo in (TT_INT, TT_FLOAT):
            node = NumberNode(tok)
            self.avancar()
            return node

        if tok.tipo == TT_ID:
            self.avancar()
            return VarAcessNode(tok)

        if tok.tipo == TT_LPAREN:
            self.avancar()
            exprNode = self.expr()
            if self.tokenAtual.tipo == TT_RPAREN:
                self.avancar()
                return exprNode
            raise ErroSintaxeInvalida("Esperava encontrar ')'", posErro=self.tokenAtual.posInicio)

        raise ErroSintaxeInvalida("Esperava número, variável ou '('", posErro=self.tokenAtual.posInicio)

    def term(self):
        left = self.factor()

        while self.tokenAtual.tipo in (TT_MULT, TT_DIV):
            operador = self.tokenAtual
            self.avancar()
            right = self.factor()
            left = OpBinario(left, operador, right)

        return left

    def parse_arith(self):
        left = self.term()

        while self.tokenAtual.tipo in (TT_SUM, TT_MINUS):
            operador = self.tokenAtual
            self.avancar()
            right = self.term()
            left = OpBinario(left, operador, right)

        return left

    def expr(self): #expressao
        left = self.parse_arith()
        while self.tokenAtual.tipo in (
            TT_MAIOR,
            TT_MENOR,
            TT_MAIOR_IGUAL,
            TT_MENOR_IGUAL,
            TT_DIFERENTE
            ):
            operador = self.tokenAtual
            self.avancar()
            right = self.parse_arith()
            left = OpBinario(left, operador, right)
        return left

    def block_statements(self): #instrucao
        statements = []

        while self.tokenAtual.tipo != TT_FECHA_CHAVE and self.tokenAtual.tipo != TT_EOF:
            statements.append(self.statment())

        return BlocoNode(statements)

    def statment(self):
        tok = self.tokenAtual

        if tok.tipo == TT_IF:
            return self.ifexpr()

        if tok.tipo == TT_ID and tok.valor is not None and tok.valor.upper() == 'PRINT':
            self.avancar()
            expr = self.expr()
            return PrintNode(expr)

        if tok.tipo == TT_ID:
            varAux = tok
            self.avancar()

            if self.tokenAtual.tipo == TT_EQ:
                self.avancar()
                valorNode = self.expr()
                return VarAssignNode(varAux, valorNode)
            else:
                self.voltar()  # Não era atribuição, trata como acesso à variável

        return self.expr()

    def ifexpr(self): #expressao if
        self.avancar()  
        
        cond = self.expr()

        if self.tokenAtual.tipo == TT_ABRE_CHAVE:
            self.avancar()  
            corpoThen = self.block_statements()
            if self.tokenAtual.tipo != TT_FECHA_CHAVE:
                raise ErroSintaxeInvalida("Esperava '}' após corpo do IF", posErro=self.tokenAtual.posInicio)
            self.avancar()  
        else:
            # Single-line: considera a próxima expressao como corpo do THEN
            corpoThen = self.statment()
        corpoElse = None
        if self.tokenAtual.tipo == TT_ELSE:
            self.avancar()  

            if self.tokenAtual.tipo == TT_ABRE_CHAVE:
                self.avancar()  
                corpoElse = self.block_statements()
                if self.tokenAtual.tipo != TT_FECHA_CHAVE:
                    raise ErroSintaxeInvalida("Esperava '}' após corpo do ELSE", posErro=self.tokenAtual.posInicio)
                self.avancar()  
            else:
                corpoElse = self.statment()

        return IfNode(cond, corpoThen, corpoElse)

    def parse(self):
        statements = []
        while self.tokenAtual.tipo != TT_EOF:
            statements.append(self.statment())

        if not statements:
            return None

        return BlocoNode(statements)


nomeVariaveis = {}


def avaliador(Node):

    if isinstance(Node, BlocoNode):
        ultimoResultado = None
        for statement in Node.statements:
            ultimoResultado = avaliador(statement)
        return ultimoResultado

    if isinstance(Node, NumberNode):
        return Node.token.valor

    if isinstance(Node, VarAcessNode):
        nome = Node.token.valor

        if nome not in nomeVariaveis:
            posErro = Node.token.posInicio.copia()
            raise ErroExecucao(f"Variável '{nome}' não foi declarada antes.", posErro)

        return nomeVariaveis[nome]

    if isinstance(Node, VarAssignNode):
        nome = Node.token.valor
        valor = avaliador(Node.valorNode)
        nomeVariaveis[nome] = valor
        return valor

    if isinstance(Node, PrintNode):
        valor = avaliador(Node.valorNode)
        print(valor)
        return None

    if isinstance(Node, IfNode):
        cond = avaliador(Node.condicaoNode)

        truthy = not (cond is False or cond == 0 or cond == 0.0 or cond == "")
        #Avalia se é verdadeiro ou falso

        if truthy:
            return avaliador(Node.corpoNode)
        elif Node.elseNode is not None:
            return avaliador(Node.elseNode)
        return None

    if isinstance(Node, OpBinario):
        left = avaliador(Node.left)
        right = avaliador(Node.right)

        tipo = Node.operadorToken.tipo

        if tipo == TT_SUM:
            return left + right
        if tipo == TT_MINUS:
            return left - right
        if tipo == TT_DIV:
            if right == 0 or right == 0.0:
                posErro = Node.operadorToken.posInicio.copia()
                raise ErroExecucao("Divisão por zero.", posErro)
            return left / right
        if tipo == TT_MULT:
            return left * right
        
        
        if tipo == TT_MAIOR:
            return left > right
        if tipo == TT_MENOR:
            return left < right
        if tipo == TT_MAIOR_IGUAL:
            return left >= right
        if tipo == TT_MENOR_IGUAL:
            return left <= right
        if tipo == TT_DIFERENTE:
            return left != right

        raise ErroExecucao('Símbolo de expressão desconhecido')

    if Node is None:
        return None

    raise ErroExecucao(f'Nó desconhecido no avaliador: {type(Node)}')


def run(nomeArquivo, texto, reset_vars=True):
    global nomeVariaveis

    if reset_vars:
        nomeVariaveis = {}

    lexer = Lexer(nomeArquivo, texto)
    tokens, erro = lexer.makeToken()

    if erro is not None:
        return None, erro

    parser = Parser(tokens)
    try:
        arvOp = parser.parse()
    except ErroSintaxeInvalida as e:
        return None, e

    if arvOp is None:
        return None, None

    try:
        resultado = avaliador(arvOp)
        return resultado, None
    except ErroExecucao as e:
        return None, e
