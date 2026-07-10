# Uso da biblioteca `pathlib`

Este projeto usa a biblioteca padrão `pathlib` para trabalhar com caminhos de
arquivos e pastas.

Como `pathlib` já acompanha o Python, não é necessário instalar nada.

## Importação

No começo de `src/main.py`, o projeto importa a classe `Path`:

```python
from pathlib import Path
```

- `pathlib` é o nome da biblioteca;
- `Path` é a classe usada para representar um caminho.

## Por que usar `Path`?

Um caminho informa onde uma pasta ou arquivo está localizado no computador.

Com `Path`, podemos:

- montar caminhos;
- verificar se um arquivo existe;
- abrir e ler arquivos;
- criar pastas;
- escrever arquivos.

Além disso, o mesmo código funciona melhor em sistemas que escrevem caminhos de
formas diferentes, como Windows, Linux e macOS.

## Encontrando a pasta do projeto

O programa possui esta linha:

```python
PASTA_PROJETO = Path(__file__).parent.parent
```

Vamos entender cada parte.

### `__file__`

`__file__` guarda o caminho do arquivo Python que está sendo executado. Neste
projeto, ele representa `src/main.py`.

### `Path(__file__)`

Transforma o caminho de `main.py` em um objeto `Path`.

### `.parent`

Representa a pasta que contém o caminho.

O primeiro `.parent` sai de `main.py` e chega à pasta `src`:

```text
stats-saude/src/main.py
            ^ pasta parent
```

O segundo `.parent` sai de `src` e chega à raiz do projeto:

```text
stats-saude/src
^ pasta parent
```

Assim, `PASTA_PROJETO` representa a pasta `stats-saude`.

## Montando caminhos com `/`

O operador `/` junta as partes de um caminho:

```python
ARQUIVO_CSV = PASTA_PROJETO / "data" / "08_saude.csv"
```

O resultado representa:

```text
stats-saude/data/08_saude.csv
```

O caminho do relatório é montado da mesma forma:

```python
ARQUIVO_RELATORIO = PASTA_PROJETO / "reports" / "relatorio_saude.txt"
```

Usar `/` dessa maneira não realiza uma divisão. Quando trabalhamos com um
objeto `Path`, ele serve para juntar pastas e nomes de arquivos.

## Verificando se o CSV existe

Antes de tentar ler os dados, o programa usa:

```python
if not ARQUIVO_CSV.exists():
    print(f"Arquivo nao encontrado: {ARQUIVO_CSV}")
    return
```

O método `.exists()` devolve:

- `True` quando o caminho existe;
- `False` quando o caminho não existe.

O `not` inverte o resultado. Portanto, o bloco é executado quando o CSV não é
encontrado.

## Abrindo o arquivo CSV

Na função `carregar_dados()`, o arquivo é aberto assim:

```python
with caminho.open(encoding="utf-8-sig") as arquivo:
    leitor = csv.DictReader(arquivo)
```

O método `.open()` abre o caminho para leitura. O `with` fecha o arquivo
automaticamente ao final do bloco.

O parâmetro `encoding="utf-8-sig"` informa como os caracteres do texto devem
ser interpretados.

## Criando a pasta do relatório

Antes de salvar o relatório, o programa garante que a pasta `reports` exista:

```python
ARQUIVO_RELATORIO.parent.mkdir(exist_ok=True)
```

Essa linha possui três partes importantes:

- `.parent` seleciona a pasta `reports`;
- `.mkdir()` cria essa pasta;
- `exist_ok=True` evita erro caso ela já exista.

## Escrevendo o relatório

O relatório é salvo com:

```python
ARQUIVO_RELATORIO.write_text(
    "\n".join(linhas),
    encoding="utf-8",
)
```

O método `.write_text()` cria ou substitui o arquivo com o texto informado.

Neste exemplo:

- `"\n".join(linhas)` transforma a lista em um único texto;
- `encoding="utf-8"` define a codificação do arquivo salvo.

## Resumo dos recursos utilizados

| Recurso | Finalidade |
| --- | --- |
| `Path(__file__)` | Representar o caminho de `main.py` |
| `.parent` | Obter a pasta anterior |
| `/` | Juntar partes de um caminho |
| `.exists()` | Verificar se o caminho existe |
| `.open()` | Abrir um arquivo |
| `.mkdir()` | Criar uma pasta |
| `.write_text()` | Escrever texto em um arquivo |

## Exemplo simples

Este pequeno exemplo cria uma pasta e salva uma mensagem nela:

```python
from pathlib import Path

pasta = Path("exemplo")
pasta.mkdir(exist_ok=True)

arquivo = pasta / "mensagem.txt"
arquivo.write_text("Olá!", encoding="utf-8")

if arquivo.exists():
    print("O arquivo foi criado.")
```

Esse exemplo pratica os recursos para dashboard.
