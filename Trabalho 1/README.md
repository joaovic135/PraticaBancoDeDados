# Trabalho 1: Contagem de palavras com MapReduce

Implementação do clássico *word count* no modelo **MapReduce**, com scripts Python
compatíveis com o **Hadoop Streaming** (leem da entrada padrão e escrevem na saída padrão).
A entrada é o texto dos *Sonetos* de William Shakespeare, obtido no Project Gutenberg.

## Visão geral do fluxo

```
shakespeare.txt ──► mapper ──► sort (shuffle) ──► reducerv1.py ──► part-00000 ──► Contador.py ──► top 10 + histograma.txt
```

1. O **mapper** lê o texto linha a linha, limpa cada palavra e conta as ocorrências.
2. A etapa de **shuffle/sort** (feita pelo Hadoop ou pelo `sort` localmente) agrupa as linhas pela palavra.
3. O **reducer** soma as contagens de cada palavra.
4. O **Contador** lê a saída final, mostra as 10 palavras mais frequentes e grava o histograma completo.

## Arquivos

### `mapperv1.py`

Mapper com *in-mapper combining*: em vez de emitir `palavra\t1` para cada ocorrência,
acumula as contagens em um dicionário e emite um par por palavra só no final (`close()`),
o que reduz o volume de dados enviado ao reducer.

- Remove os caracteres `. , ? ! ( ) " ' $ #` de cada termo.
- Descarta termos vazios e o hífen isolado (`-`).
- Mantém números, palavras com hífen e outros símbolos (por exemplo `;` e `:`).

### `mapperv2.py`

Mesma estrutura do `mapperv1.py`, com um filtro mais rígido: depois da limpeza, só conta
termos formados **apenas por letras** (`^[a-zA-Z]+$`). Números, palavras com hífen ou
apóstrofo interno e termos com outra pontuação são descartados. É a versão recomendada
para obter um histograma "limpo".

> Nas duas versões a contagem diferencia maiúsculas de minúsculas: `Love` e `love` são
> contadas como palavras diferentes.

### `reducerv1.py`

Lê linhas no formato `palavra\tcontagem`, **já ordenadas pela palavra**, e soma as
contagens de cada palavra, emitindo `palavra\ttotal`. Como o mapper já faz a combinação
local, o reducer recebe poucos pares por palavra (um por mapper).

### `Contador.py`

Pós-processamento da saída do MapReduce:

- Lê o arquivo `part-00000` do diretório atual (nome padrão da saída do Hadoop).
- Soma as contagens por palavra (útil se houver palavras repetidas no arquivo).
- Imprime no terminal as **10 palavras mais frequentes**.
- Grava em `histograma.txt` todas as palavras em ordem decrescente de frequência,
  no formato `palavra: contagem`.

### `shakespeare.txt`

*Shakespeare's Sonnets* (Project Gutenberg EBook #1041). O arquivo inclui o cabeçalho e
a licença do Project Gutenberg, que também entram na contagem.

## Como executar

### Localmente (sem Hadoop)

Simule o MapReduce com um pipe; o `sort` faz o papel da etapa de shuffle.
Em Linux, macOS, WSL ou Git Bash, dentro da pasta `Trabalho 1`:

```bash
cat shakespeare.txt | python3 mapperv2.py | sort | python3 reducerv1.py > part-00000
python3 Contador.py
```

Para usar a primeira versão do mapper, troque `mapperv2.py` por `mapperv1.py`.

> O reducer depende de a entrada estar ordenada pela palavra. Sem o `sort`, a mesma
> palavra aparece em grupos separados e a contagem fica fragmentada.

### No Hadoop (Hadoop Streaming)

```bash
# Envia a entrada para o HDFS
hdfs dfs -mkdir -p /user/$USER/wordcount/input
hdfs dfs -put shakespeare.txt /user/$USER/wordcount/input/

# Executa o job
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files mapperv2.py,reducerv1.py \
  -mapper "python3 mapperv2.py" \
  -reducer "python3 reducerv1.py" \
  -input /user/$USER/wordcount/input \
  -output /user/$USER/wordcount/output

# Traz o resultado e gera o ranking/histograma
hdfs dfs -get /user/$USER/wordcount/output/part-00000 .
python3 Contador.py
```

O diretório de saída não pode existir antes da execução; apague-o com
`hdfs dfs -rm -r /user/$USER/wordcount/output` se for rodar de novo.

## Saídas

| Arquivo | Gerado por | Conteúdo |
|---------|------------|----------|
| `part-00000` | reducer (Hadoop ou pipe local) | `palavra<TAB>total`, uma palavra por linha, ordenado pela palavra |
| `histograma.txt` | `Contador.py` | `palavra: total`, da mais para a menos frequente |
