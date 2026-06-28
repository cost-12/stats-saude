# Dashboard de Saude

Este projeto e uma dashboard simples feita em Python, sem interface grafica.
Ela le a base `data/08_saude.csv`, transforma cada linha em um dicionario e
guarda todos os registros em uma lista.

O objetivo e permitir consultas e analises uteis sobre dados de saude usando
apenas o terminal.

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
    +-- main.py
```

## Arquivos principais

- `src/main.py`: codigo principal da dashboard.
- `data/08_saude.csv`: base de dados analisada.
- `reports/relatorio_saude.txt`: relatorio gerado pela dashboard.
- `docs/USO.md`: explica como executar e usar o menu.
- `docs/FUNCOES.md`: explica para que serve cada funcao do codigo.

## Dados utilizados

A base possui as seguintes colunas originais:

- `municipio`: nome do municipio.
- `ubs`: quantidade de UBS.
- `medicos`: quantidade de medicos.
- `enfermeiros`: quantidade de enfermeiros.
- `populacao_atendida`: populacao atendida no municipio.

Durante a execucao, o programa cria novas colunas calculadas, como:

- `total_profissionais`
- `profissionais_por_ubs`
- `medicos_por_10k`
- `enfermeiros_por_10k`
- `profissionais_por_10k`
- `habitantes_por_ubs`
- `habitantes_por_medico`
- `habitantes_por_profissional`
- `faixa_populacao`
- `nivel_ubs`
- `nivel_medicos_10k`

## Como os dados ficam na memoria

O programa usa uma lista de dicionarios. Cada dicionario representa uma linha do
CSV.

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

Esse formato facilita buscas por municipio, rankings e calculos estatisticos.

## O que a dashboard faz

- Carrega dados do CSV.
- Converte numeros automaticamente.
- Calcula indicadores de saude.
- Exibe estatisticas gerais.
- Mostra distribuicoes, frequencias e percentuais.
- Gera rankings com municipios prioritarios para analise.
- Permite consultas por municipio e por prioridades de atendimento.
- Mostra descobertas sobre os dados.
- Gera um arquivo TXT estruturado com os principais resultados.

## Observacao importante

As classificacoes como `Alta disponibilidade`, `Disponibilidade media` e
`Baixa disponibilidade` sao criterios internos para facilitar a analise
exploratoria. Elas nao substituem parametros oficiais de saude publica.
