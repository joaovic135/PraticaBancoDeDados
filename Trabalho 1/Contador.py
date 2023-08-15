import sys

def ContadorDePalavras(documento):
    palavra_numero = {}
    
    with open(documento, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2:
                palavra = " ".join(parts[:-1])
                numero = int(parts[-1])
                
                if palavra in palavra_numero:
                    palavra_numero[palavra] += numero
                else:
                    palavra_numero[palavra] = numero
    
    palavras_ordenadas = sorted(palavra_numero, key=palavra_numero.get, reverse=True)
    
    for palavra in palavras_ordenadas[:10]:
        print(f'{palavra}: {palavra_numero[palavra]}')

    with open("histograma.txt", "w") as output_file:
      for palavra in palavras_ordenadas:
        output_file.write(f'{palavra}: {palavra_numero[palavra]}\n')


arquivo_path = 'part-00000'  
ContadorDePalavras(arquivo_path)
