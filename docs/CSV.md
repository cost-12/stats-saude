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

Ela e usada dentro da funcao `carregar_dados(caminho_csv)`.

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

No CSV, os valores chegam como texto. Por isso o projeto chama
`converter_valor()` para transformar numeros em `int` ou `float`.

## Fluxo da leitura

A funcao `carregar_dados()` segue esta ordem:

1. Abre o arquivo CSV.
2. Cria um leitor com `csv.DictReader`.
3. Percorre cada linha do arquivo.
4. Cria um dicionario chamado `registro`.
5. Converte cada valor com `converter_valor()`.
6. Adiciona indicadores com `adicionar_indicadores()`.
7. Guarda o registro na lista `registros_municipios`.

Trecho principal:

```python
with caminho_csv.open("r", encoding="utf-8-sig", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)
    for linha_csv in leitor:
        registro = {}
        for nome_coluna_csv, valor_csv in linha_csv.items():
            registro[nome_coluna_csv.strip()] = converter_valor(valor_csv)
        adicionar_indicadores(registro)
        registros_municipios.append(registro)
```

## Detalhes importantes

### `encoding="utf-8-sig"`

Esse formato ajuda a ler arquivos CSV salvos em UTF-8 com BOM. Isso evita que o
primeiro nome de coluna venha com caracteres escondidos.

### `newline=""`

Esse parametro e recomendado pela documentacao do Python ao trabalhar com
arquivos CSV. Ele ajuda a evitar problemas de quebra de linha em sistemas
diferentes, como Windows e Linux.

### `nome_coluna_csv.strip()`

O `strip()` remove espacos extras no nome da coluna.

Exemplo:

```python
" municipio ".strip()
```

Resultado:

```python
"municipio"
```

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
