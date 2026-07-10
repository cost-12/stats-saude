# Stats Saude

Dashboard para análisa de dados de saúde, focado em
apresentar conceitos variáveis, listas, dicionários,
condições, laços e funções.

O projeto usa apenas bibliotecas: `csv`, `pathlib` e
`statistics`.

## O que o programa faz

- lê os municípios do arquivo CSV;
- converte textos para números com `int()`;
- calcula três indicadores de saúde;
- mostra rankings e busca por município;
- calcula estatísticas;
- cria um relatório TXT.

## Estrutura

```text
stats-saude/
+-- data/08_saude.csv
+-- docs/
|   +-- README.md
|   +-- USO.md
|   +-- FUNCOES.md
|   +-- CSV.md
+-- reports/
+-- src/main.py
+-- README.md
```

## Como executar

Na pasta do projeto, execute:

```powershell
py -3 src/main.py
```

Ou, se o comando estiver configurado no computador:

```powershell
python src/main.py
```

O menu possui quatro opções:

```text
1. Consultas
2. Estatisticas
3. Criar relatorio TXT
0. Sair
```

## Dados e indicadores

Cada linha do CSV vira um dicionário dentro de uma lista. As colunas originais
são `municipio`, `ubs`, `medicos`, `enfermeiros` e `populacao_atendida`.

O programa acrescenta somente estes indicadores:

- `total_profissionais`;
- `medicos_por_10k`;
- `habitantes_por_ubs`.

Os dados numéricos do CSV devem ser números inteiros, sem pontos ou vírgulas.
