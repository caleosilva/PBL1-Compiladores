class AnalisadorLexico:
    def __init__(self, fita, numero_da_linha=1):
        self.cabeca = 0  # Cabeça de leitura
        self.fita = fita  # Conteúdo a ser analisado
        self.numero_da_linha = numero_da_linha  # Número da linha do código sendo analisado
        self.tabela_de_simbolos = []  # Tabela de símbolos encontrada
        self.erros = []  # Lista de erros encontrados
        self.lexema = ""  # Lexema atual em construção
        self.keywords = [
            "variables", "methods", "constants", "class", "return", "empty", "main",
            "if", "then", "else", "while", "for", "read", "write", "integer", "float",
            "boolean", "string", "true", "false", "extends"
        ]

    def is_letter(self, char):
        return char.isalpha()

    def is_digit(self, char):
        return char.isdigit()

    def avancar_cabeca(self):
        """Avança a cabeça de leitura e atualiza o número da linha, se necessário."""
        if self.cabeca < len(self.fita):
            if self.fita[self.cabeca] == '\n':
                self.numero_da_linha += 1
            self.cabeca += 1

    def q0(self):
        """Estado inicial q0."""
        if self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if self.is_letter(char):
                self.lexema += char
                self.avancar_cabeca()
                self.q1()  # Transição direta para q1
            elif char == '"':  # Início de uma string
                self.lexema += char
                self.avancar_cabeca()
                self.q3()  # Transição direta para q3
            else:
                self.avancar_cabeca()
                self.q0()  # Continua no estado q0 para ler o próximo caractere

    def q1(self):
        """Estado q1 para acumular letras, dígitos ou underscore."""
        if self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if self.is_letter(char) or self.is_digit(char) or char == "_":
                self.lexema += char
                self.avancar_cabeca()
                self.q1()  # Continua no estado q1 até encontrar um caractere inválido
            else:
                # Verifica se é palavra-chave ou identificador
                if self.lexema in self.keywords:
                    self.tabela_de_simbolos.append((self.lexema, "keyword", self.numero_da_linha))
                else:
                    self.tabela_de_simbolos.append((self.lexema, "identifier", self.numero_da_linha))
                
                # Reseta o lexema e volta ao estado q0
                self.lexema = ""
                self.q0()
        else:
            # Finaliza o último token se houver
            if self.lexema:
                if self.lexema in self.keywords:
                    self.tabela_de_simbolos.append((self.lexema, "keyword", self.numero_da_linha))
                else:
                    self.tabela_de_simbolos.append((self.lexema, "identifier", self.numero_da_linha))

    def q2(self):
        """Estado q2 vazio."""
        pass

    def q3(self):
        """Estado q3 para tratar strings."""
        while self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if 32 <= ord(char) <= 126 and char not in ('"', "'"):
                self.lexema += char
                self.avancar_cabeca()
            elif char == '"':  # Fim da string
                self.lexema += char
                self.avancar_cabeca()
                self.tabela_de_simbolos.append((self.lexema, "string", self.numero_da_linha))
                self.lexema = ""
                self.q0()  # Volta ao estado q0 após fechar a string
                break
            elif char == "'":  # Erro: Aspas simples dentro da string
                self.erros.append((self.lexema + char, "Erro: Aspas simples em string", self.numero_da_linha))
                self.lexema += char  # Continua adicionando ao lexema
                self.avancar_cabeca()
            else:
                self.erros.append((self.lexema, "Erro: String não fechada", self.numero_da_linha))
                self.lexema = ""
                break

        if self.cabeca >= len(self.fita) and self.lexema:
            # Fim da fita e string não foi fechada
            self.erros.append((self.lexema, "Erro: String não fechada", self.numero_da_linha))

    def analisar(self):
        """Função para iniciar a análise."""
        self.q0()  # Começa no estado q0
        return self.tabela_de_simbolos, self.erros

# Exemplo de uso
fita = '''
main "hello world" 'invalido' "string' sem fechar
'''
analisador = AnalisadorLexico(fita)
tokens, erros = analisador.analisar()

print("Tokens:")
for token in tokens:
    print(token)

print("\nErros:")
for erro in erros:
    print(erro)
