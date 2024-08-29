import re

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
            resultado.append(text[start:end + 2])  # Adiciona o comentário ao resultado
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

# Exemplo de uso
text = '''
Aqui está um comentário de bloco:
    /* Este é um comentário de bloco
E aqui está uma string com comentário: "Texto /*' não é um comentário */"
Mais um comentário de bloco:
    /* Outro comentário de bloco */
E uma linha de comentário: // Comentário de linha
'''

tokens, comentarios, texto_limpo = verificar_comentarios_bloco(text)
print("Tokens encontrados:")
print(tokens)
print("\nComentários encontrados:")
print(comentarios)
print("\nTexto limpo:")
print(texto_limpo)
