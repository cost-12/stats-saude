# Guia de Uso

Este guia mostra como executar a dashboard e usar o menu simplificado.

## Requisitos

- Ter Python instalado.
- No Windows deste ambiente, o comando validado foi `py -3`.
- Nao e necessario instalar bibliotecas externas.

O projeto usa apenas bibliotecas padrao do Python:

- `csv`
- `pathlib`
- `statistics`

O codigo usa principalmente `int`, listas, dicionarios, `for`, `if` e funcoes.
As secoes do arquivo possuem separadores visuais para facilitar a leitura.

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
3. Criar relatorio TXT
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
Buscar municipio por nome (enter para voltar): Goiania
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
- media, mediana, menor e maior valor.

Exemplos de indicadores derivados:

- `medicos_por_10k`
- `habitantes_por_ubs`
- `total_profissionais`

## Opcao 3: Relatorio TXT

Gera ou atualiza o arquivo:

```text
reports/relatorio_saude.txt
```

O relatorio contem um cabecalho, as medias gerais e os cinco municipios com
menos medicos por 10 mil habitantes.

O programa usa sempre o CSV padrao do projeto. Esse CSV deve ter as colunas
esperadas:

- `municipio`
- `ubs`
- `medicos`
- `enfermeiros`
- `populacao_atendida`
