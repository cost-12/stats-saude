# Guia de Uso

Este guia mostra como executar a dashboard e usar o menu simplificado.

## Requisitos

- Ter Python instalado.
- No Windows deste ambiente, o comando validado foi `py -3`.
- Nao e necessario instalar bibliotecas externas.

O projeto usa apenas bibliotecas padrao do Python:

- `argparse`
- `csv`
- `pathlib`
- `statistics`

O codigo foi mantido com lacos `for` explicitos e funcoes pequenas para ficar
mais facil de acompanhar por quem esta aprendendo Python.

## Executar a dashboard

Na pasta raiz do projeto, use:

```powershell
py -3 src/main.py
```

O programa carrega o CSV padrao:

```text
data/08_saude.csv
```

Depois disso, o menu principal aparece no terminal.

## Menu principal

O projeto possui apenas um menu:

```text
1. Consultas
2. Estatisticas
3. Relatorio TXT
0. Sair
```

## Opcao 1: Consultas

Mostra consultas uteis para o tema de saude.

Essa opcao exibe automaticamente:

- municipios com menor disponibilidade de medicos por 10 mil habitantes;
- municipios com maior numero de habitantes por UBS;
- municipios com maior populacao atendida.

Depois, o programa permite buscar um municipio pelo nome.

Exemplo:

```text
Buscar municipio por nome (enter para voltar): Municipio_10
```

Se voce apertar `Enter` sem digitar nada, a dashboard volta ao menu principal.

## Opcao 2: Estatisticas

Calcula e exibe informacoes uteis do dataset:

- quantidade de registros;
- soma;
- media;
- mediana;
- minimo;
- maximo;
- indicadores derivados de saude;
- distribuicao por categoria;
- frequencia por categoria;
- percentual por categoria;
- descobertas sobre os dados.

Exemplos de indicadores derivados:

- `medicos_por_10k`
- `enfermeiros_por_10k`
- `profissionais_por_10k`
- `habitantes_por_ubs`
- `habitantes_por_medico`

## Opcao 3: Relatorio TXT

Gera ou atualiza o arquivo:

```text
reports/relatorio_saude.txt
```

O relatorio contem:

- cabecalho;
- resumo da base;
- indicadores principais;
- distribuicoes;
- rankings importantes em Top 5;
- descobertas sobre os dados.

## Gerar relatorio sem abrir o menu

Use:

```powershell
py -3 src/main.py --relatorio
```

## Usar outro CSV

Tambem e possivel informar outro arquivo CSV:

```powershell
py -3 src/main.py --csv caminho/do/arquivo.csv
```

Para gerar relatorio com outro CSV:

```powershell
py -3 src/main.py --csv caminho/do/arquivo.csv --relatorio
```

O outro CSV deve ter as colunas esperadas pelo projeto:

- `municipio`
- `ubs`
- `medicos`
- `enfermeiros`
- `populacao_atendida`
