class AnalisadorLexico:
    def __init__(self, fita, numero_da_linha=1):
        self.cabeca = 0  # Cabeça de leitura
        self.fita = fita  # Conteúdo a ser analisado
        self.numero_da_linha = numero_da_linha  # Número da linha do código sendo analisado
        self.tabela_de_simbolos = []  # Tabela de símbolos encontrada
        self.lexema = ""  # Lexema atual em construção
        self.estado_atual = "q0"  # Estado inicial
        self.keywords = [
            "variables", "methods", "constants", "class", "return", "empty", "main",
            "if", "then", "else", "while", "for", "read", "write", "integer", "float",
            "boolean", "string", "true", "false", "extends"
        ]

    def is_letter(self, char):
        return char.isalpha()

    def is_digit(self, char):
        return char.isdigit()

    def q0(self):
        """Estado inicial q0."""
        if self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if self.is_letter(char):
                self.estado_atual = "q1"
                self.lexema += char
            self.cabeca += 1
        else:
            self.estado_atual = "fim"

    def q1(self):
        """Estado q1 para acumular letras, dígitos ou underscore."""
        if self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if self.is_letter(char) or self.is_digit(char) or char == "_":
                self.lexema += char
                self.cabeca += 1
            else:
                # Verifica se é palavra-chave ou identificador
                if self.lexema in self.keywords:
                    self.tabela_de_simbolos.append((self.lexema, "keyword", self.numero_da_linha))
                else:
                    self.tabela_de_simbolos.append((self.lexema, "identifier", self.numero_da_linha))
                
                # Reseta o lexema e volta ao estado q0
                self.lexema = ""
                self.estado_atual = "q0"
        else:
            # Finaliza o último token se houver
            if self.lexema:
                if self.lexema in self.keywords:
                    self.tabela_de_simbolos.append((self.lexema, "keyword", self.numero_da_linha))
                else:
                    self.tabela_de_simbolos.append((self.lexema, "identifier", self.numero_da_linha))
            self.estado_atual = "fim"

    def analisar(self):
        """Função para iniciar a análise."""
        while self.estado_atual != "fim":
            if self.estado_atual == "q0":
                self.q0()
            elif self.estado_atual == "q1":
                self.q1()

        return self.tabela_de_simbolos

# Exemplo de uso
fita = "main main_principal2 var1 var2 class"
analisador = AnalisadorLexico(fita)
tokens = analisador.analisar()

for token in tokens:
    print(token)
