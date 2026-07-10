# Uso da biblioteca `csv`

Este projeto usa a biblioteca padrao `csv` do Python para ler a base
`data/08_saude.csv`.

Como `csv` ja vem instalada com o Python, nao e necessario instalar nenhuma
dependencia externa.

## Onde ela aparece

A biblioteca e importada em `src/main.py`:

```python
import csv
```

Ela e usada dentro da funcao `carregar_dados(caminho)`.

## Por que usar `csv.DictReader`

O projeto usa:

```python
leitor = csv.DictReader(arquivo)
```

O `DictReader` le a primeira linha do CSV como cabecalho. Depois, cada nova
linha vira um dicionario.

Exemplo de cabecalho:

```text
municipio,ubs,medicos,enfermeiros,populacao_atendida
```

Exemplo de linha:

```text
Sao Paulo,25,82,148,188675
```

Depois da leitura com `DictReader`, essa linha fica parecida com:

```python
{
    "municipio": "Sao Paulo",
    "ubs": "25",
    "medicos": "82",
    "enfermeiros": "148",
    "populacao_atendida": "188675",
}
```

No CSV, os valores chegam como texto. Por isso o programa percorre as colunas
numericas e usa `int()` para transformar cada valor em numero inteiro.

## Fluxo da leitura

A funcao `carregar_dados()` segue esta ordem:

1. Abre o arquivo CSV.
2. Cria um leitor com `csv.DictReader`.
3. Percorre cada linha do arquivo.
4. Converte as colunas numericas com `int()`.
5. Adiciona tres indicadores com `calcular_indicadores()`.
6. Guarda o dicionario na lista `municipios`.

Trecho principal:

```python
with caminho.open(encoding="utf-8-sig") as arquivo:
    leitor = csv.DictReader(arquivo)
    for linha in leitor:
        for coluna in COLUNAS_NUMERICAS:
            linha[coluna] = int(linha[coluna])

        calcular_indicadores(linha)
        municipios.append(linha)
```

## Detalhes importantes

### `encoding="utf-8-sig"`

Esse formato ajuda a ler arquivos CSV salvos em UTF-8 com BOM. Isso evita que o
primeiro nome de coluna venha com caracteres escondidos.

## Formato esperado do CSV

Para funcionar corretamente, o arquivo precisa ter estas colunas:

- `municipio`
- `ubs`
- `medicos`
- `enfermeiros`
- `populacao_atendida`

O arquivo padrao do projeto e:

```text
data/08_saude.csv
```

As quatro colunas numericas devem conter inteiros sem separadores. Por exemplo,
use `188675`, e nao `188.675` ou `188,675`.

## Por que os dados viram lista de dicionarios

Depois da leitura, o programa trabalha com uma lista assim:

```python
[
    {
        "municipio": "Sao Paulo",
        "ubs": 25,
        "medicos": 82,
        "enfermeiros": 148,
        "populacao_atendida": 188675,
    }
]
```

Esse formato facilita:

- buscar municipio por nome;
- calcular estatisticas;
- montar rankings;
- gerar o relatorio TXT.
