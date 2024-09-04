class AnalisadorLexico:
    def __init__(self, file_path, numero_da_linha=1):
        self.cabeca = 0  # Cabeça de leitura
        self.fita = ""  # Inicialmente vazia, será preenchida pelo conteúdo do arquivo
        self.numero_da_linha = numero_da_linha  # Número da linha do código sendo analisado
        self.tabela_de_simbolos = []  # Tabela de símbolos encontrada
        self.erros = []  # Lista de erros encontrados
        self.lexema = ""  # Lexema atual em construção
        self.identificadores = {}  # Dicionário para armazenar identificadores com números associados
        self.contador_identificadores = 1  # Contador para atribuir números aos identificadores
        self.keywords = [
            "variables", "methods", "constants", "class", "return", "empty", "main",
            "if", "then", "else", "while", "for", "read", "write", "integer", "float",
            "boolean", "string", "true", "false", "extends"
        ]
        self.delimiters = {'(': ')', '{': '}', '[': ']'}
        self.delimiter_stack = []  # Pilha para verificar correspondência de delimitadores
        
        self.ler_arquivo(file_path)  # Lê o conteúdo do arquivo e armazena em fita



    def is_letter(self, char):
        return char.isalpha()

    def is_digit(self, char):
        return char.isdigit()

    def ler_arquivo(self, file_path):
        """Lê o arquivo e armazena o conteúdo na fita."""
        try:
            with open(file_path, 'r') as file:
                self.fita = file.read()
        except IOError as e:
            print(f"Erro ao ler o arquivo: {e}")

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
            elif char == "'":  # Início de um caractere
                self.lexema += char
                self.avancar_cabeca()
                self.q4()  # Transição direta para q4
            elif char in self.delimiters or char in self.delimiters.values() or char in [';', ',']:
                self.lexema += char
                self.avancar_cabeca()
                self.q5()  # Transição direta para q5
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
                    # Verifica se o identificador já existe na tabela de identificadores
                    if self.lexema not in self.identificadores:
                        self.contador_identificadores += 1
                        self.identificadores[self.lexema] = self.contador_identificadores
                    
                    # Adiciona o número associado ao identificador na tabela de símbolos
                    numero_associado = self.identificadores[self.lexema]
                    self.tabela_de_simbolos.append((numero_associado, "identifier", self.numero_da_linha))

                # Reseta o lexema e volta ao estado q0
                self.lexema = ""
                self.q0()
        else:
            # Finaliza o último token se houver
            if self.lexema:
                if self.lexema in self.keywords:
                    self.tabela_de_simbolos.append((self.lexema, "keyword", self.numero_da_linha))
                else:
                    # Verifica se o identificador já existe na tabela de identificadores
                    if self.lexema not in self.identificadores:
                        self.contador_identificadores += 1
                        self.identificadores[self.lexema] = self.contador_identificadores
                    
                    # Adiciona o número associado ao identificador na tabela de símbolos
                    numero_associado = self.identificadores[self.lexema]
                    self.tabela_de_simbolos.append((numero_associado, "identifier", self.numero_da_linha))


    def q2(self):
        """Estado q2 vazio."""
        pass

    def q3(self):
        """Estado q3 para tratar strings."""
        linha_inicial = self.numero_da_linha  # Armazena a linha onde a string começou
        while self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if char == '\n':  # Verifica se a linha terminou
                self.erros.append(
                    (self.lexema, "Erro: String não fechada antes do fim da linha", linha_inicial))
                self.lexema = ""
                self.q0()  # Volta ao estado q0 após emitir o erro
                break
            elif 32 <= ord(char) <= 126 and char not in ('"', "'"):
                self.lexema += char
                self.avancar_cabeca()
            elif char == '"':  # Fim da string
                self.lexema += char
                self.avancar_cabeca()
                self.tabela_de_simbolos.append(
                    (self.lexema, "string", self.numero_da_linha))
                self.lexema = ""
                self.q0()  # Volta ao estado q0 após fechar a string
                break
            elif char == "'":  # Erro: Aspas simples dentro da string
                self.erros.append(
                    (self.lexema + char, "Erro: Aspas simples em string", self.numero_da_linha))
                self.lexema += char  # Continua adicionando ao lexema
                self.avancar_cabeca()
            else:
                self.erros.append(
                    (self.lexema, "Erro: String não fechada", self.numero_da_linha))
                self.lexema = ""
                break

        if self.cabeca >= len(self.fita) and self.lexema:
            # Fim da fita e string não foi fechada
            self.erros.append(
                (self.lexema, "Erro: String não fechada antes do fim da fita", linha_inicial))


    def q4(self):
        """Estado q4 para tratar caracteres."""
        if self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if char == '"':  # Erro: Aspas duplas dentro de um caractere
                self.erros.append(
                    (self.lexema + char, "Erro: Aspas duplas em caractere", self.numero_da_linha))
                self.lexema = ""
                self.avancar_cabeca()
                self.q0()  # Retorna ao estado q0 para continuar a análise
            elif 32 <= ord(char) <= 126 and char != "'":
                self.lexema += char
                self.avancar_cabeca()
                if self.cabeca < len(self.fita) and self.fita[self.cabeca] == "'":
                    self.lexema += "'"
                    self.avancar_cabeca()
                    self.tabela_de_simbolos.append(
                        (self.lexema, "char", self.numero_da_linha))
                    self.lexema = ""
                    self.q0()  # Volta ao estado q0 após fechar o caractere
                else:
                    self.erros.append(
                        (self.lexema, "Erro: Caractere não fechado", self.numero_da_linha))
                    self.lexema = ""
                    self.q0()  # Continua a análise no estado q0
            else:
                self.erros.append(
                    (self.lexema + char, "Erro: Caractere inválido", self.numero_da_linha))
                self.lexema = ""
                self.avancar_cabeca()
                self.q0()  # Retorna ao estado q0 para continuar a análise

        if self.cabeca >= len(self.fita):
            # Fim da fita e caractere não foi fechado
            self.erros.append(
                (self.lexema, "Erro: Caractere não fechado", self.numero_da_linha))

    def q5(self):
        """Estado q5 simplificado para tratar delimitadores."""
        char = self.fita[self.cabeca - 1]  # Caractere já avançado na fita

        if char in self.delimiters or char in self.delimiters.values() or char in [';', ',']:
            self.tabela_de_simbolos.append(
                (char, "delimiter", self.numero_da_linha))

        self.lexema = ""
        self.q0()  # Volta ao estado q0 para continuar a leitura

    def analisar(self):
        """Função para iniciar a análise."""
        self.q0()  # Começa no estado q0
        return self.tabela_de_simbolos, self.identificadores, self.erros


# Exemplo de uso
fita = '''
main { 
    print(b;
}
'''
file_path = './t1.txt'
analisador = AnalisadorLexico(file_path)
tokens, identificadores, erros = analisador.analisar()

print("Tokens:")
for token in tokens:
    print(token)

print("\nIdentificadores:")
for identificador, numero in identificadores.items():
    print(f"{numero}: {identificador}")

print("\nErros:")
for erro in erros:
    print(erro)
