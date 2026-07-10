import csv
from pathlib import Path
from statistics import mean, median


# Caminhos dos arquivos por path
PASTA_PROJETO = Path(__file__).parent.parent
ARQUIVO_CSV = PASTA_PROJETO / "data" / "08_saude.csv"
ARQUIVO_RELATORIO = PASTA_PROJETO / "reports" / "relatorio_saude.txt"


COLUNAS_NUMERICAS = ["ubs", "medicos", "enfermeiros", "populacao_atendida"]

# Nomes mais faceis de entender quando as estatisticas aparecem na tela.
NOMES_COLUNAS = {
    "ubs": "UBS",
    "medicos": "medicos",
    "enfermeiros": "enfermeiros",
    "populacao_atendida": "pessoas atendidas",
}



# seção de leitura dos dados

def dividir(numero, divisor):
    ###Corrigi o erro da divisao quando o divisor e zero
    if divisor == 0:
        return 0
    return numero / divisor


def calcular_indicadores(municipio):
    ### Adiciona  calculadas ao dicionario do municipio

    populacao = municipio["populacao_atendida"]
    medicos = municipio["medicos"]
    enfermeiros = municipio["enfermeiros"]
    ubs = municipio["ubs"]

    municipio["total_profissionais"] = medicos + enfermeiros
    municipio["medicos_por_10k"] = dividir(medicos * 10_000, populacao)
    municipio["habitantes_por_ubs"] = dividir(populacao, ubs)


def carregar_dados(caminho):
    ### Leitor do CSV para devolver a lista de municipios
    municipios = []

    with caminho.open(encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            # O CSV guarda tudo como texto. Essas colunas precisam virar numeros
            for coluna in COLUNAS_NUMERICAS:
                linha[coluna] = int(linha[coluna])

            calcular_indicadores(linha)
            municipios.append(linha)

    return municipios



# funções bestas de apoio

def formatar_numero(numero):
    ###formatador com duas casas decimais e virgula
    texto = f"{numero:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def mostrar_tabela(municipios):
    ##Mostra a tabela curta com os municipios recebidos
    if len(municipios) == 0:
        print("Nenhum municipio encontrado.")
        return

    print(f"{'Municipio':<22} {'UBS':>5} {'Medicos':>8} {'Populacao':>12} {'Med./10 mil':>12}")
    print("-" * 63)

    for municipio in municipios:
        nome = municipio["municipio"][:22]
        indicador = formatar_numero(municipio["medicos_por_10k"])
        print(
            f"{nome:<22} "
            f"{municipio['ubs']:>5} "
            f"{municipio['medicos']:>8} "
            f"{municipio['populacao_atendida']:>12} "
            f"{indicador:>12}"
        )


def buscar_municipio(municipios, nome_procurado):
    ### buscador filtrado de miusculas e minusculas
    encontrados = []
    nome_procurado = nome_procurado.lower()

    for municipio in municipios:
        nome = municipio["municipio"].lower()
        if nome_procurado in nome:
            encontrados.append(municipio)

    return encontrados


def criar_ranking(municipios, coluna, ordem_decrescente):
    ##  A função de ordenação dos municipios por uma coluna e devolve os cinco primeiros
    ordenados = sorted(
        municipios,
        key=lambda municipio: municipio[coluna],
        reverse=ordem_decrescente,
    )
    return ordenados[:5]


# ----------------------------------------------------------------------------
# OPCOES DO MENU


def mostrar_consultas(municipios):
    ### A função de mostra o rankings, também permite buscar um municipio pelo nome

    print("\nMENOR NUMERO DE MEDICOS POR 10 MIL HABITANTES")
    ranking = criar_ranking(municipios, "medicos_por_10k", False)
    mostrar_tabela(ranking)

    print("\nMAIOR NUMERO DE HABITANTES POR UBS")
    ranking = criar_ranking(municipios, "habitantes_por_ubs", True)
    mostrar_tabela(ranking)

    print("\nMAIOR POPULACAO ATENDIDA")
    ranking = criar_ranking(municipios, "populacao_atendida", True)
    mostrar_tabela(ranking)

    busca = input("\nDigite um municipio ou pressione Enter para voltar: ").strip()
    if busca != "":
        encontrados = buscar_municipio(municipios, busca)
        print()
        mostrar_tabela(encontrados)


def mostrar_estatisticas(municipios):
    ###Calcula as estatisticas simples das colunas da tabela

    print("\n=== ESTATISTICAS ===")
    print(f"Municipios analisados: {len(municipios)}")

    for coluna in COLUNAS_NUMERICAS:
        valores = []

        for municipio in municipios:
            valores.append(municipio[coluna])

        nome = NOMES_COLUNAS[coluna]

        print(f"\n{nome.upper()}")
        print(f"  Total de {nome} na base: {formatar_numero(sum(valores))}")
        print(f"  Media de {nome} por municipio: {formatar_numero(mean(valores))}")
        print(f"  Mediana de {nome} por municipio: {formatar_numero(median(valores))}")
        print(f"  Menor quantidade em um municipio: {formatar_numero(min(valores))}")
        print(f"  Maior quantidade em um municipio: {formatar_numero(max(valores))}")


def gerar_relatorio(municipios):
    #### O criador do arquivo TXT com um resumo dos dados

    linhas = [
        "RELATORIO DA DASHBOARD DE SAUDE",
        "=" * 36,
        f"Municipios analisados: {len(municipios)}",
        "",
        "MEDIAS GERAIS",
    ]

    for coluna in COLUNAS_NUMERICAS:
        valores = []
        for municipio in municipios:
            valores.append(municipio[coluna])

        linhas.append(f"{coluna}: {formatar_numero(mean(valores))}")

    linhas.append("")
    linhas.append("CINCO MUNICIPIOS COM MENOS MEDICOS POR 10 MIL HABITANTES")

    ranking = criar_ranking(municipios, "medicos_por_10k", False)
    for posicao, municipio in enumerate(ranking, start=1):
        indicador = formatar_numero(municipio["medicos_por_10k"])
        linhas.append(f"{posicao}. {municipio['municipio']}: {indicador}")

    ARQUIVO_RELATORIO.parent.mkdir(exist_ok=True)
    ARQUIVO_RELATORIO.write_text("\n".join(linhas), encoding="utf-8")
    print(f"\nRelatorio criado em: {ARQUIVO_RELATORIO}")



# MENU
# -----------------------------------------------------------------------------

def mostrar_menu(municipios):

    while True:
        print("\n=== DASHBOARD DE SAUDE ===")
        print("1. Consultas")
        print("2. Estatísticas")
        print("3. Criar relatório TXT")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_consultas(municipios)
        elif opcao == "2":
            mostrar_estatisticas(municipios)
        elif opcao == "3":
            gerar_relatorio(municipios)
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida.")


def main():
    ### carregador dos dados para iniciar o dash
    if not ARQUIVO_CSV.exists():
        print(f"Arquivo não encontrado: {ARQUIVO_CSV}")
        return

    municipios = carregar_dados(ARQUIVO_CSV)
    print(f"Foram carregados {len(municipios)} municípios.")
    mostrar_menu(municipios)


if __name__ == "__main__":
    main()
