class AnalisadorLexico:
    def __init__(self, file_path, numero_da_linha=1):
        self.cabeca = 0  # Cabeça de leitura
        self.fita = ""  # Inicialmente vazia, será preenchida pelo conteúdo do arquivo
        self.numero_da_linha = numero_da_linha  # Número da linha do código sendo analisado
        self.tabela_de_tokens = []  # Tabela de símbolos encontrada
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
        self.operators = ['+', '-', '*', '/', '=', '>', '<', '!', '&', '|', '.', ';']
        self.comentarios = []  # Lista para armazenar os comentários encontrados
        self.processar_entrada(file_path)  # Lê o conteúdo do arquivo e armazena em fita



    def is_letter(self, char):
        return char.isalpha()

    def is_digit(self, char):
        return char.isdigit()

    def is_operator(self, char):
        """Verifica se o caractere é um operador."""
        return char in self.operators
        
    def processar_entrada(self, file_path):
        """Lê o arquivo e armazena o conteúdo na fita."""
        try:
            with open(file_path, 'r') as file:
                self.fita = file.read()
        except IOError as e:
            print(f"Erro ao ler o arquivo: {e}")
    
    def processar_saida(self, output_path='saida.txt'):
        """Gera um arquivo com a saída formatada das listas e dicionários."""
        with open(output_path, 'w') as file:
            # Especificar largura mínima para cada coluna
            largura_lexema = 15
            largura_classe = 12
            largura_linha = 8
            
            # Escrever tabela de tokens
            file.write("****Tabela de Tokens****\n")
            file.write(f"{'linha'.ljust(largura_linha)} | {'classe'.ljust(largura_classe)} | {'lexema'.ljust(largura_lexema)} \n")
            for token in self.tabela_de_tokens:
                lexema, classe, linha = token
                file.write(f"{str(linha).ljust(largura_linha)} | {classe.ljust(largura_classe)} | {str(lexema).ljust(largura_lexema)}\n")
            file.write("\n")
            
            # Escrever identificadores
            file.write("****Identificadores****\n")
            file.write(f"{'Id'.ljust(5)} | {'lexema'.ljust(largura_lexema)}\n")
            for identificador, numero in self.identificadores.items():
                file.write(f"{str(numero).ljust(5)} | {str(identificador).ljust(largura_lexema)}\n")
            file.write("\n")
            
            # Escrever erros
            file.write("****Erros****\n")
            file.write("Descrição do erro\n")
            for erro in self.erros:
                file.write(f"{erro}\n")
            file.write("\n")
            
            # Escrever comentários
            file.write("****Comentários****\n")
            file.write(f"{'Tipo'.ljust(10)} | {'Linha inicial'.ljust(15)} | {'Conteúdo'}\n")
            for comentario, tipo, linha in self.comentarios:
                file.write(f"{str(tipo).ljust(10)} | {str(linha).ljust(15)} | {comentario}\n")
            file.write("\n")

        print(f"Saída gerada no arquivo: {output_path}")

    def avancar_cabeca(self):
        """Avança a cabeça de leitura e atualiza o número da linha, se necessário."""
        if self.cabeca < len(self.fita) - 1:
            if self.fita[self.cabeca] == '\n':
                self.numero_da_linha += 1
            self.cabeca += 1

            if self.fita[self.cabeca] != '\n' and self.fita[self.cabeca] != '\t' and not (32 <= ord(self.fita[self.cabeca]) and ord(self.fita[self.cabeca]) <= 126):
                self.erros.append(
                    (self.fita[self.cabeca], "Erro: Caractere não permitido", self.numero_da_linha))
                
                self.cabeca += 1

        else:
            self.cabeca += 1
            self.q0

    def q0(self):
        """Estado inicial q0."""
        if self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if self.is_letter(char):
                self.lexema += char
                self.avancar_cabeca()
                self.q1()  # Transição direta para q1
            elif self.is_operator(char):
                self.lexema += char
                self.avancar_cabeca()
                self.q2()  # Transição direta para q2 
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
            elif self.is_digit(char):  # Início de um número
                self.lexema += char
                self.avancar_cabeca()
                self.q7()  # Transição direta para q7
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
                    self.tabela_de_tokens.append((self.lexema, "keyword", self.numero_da_linha))
                else:
                    # Verifica se o identificador já existe na tabela de identificadores
                    if self.lexema not in self.identificadores:
                        self.contador_identificadores += 1
                        self.identificadores[self.lexema] = self.contador_identificadores
                    
                    # Adiciona o número associado ao identificador na tabela de símbolos
                    numero_associado = self.identificadores[self.lexema]
                    self.tabela_de_tokens.append((numero_associado, "identifier", self.numero_da_linha))

                # Reseta o lexema e volta ao estado q0
                self.lexema = ""
                self.q0()
        else:
            # Finaliza o último token se houver
            if self.lexema:
                if self.lexema in self.keywords:
                    self.tabela_de_tokens.append((self.lexema, "keyword", self.numero_da_linha))
                else:
                    # Verifica se o identificador já existe na tabela de identificadores
                    if self.lexema not in self.identificadores:
                        self.contador_identificadores += 1
                        self.identificadores[self.lexema] = self.contador_identificadores
                    
                    # Adiciona o número associado ao identificador na tabela de símbolos
                    numero_associado = self.identificadores[self.lexema]
                    self.tabela_de_tokens.append((numero_associado, "identifier", self.numero_da_linha))

    def q2(self):
        """Estado q2 para tratar operadores e detectar comentários."""
        if self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if self.lexema == '/':  # Pode ser início de comentário
                if char == '/':  # Comentário de linha
                    self.lexema += char
                    self.tabela_de_tokens.append(
                        (self.lexema, "comment_start", self.numero_da_linha))  # Adiciona '//' na tabela de símbolos
                    self.lexema = ""
                    self.avancar_cabeca()
                    self.q6(tipo='linha')  # Vai para o estado q6 para processar o comentário de linha
                elif char == '*':  # Comentário de bloco
                    self.lexema += char
                    self.tabela_de_tokens.append(
                        (self.lexema, "comment_start", self.numero_da_linha))  # Adiciona '/*' na tabela de símbolos
                    self.lexema = ""
                    self.avancar_cabeca()
                    self.q6(tipo='bloco')  # Vai para o estado q6 para processar o comentário de bloco
                else:
                    self.tabela_de_tokens.append(
                        (self.lexema, "operator", self.numero_da_linha))
                    self.lexema = ""
                    self.q0()  # Volta para o estado inicial após tratar o operador
            elif char in ['+', '-', '*', '/', '=', '!', '>', '<', '&', '|']:
                if self.lexema + char in ['==', '!=', '>=', '<=', '&&', '||', '++', '--']:
                    self.lexema += char
                    self.avancar_cabeca()
                self.tabela_de_tokens.append(
                    (self.lexema, "operator", self.numero_da_linha))
                self.lexema = ""
                self.q0()  # Volta para o estado inicial após tratar o operador
            else:
                self.tabela_de_tokens.append(
                    (self.lexema, "operator", self.numero_da_linha))
                self.lexema = ""
                self.q0()  # Volta para o estado inicial após tratar o operador

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

            elif self.cabeca >= len(self.fita) - 1 and self.lexema:
                # Fim da fita e string não foi fechada
                self.erros.append(
                    (self.lexema, "Erro: String não fechada antes do fim da fita", linha_inicial))
                self.avancar_cabeca()

            elif 32 <= ord(char) <= 126 and char not in ('"', "'"): # adicionar char a char
                self.lexema += char
                self.avancar_cabeca()

            elif char == '"':  # Fim da string
                self.lexema += char
                self.avancar_cabeca()
                self.tabela_de_tokens.append(
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
                    self.tabela_de_tokens.append(
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

        elif self.cabeca >= len(self.fita):
            # Fim da fita e caractere não foi fechado
            self.erros.append(
                (self.lexema, "Erro: Caractere não fechado", self.numero_da_linha))
                  

    def q5(self):
        """Estado q5 simplificado para tratar delimitadores."""
        char = self.fita[self.cabeca - 1]  # Caractere já avançado na fita

        if char in self.delimiters or char in self.delimiters.values() or char in [';', ',']:
            self.tabela_de_tokens.append(
                (char, "delimiter", self.numero_da_linha))

        self.lexema = ""
        self.q0()  # Volta ao estado q0 para continuar a leitura

    def q6(self, tipo):
        """Estado q6 para processar o conteúdo de comentários."""
        if tipo == 'linha':
            comentario = ""
            while self.cabeca < len(self.fita):
                char = self.fita[self.cabeca]
                if char == '\n':  # Fim do comentário de linha
                    self.comentarios.append((comentario, "linha", self.numero_da_linha))
                    self.avancar_cabeca()
                    self.q0()  # Volta para o estado inicial após o comentário de linha
                    break
                else:
                    comentario += char
                    self.avancar_cabeca()
            else:
                # Se terminar o arquivo sem encontrar o fim do comentário
                self.comentarios.append((comentario, "linha", self.numero_da_linha))
                self.q0()

        elif tipo == 'bloco':
            comentario = ""
            linha_inicial = self.numero_da_linha  # Armazena a linha onde o bloco começou
            while self.cabeca < len(self.fita):
                char = self.fita[self.cabeca]
                if char == '*':  # Possível fechamento do bloco
                    self.avancar_cabeca()
                    if self.cabeca < len(self.fita) and self.fita[self.cabeca] == '/':
                        self.avancar_cabeca()
                        self.comentarios.append((comentario, "bloco", linha_inicial))
                        self.tabela_de_tokens.append(('*/', "comment_end", self.numero_da_linha))
                        self.q0()  # Volta para o estado inicial após o fechamento do bloco
                        break
                    else:
                        comentario += '*'
                else:
                    if char != '\n':
                        comentario += char
                    self.avancar_cabeca()
            else:
                # Se não encontrar o fechamento do bloco até o final do arquivo, gera um erro
                self.erros.append(
                    ("/*", "Erro: Bloco de comentário não fechado", linha_inicial))
                
                    
                self.q0()  # Volta para o estado inicial após emitir o erro

    def q7(self):
        """Estado q7 para tratar números."""
        has_dot = False  # Flag para verificar se já existe um ponto decimal
        while self.cabeca < len(self.fita):
            char = self.fita[self.cabeca]
            if self.is_digit(char):
                self.lexema += char
                self.avancar_cabeca()
            elif char == '.' and not has_dot:
                self.lexema += char
                has_dot = True  # Marca que um ponto decimal foi encontrado
                self.avancar_cabeca()
            else:
                # Se encontra qualquer outra coisa, encerra o número
                self.tabela_de_tokens.append((self.lexema, "number", self.numero_da_linha))
                self.lexema = ""
                self.q0()  # Volta para o estado inicial
                return

        # Se a fita terminar enquanto ainda estamos no estado q7, finalize o número
        if self.lexema:
            self.tabela_de_tokens.append((self.lexema, "number", self.numero_da_linha))
            self.lexema = ""

    def analisar(self):
        """Função para iniciar a análise."""
        self.q0()  # Começa no estado q0
        self.processar_saida('saida.txt')
        return self.tabela_de_tokens, self.identificadores, self.erros, self.comentarios


file_path = './entrada.txt'
analisador = AnalisadorLexico(file_path)
tokens, identificadores, erros, comentarios = analisador.analisar()

input()
