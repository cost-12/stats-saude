# Stats Saude

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Interface](https://img.shields.io/badge/interface-terminal-lightgrey)
![Dependencias](https://img.shields.io/badge/dependencias-biblioteca%20padrao-brightgreen)
![Relatorio](https://img.shields.io/badge/relatorio-TXT-orange)
![License](https://img.shields.io/badge/license-GPLv3-blue)

Dashboard de saude executada totalmente pelo terminal. O projeto le um arquivo
CSV, transforma os registros em uma lista de dicionarios, calcula estatisticas
uteis e gera um relatorio TXT com informacoes relevantes sobre a base.

## Objetivo

O objetivo do projeto e facilitar a consulta e a analise de dados de saude sem
usar interface grafica ou bibliotecas externas.

A dashboard permite responder perguntas como:

- Quais municipios possuem menor disponibilidade de medicos por 10 mil habitantes?
- Quais municipios possuem maior quantidade de habitantes por UBS?
- Qual e a media de UBS, medicos, enfermeiros e populacao atendida?
- Qual municipio possui a maior populacao atendida?
- Quantos municipios estao em cada faixa de disponibilidade?
- Quais informacoes principais devem aparecer em um relatorio final?

## Recursos

- Leitura de CSV com `csv.DictReader`.
- Armazenamento dos dados em lista de dicionarios.
- Conversao automatica de numeros lidos do CSV.
- Menu unico via terminal.
- Consultas principais para o tema de saude.
- Estatisticas gerais: quantidade, soma, media, mediana, minimo e maximo.
- Distribuicao, frequencia e percentual por categoria.
- Rankings de municipios prioritarios.
- Descobertas textuais sobre os dados.
- Geracao de relatorio TXT estruturado.
- Codigo comentado para facilitar estudo por iniciantes.
- Documentacao complementar em Markdown.
- Sem dependencias externas.

## Tecnologias

O projeto usa apenas Python e bibliotecas padrao:

- `argparse`
- `csv`
- `collections`
- `datetime`
- `pathlib`
- `statistics`
- `textwrap`

## Estrutura do projeto

```text
stats-saude/
+-- data/
|   +-- 08_saude.csv
+-- docs/
|   +-- README.md
|   +-- USO.md
|   +-- FUNCOES.md
+-- reports/
|   +-- relatorio_saude.txt
+-- src/
|   +-- main.py
+-- LICENSE
+-- README.md
```

## Base de dados

O arquivo analisado fica em:

```text
data/08_saude.csv
```

Colunas originais da base:

| Coluna | Descricao |
| --- | --- |
| `municipio` | Nome do municipio |
| `ubs` | Quantidade de UBS |
| `medicos` | Quantidade de medicos |
| `enfermeiros` | Quantidade de enfermeiros |
| `populacao_atendida` | Populacao atendida no municipio |

Durante a execucao, o programa cria indicadores derivados:

| Indicador | Para que serve |
| --- | --- |
| `total_profissionais` | Soma de medicos e enfermeiros |
| `profissionais_por_ubs` | Media de profissionais por UBS |
| `medicos_por_10k` | Medicos por 10 mil habitantes |
| `enfermeiros_por_10k` | Enfermeiros por 10 mil habitantes |
| `profissionais_por_10k` | Profissionais por 10 mil habitantes |
| `habitantes_por_ubs` | Pressao populacional sobre cada UBS |
| `habitantes_por_medico` | Pressao populacional sobre cada medico |
| `habitantes_por_profissional` | Pressao populacional sobre a equipe |
| `faixa_populacao` | Grupo de porte populacional |
| `nivel_ubs` | Classificacao de disponibilidade de UBS |
| `nivel_medicos_10k` | Classificacao de disponibilidade medica |

## Como os dados ficam na memoria

Cada linha do CSV vira um dicionario Python. Todos os dicionarios ficam dentro
de uma lista.

Exemplo simplificado:

```python
[
    {
        "municipio": "Municipio_1",
        "ubs": 25,
        "medicos": 82,
        "enfermeiros": 148,
        "populacao_atendida": 188675,
        "total_profissionais": 230,
        "medicos_por_10k": 4.35,
    }
]
```

Esse formato facilita consultas, rankings e calculos estatisticos.

## Como executar

Na raiz do projeto, execute:

```powershell
py -3 src/main.py
```

Em ambientes onde `python` esteja configurado, tambem pode funcionar:

```powershell
python src/main.py
```

No ambiente em que o projeto foi validado, o comando usado foi `py -3`.

## Menu da dashboard

```text
1. Consultas
2. Estatisticas
3. Relatorio TXT
0. Sair
```

### Consultas

Mostra automaticamente consultas importantes para o problema:

- municipios com menor disponibilidade de medicos por 10 mil habitantes;
- municipios com maior numero de habitantes por UBS;
- municipios com maior populacao atendida;
- busca simples de municipio por nome.

### Estatisticas

Calcula e exibe:

- quantidade de registros;
- soma;
- media;
- mediana;
- minimo;
- maximo;
- distribuicao por categoria;
- frequencia por categoria;
- percentual por categoria;
- descobertas sobre os dados.

### Relatorio TXT

Gera ou atualiza:

```text
reports/relatorio_saude.txt
```

## Gerar relatorio sem abrir o menu

```powershell
py -3 src/main.py --relatorio
```

## Usar outro CSV

```powershell
py -3 src/main.py --csv caminho/do/arquivo.csv
```

Para gerar relatorio com outro CSV:

```powershell
py -3 src/main.py --csv caminho/do/arquivo.csv --relatorio
```

O CSV precisa possuir as colunas esperadas:

- `municipio`
- `ubs`
- `medicos`
- `enfermeiros`
- `populacao_atendida`

## Relatorio gerado

O relatorio TXT contem:

- cabecalho com data e base analisada;
- analise exploratoria dos dados;
- estatisticas gerais;
- distribuicao, frequencia e percentual;
- rankings de municipios;
- descobertas sobre os dados;
- fechamento do relatorio.

## Documentacao

Arquivos de apoio:

- [docs/README.md](docs/README.md): visao geral do projeto.
- [docs/USO.md](docs/USO.md): guia de execucao e uso do menu.
- [docs/FUNCOES.md](docs/FUNCOES.md): explicacao de constantes e funcoes.

## Validacao

Comandos usados para validar o projeto:

```powershell
py -3 -m py_compile src/main.py
py -3 src/main.py --relatorio
```

Para testar abertura e saida do menu:

```powershell
@("0") | py -3 src/main.py
```

## Observacao sobre os criterios

As classificacoes como `Alta disponibilidade`, `Disponibilidade media` e
`Baixa disponibilidade` sao criterios internos para facilitar a analise
exploratoria. Elas nao substituem parametros oficiais de saude publica.

## Licenca

Este projeto esta licenciado sob a GPLv3. Consulte o arquivo [LICENSE](LICENSE)
para mais detalhes.
