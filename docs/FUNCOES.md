# Referencia das Funcoes

Este arquivo explica, de forma simples, para que serve cada funcao de
`src/main.py`.

## Fluxo geral

O programa segue esta ordem:

1. `main()` le os argumentos do terminal.
2. `carregar_dados()` abre o CSV.
3. Cada linha do CSV vira um dicionario.
4. `adicionar_indicadores()` cria informacoes calculadas.
5. `menu_principal()` mostra o menu unico com consultas, estatisticas e relatorio.

## Constantes

### `BASE_DIR`

Guarda o caminho da pasta raiz do projeto.

### `CSV_PADRAO`

Guarda o caminho padrao do CSV: `data/08_saude.csv`.

### `RELATORIO_PADRAO`

Guarda o caminho padrao do relatorio: `reports/relatorio_saude.txt`.

### `CAMPOS_BASE`

Lista os campos originais que recebem estatisticas principais:

- `ubs`
- `medicos`
- `enfermeiros`
- `populacao_atendida`

### `CAMPOS_INDICADORES`

Lista os campos calculados pelo programa, como `medicos_por_10k` e
`habitantes_por_ubs`.

### `CAMPOS_TABELA`

Define quais colunas aparecem na tabela padrao do terminal.

### `CAMPOS_CATEGORICOS_ANALISE`

Define as categorias usadas nas distribuicoes:

- `faixa_populacao`
- `nivel_ubs`
- `nivel_medicos_10k`

### `RANKINGS_RELATORIO`

Define quais rankings aparecem automaticamente no relatorio TXT.

## Conversao e calculos basicos

### `converter_valor(valor)`

Recebe um valor lido do CSV.

Tenta converter esse valor para numero. Se conseguir, retorna `int` ou `float`.
Se nao conseguir, retorna o texto original.

### `dividir(numerador, denominador)`

Faz uma divisao.

Se o denominador for zero, vazio ou nulo, retorna `0` para evitar erro.

### `percentual(parte, total)`

Calcula o percentual que uma parte representa de um total.

### `valor_formatado(valor)`

Formata numeros para exibicao no padrao brasileiro.

Exemplos:

- `1500` vira `1.500`
- `12.5` vira `12,50`

## Categorias e indicadores de saude

### `categorizar_populacao(populacao)`

Classifica a populacao atendida em faixas:

- ate 100 mil
- 100 mil a 199 mil
- 200 mil a 299 mil
- 300 mil ou mais

### `categorizar_ubs(habitantes_por_ubs)`

Classifica a disponibilidade de UBS conforme a quantidade de habitantes por
unidade.

### `categorizar_medicos(medicos_por_10k)`

Classifica a disponibilidade medica usando a quantidade de medicos por 10 mil
habitantes.

### `adicionar_indicadores(registro)`

Recebe um dicionario com os dados de um municipio e adiciona novos campos
calculados.

Exemplos de campos adicionados:

- `total_profissionais`
- `medicos_por_10k`
- `habitantes_por_ubs`
- `faixa_populacao`
- `nivel_ubs`
- `nivel_medicos_10k`

## Leitura dos dados

### `carregar_dados(caminho_csv)`

Abre o arquivo CSV e le todas as linhas.

Para cada linha:

- cria um dicionario;
- converte valores numericos;
- adiciona indicadores calculados;
- adiciona o dicionario na lista `dados`.

No final, retorna uma lista de dicionarios.

## Estatisticas e organizacao dos dados

### `valores_numericos(dados, campo)`

Recebe a lista de registros e o nome de uma coluna.

Retorna apenas os valores numericos dessa coluna.

### `estatisticas_coluna(dados, campo)`

Calcula estatisticas de uma coluna numerica:

- quantidade;
- soma;
- media;
- mediana;
- minimo;
- maximo.

Retorna um dicionario com esses resultados.

### `colunas_numericas(dados)`

Verifica quais colunas possuem valores numericos.

E usada na analise exploratoria do relatorio para listar intervalos das colunas numericas.

### `frequencia(dados, campo)`

Conta quantas vezes cada categoria aparece em uma coluna.

Tambem calcula o percentual de cada categoria.

### `ranking(dados, campo, reverso=True, limite=10)`

Ordena os registros por uma coluna.

Quando `reverso=True`, mostra os maiores valores primeiro.

Quando `reverso=False`, mostra os menores valores primeiro.

### `agrupar_media(dados, categoria, campo)`

Agrupa os dados por uma categoria e calcula a media de um campo numerico.

Exemplo:

- agrupar por `faixa_populacao`;
- calcular a media de `medicos_por_10k`.

## Tabelas no terminal

### `texto_tabela(registros, campos=None, limite=20)`

Monta uma tabela em formato de texto.

Ela nao imprime sozinha. Apenas retorna o texto pronto.

### `imprimir_tabela(registros, campos=None, limite=20)`

Chama `texto_tabela()` e imprime o resultado no terminal.

## Consultas

### `buscar_municipios_por_nome(dados, termo)`

Procura municipios cujo nome contem o termo digitado.

Retorna uma lista de registros encontrados.

### `mostrar_municipios_prioritarios(dados)`

Mostra consultas prontas para localizar municipios que merecem atencao:

- menor disponibilidade de medicos por 10 mil habitantes;
- maior numero de habitantes por UBS;
- maior populacao atendida.

### `mostrar_consultas(dados)`

Executa a opcao `Consultas` do menu principal.

Ela mostra os municipios prioritarios e permite uma busca simples por nome.

## Estatisticas no terminal

### `mostrar_estatisticas_gerais(dados)`

Mostra no terminal:

- quantidade de registros;
- soma;
- media;
- mediana;
- minimo;
- maximo;
- indicadores derivados.

### `mostrar_distribuicoes(dados)`

Mostra frequencia e percentual das categorias da analise exploratoria.

### `gerar_descobertas(dados)`

Cria frases com informacoes relevantes sobre a base.

Exemplos:

- municipio com maior populacao atendida;
- media de UBS por municipio;
- percentual de municipios com baixa disponibilidade medica.

### `mostrar_descobertas(dados)`

Imprime no terminal as frases criadas por `gerar_descobertas()`.

### `mostrar_estatisticas(dados)`

Executa a opcao `Estatisticas` do menu principal.

Ela chama:

- `mostrar_estatisticas_gerais()`;
- `mostrar_distribuicoes()`;
- `mostrar_descobertas()`.

## Relatorio TXT

### `linhas_analise_exploratoria(dados)`

Cria uma lista de linhas de texto com a Analise Exploratoria de Dados.

Ela e usada no relatorio.

### `linhas_estatisticas(dados)`

Cria as linhas de texto da secao de estatisticas do relatorio.

### `linhas_distribuicao(dados)`

Cria as linhas de texto da secao de distribuicao, frequencia e percentual.

### `linhas_rankings(dados)`

Cria as linhas de texto da secao de rankings do relatorio.

### `gerar_relatorio(dados, caminho_saida, caminho_csv)`

Gera o arquivo TXT final.

Ele junta:

- cabecalho;
- analise exploratoria dos dados;
- estatisticas;
- distribuicoes;
- rankings;
- descobertas sobre os dados.

## Entrada do programa

### `menu_principal(dados, caminho_csv)`

Controla o menu unico da dashboard.

Opcoes disponiveis:

- `Consultas`;
- `Estatisticas`;
- `Relatorio TXT`.

### `parse_args()`

Le argumentos passados pelo terminal.

Argumentos aceitos:

- `--csv`
- `--relatorio`

### `main()`

E a funcao principal do programa.

Ela:

- le argumentos do terminal;
- verifica se o CSV existe;
- carrega os dados;
- gera relatorio direto ou abre o menu principal.

### `if __name__ == "__main__":`

Esse bloco garante que `main()` seja chamada quando o arquivo `main.py` for
executado diretamente pelo terminal.
