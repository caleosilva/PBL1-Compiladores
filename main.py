import re

def verificar_delimitadores(text):
    # Padrão para encontrar delimitadores (parênteses, colchetes e chaves)
    delimiter_pattern = re.compile(r'[()\[\]{}]')
    
    # Encontrar todos os delimitadores no texto
    tokens = delimiter_pattern.findall(text)
    
    # Função para verificar a correspondência dos delimitadores
    def verificar(tokens):
        pilha = []
        correspondencia = {')': '(', '}': '{', ']': '['}
        erros = []
        
        for token in tokens:
            if token in '({[':
                pilha.append(token)
            elif token in correspondencia:
                if not pilha or pilha[-1] != correspondencia[token]:
                    erros.append(token)
                else:
                    pilha.pop()
        
        if pilha:
            for token in pilha:
                erros.append(token)

        return erros

    # Verificar erros de delimitadores
    erros = verificar(tokens)
    
    # Remover delimitadores do texto
    texto_sem_delimitadores = delimiter_pattern.sub(' ', text)
    
    return tokens, texto_sem_delimitadores, erros

def verificar_comentarios_linha(text):
    tokens_encontrados = []
    comentarios_encontrados = []
    
    in_string = False
    i = 0
    resultado = []
    while i < len(text):
        if text[i] == '"':
            in_string = not in_string
            resultado.append(text[i])
        elif not in_string and text[i:i+2] == '//':
            start = i
            end = text.find('\n', i)
            if end == -1:
                end = len(text)
            tokens_encontrados.append('//')  # Adiciona o token encontrado
            comentarios_encontrados.append(text[start:end])  # Adiciona o comentário encontrado
            i = end
            continue
        resultado.append(text[i])
        i += 1
    
    # Cria o texto limpo removendo os comentários
    texto_limpo = ''.join(resultado)
    
    return tokens_encontrados, comentarios_encontrados, texto_limpo

# TÁ COM PROBLEMAS:
def verificar_comentarios_bloco(text):
    tokens_encontrados = []
    comentarios_encontrados = []
    resultado = []

    # Padrão para encontrar comentários de bloco
    block_comment_pattern = re.compile(r'/\*.*?\*/', re.DOTALL)
    in_string = False
    i = 0

    while i < len(text):
        if text[i] == '"':
            in_string = not in_string
            resultado.append(text[i])
            i += 1
            continue

        if not in_string and text[i:i+2] == '/*':
            start = i
            end = text.find('*/', i + 2)
            if end == -1:
                end = len(text)
            comentario = text[start:end + 2]
            tokens_encontrados.append('/*')  # Adiciona o token de início do comentário
            tokens_encontrados.append('*/')  # Adiciona o token de fim do comentário
            comentarios_encontrados.append(comentario)  # Adiciona o comentário encontrado
            i = end + 2
            continue

        resultado.append(text[i])
        i += 1

    texto_sem_comentarios = ''.join(resultado)

    # Função para verificar erros de delimitadores de bloco
    def verificar_delimitadores_bloco(text):
        stack = []
        erros = []

        i = 0
        while i < len(text):
            if text[i:i+2] == '/*':
                if not in_string:
                    stack.append(i)
                i += 2
            elif text[i:i+2] == '*/':
                if stack:
                    stack.pop()
                else:
                    erros.append(f"Fechamento de comentário '*/' inesperado na posição {i}.")
                i += 2
            else:
                i += 1

        while stack:
            start = stack.pop()
            erros.append(f"Início de comentário '/*' não fechado na posição {start}.")

        return erros

    erros = verificar_delimitadores_bloco(text)

    if erros:
        print("Erros encontrados:")
        for erro in erros:
            print(erro)

    return tokens_encontrados, comentarios_encontrados, texto_sem_comentarios


def ler_txt(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text


# Exemplo de chamada
if __name__ == '__main__':
    file_path = './t1.txt'
    texto = ler_txt(file_path)

    tokens_delimitadores, texto_sem_delimitadores, erros_delimitadores = verificar_delimitadores(texto)
    tokens_comentarios_linha, comentarios_encontrados, texto_sem_linha = verificar_comentarios_linha(texto_sem_delimitadores)
    tokens_comentarios_bloco, comentarios_bloco, texto_sem_bloco = verificar_comentarios_bloco(texto_sem_linha)

    print("=== Resultados da Verificação de Delimitadores ===")
    print("Tokens de Delimitadores Encontrados:")
    print(tokens_delimitadores)
    if erros_delimitadores:
        print("\nErros de Delimitadores Encontrados:")
        for erro in erros_delimitadores:
            print(erro)
    else:
        print("\nNenhum erro de delimitadores encontrado.")

    print("\n=== Resultados da Verificação de Comentários de Linha ===")
    print("Tokens de Comentários de Linha Encontrados:")
    print(tokens_comentarios_linha)
    print("\nComentários de Linha Encontrados:")
    print(comentarios_encontrados)

    print("\n=== Resultados da Verificação de Comentários de Bloco ===")
    print("Tokens de Comentários de Bloco Encontrados:")
    print(tokens_comentarios_bloco)
    print("\nComentários de Bloco Encontrados:")
    print(comentarios_bloco)

