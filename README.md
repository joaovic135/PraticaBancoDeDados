# Prática em Banco de Dados

Repositório com os trabalhos práticos da disciplina de **Prática em Banco de Dados**.

---

## Trabalho 1: Contagem de palavras com MapReduce

### O problema

Dado um texto grande, descobrir **quantas vezes cada palavra aparece** e **quais são as
mais frequentes**, usando o modelo de processamento distribuído **MapReduce** (Hadoop).

O texto escolhido foi *Shakespeare's Sonnets* (Project Gutenberg), com 3.029 linhas.
Ao dividir o texto por espaços aparecem dois obstáculos:

- **Pontuação colada às palavras:** `love`, `love,` e `love.` seriam contadas como três
  palavras diferentes.
- **Tokens que não são palavras:** números, hífens soltos e símbolos poluem o resultado.

### Como foi feito

A solução foi escrita em Python, no formato do **Hadoop Streaming**: cada script lê da
entrada padrão e escreve na saída padrão.

```
shakespeare.txt ─► mapper ─► sort (shuffle) ─► reducer ─► part-00000 ─► Contador.py ─► top 10 + histograma.txt
```

1. **Mapper** (`mapperv1.py` / `mapperv2.py`): lê o texto linha a linha, remove a
   pontuação `. , ? ! ( ) " ' $ #` com expressão regular e conta as palavras em um
   dicionário. Usa o padrão **in-mapper combining**: emite um único par
   `palavra<TAB>contagem` por palavra no final, em vez de `palavra<TAB>1` a cada
   ocorrência, o que reduz o tráfego até o reducer.
   - `mapperv1.py`: aceita qualquer termo que não fique vazio nem seja só `-`.
   - `mapperv2.py`: aceita **apenas termos formados só por letras**, descartando números
     e símbolos.
2. **Shuffle/sort**: o Hadoop (ou o `sort`, quando executado localmente) ordena os pares
   pela palavra, para que as ocorrências da mesma palavra cheguem juntas ao reducer.
3. **Reducer** (`reducerv1.py`): soma as contagens de cada palavra.
4. **Análise** (`Contador.py`): lê a saída `part-00000`, ordena as palavras por
   frequência, mostra o top 10 e grava todas em `histograma.txt`.

O desenvolvimento foi incremental, em 15 e 16 de agosto de 2023: primeiro o word count
básico, depois a limpeza da pontuação e o script de análise, e por fim a segunda versão
do mapper com o filtro de palavras.

### Resultado

Com o `mapperv2.py`, o texto completo produz:

| Métrica | Valor |
|---------|-------|
| Palavras contadas | **19.940** |
| Palavras distintas | **4.016** |
| Palavras que aparecem só uma vez | 2.348 (58% das distintas) |

**Top 10 palavras mais frequentes**

| # | Palavra | Ocorrências |
|---|---------|-------------|
| 1 | the | 514 |
| 2 | of | 457 |
| 3 | to | 405 |
| 4 | I | 344 |
| 5 | my | 341 |
| 6 | in | 339 |
| 7 | and | 317 |
| 8 | thy | 252 |
| 9 | that | 250 |
| 10 | And | 242 |

**Conclusões**

- O topo do ranking é dominado por *stopwords* (artigos, preposições e pronomes), como
  é típico em textos em inglês.
- Aparecem marcas do inglês arcaico dos sonetos: **thy** (252), **thou** (208) e
  **thee** (145).
- A primeira palavra de conteúdo é **love**, com 149 ocorrências (mais 10 como `Love`),
  o que condiz com o tema central dos sonetos.
- Como a contagem diferencia maiúsculas de minúsculas, `and` (317) e `And` (242)
  aparecem separadas (somadas seriam 559), assim como `the` (514) e `The` (90).
- O cabeçalho e a licença do Project Gutenberg também entram na contagem. Por isso
  `Project` aparece 83 vezes.
- O filtro do `mapperv2.py` eliminou 582 termos distintos (754 ocorrências) em relação ao
  `mapperv1.py`, que contava 4.598 termos distintos e 20.694 ocorrências.

Detalhes de cada script, a metodologia completa e os comandos de execução estão no
[README do Trabalho 1](./Trabalho%201/README.md).

---

## Estrutura do repositório

```
PraticaBancoDeDados/
├── README.md
└── Trabalho 1/
    ├── README.md          # Documentação detalhada do trabalho
    ├── mapperv1.py        # Mapper: remove pontuação básica
    ├── mapperv2.py        # Mapper: mantém apenas palavras só com letras
    ├── reducerv1.py       # Reducer: soma as contagens de cada palavra
    ├── Contador.py        # Gera o top 10 e o histograma a partir da saída do reducer
    └── shakespeare.txt    # Entrada: Shakespeare's Sonnets (Project Gutenberg)
```

## Requisitos

- Python 3.6 ou superior (os scripts usam f-strings e apenas a biblioteca padrão)
- Opcional: Apache Hadoop com Hadoop Streaming, para executar em um cluster

## Execução rápida (local)

```bash
cd "Trabalho 1"
cat shakespeare.txt | python3 mapperv2.py | sort | python3 reducerv1.py > part-00000
python3 Contador.py
```
