# Funcoes do Programa

O arquivo `src/main.py` foi dividido em quatro blocos. As linhas compridas de
tracos ajudam o aluno a enxergar onde cada assunto comeca.

## 1. Leitura e preparacao

### `dividir(numero, divisor)`

Faz uma divisao. Se o divisor for zero, devolve `0` e evita um erro.

### `calcular_indicadores(municipio)`

Recebe o dicionario de um municipio e acrescenta somente tres calculos:

- total de profissionais;
- medicos por 10 mil habitantes;
- habitantes por UBS.

### `carregar_dados(caminho)`

Abre o CSV com `csv.DictReader`. Cada linha vira um dicionario e cada coluna
numerica e convertida com `int()`.

Todos os dicionarios sao guardados na lista `municipios`.

## 2. Funcoes de apoio

### `formatar_numero(numero)`

Prepara um numero para aparecer com duas casas decimais e virgula.

### `mostrar_tabela(municipios)`

Usa um laco `for` para imprimir os municipios em forma de tabela.

### `buscar_municipio(municipios, nome_procurado)`

Compara o texto digitado com o nome de cada municipio e cria uma lista com os
resultados encontrados.

### `criar_ranking(municipios, coluna, ordem_decrescente)`

Ordena a lista pela coluna escolhida e devolve os cinco primeiros municipios.

## 3. Opcoes do menu

### `mostrar_consultas(municipios)`

Mostra tres rankings e oferece uma busca pelo nome do municipio.

### `mostrar_estatisticas(municipios)`

Mostra soma, media, mediana, menor valor e maior valor de cada coluna numerica.

### `gerar_relatorio(municipios)`

Cria `reports/relatorio_saude.txt` com as medias e um ranking curto.

## 4. Inicio do programa

### `mostrar_menu(municipios)`

Mostra as opcoes dentro de um `while`. O laco termina quando a opcao e `0`.

### `main()`

Confere se o CSV existe, carrega os municipios e chama o menu.

O bloco abaixo inicia o programa quando executamos `src/main.py`:

```python
if __name__ == "__main__":
    main()
```

## Caminho percorrido pelos dados

```text
CSV -> carregar_dados() -> lista de municipios -> menu
                                              -> consultas
                                              -> estatisticas
                                              -> relatorio
```
