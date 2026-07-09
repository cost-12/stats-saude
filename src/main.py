"""Dashboard de saude via terminal.

O programa le um CSV, guarda os registros em uma lista de dicionarios,
calcula estatisticas, permite consultas pelo menu e gera um relatorio TXT.
Foi escrito apenas com bibliotecas padrao do Python para facilitar o estudo.
"""
# from import foi usado pois permite importar apenas as funções necessárias de um módulo, sem poluir o namespace com vários arquivos.
import argparse
import csv
from datetime import datetime
from pathlib import Path
from statistics import mean, median


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PADRAO = BASE_DIR / "data" / "08_saude.csv"
RELATORIO_PADRAO = BASE_DIR / "reports" / "relatorio_saude.txt"

# Campos originais do arquivo CSV.
CAMPOS_BASE = ["ubs", "medicos", "enfermeiros", "populacao_atendida"]

# Campos calculados pelo programa a partir dos dados originais.
CAMPOS_INDICADORES = [
    "total_profissionais",
    "profissionais_por_ubs",
    "medicos_por_10k",
    "enfermeiros_por_10k",
    "profissionais_por_10k",
    "habitantes_por_ubs",
    "habitantes_por_medico",
    "habitantes_por_profissional",
]

# Campos usados na exibicao padrao de tabelas.
CAMPOS_TABELA = [
    "municipio",
    "ubs",
    "medicos",
    "enfermeiros",
    "populacao_atendida",
    "medicos_por_10k",
    "habitantes_por_ubs",
    "faixa_populacao",
]
CAMPOS_CATEGORICOS_ANALISE = ["faixa_populacao", "nivel_ubs", "nivel_medicos_10k"]

RANKINGS_RELATORIO = [
    ("Top 10 maiores populacoes atendidas", "populacao_atendida", True),
    ("Top 10 menores medicos por 10 mil habitantes", "medicos_por_10k", False),
    ("Top 10 maiores habitantes por UBS", "habitantes_por_ubs", True),
    ("Top 10 maiores equipes de saude", "total_profissionais", True),
]


def converter_valor(valor):
    """Converte um valor lido do CSV para int, float ou texto."""
    if valor is None:
        return ""

    texto = valor.strip()
    if texto == "":
        return ""

    # O CSV pode vir com formatos diferentes: "1.500", "10,5" ou "10.5".
    # Este bloco normaliza o texto antes de tentar converter para float.
    if "," in texto and "." in texto:
        texto_numerico = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto_numerico = texto.replace(",", ".")
    elif texto.count(".") == 1 and len(texto.rsplit(".", 1)[1]) != 3:
        texto_numerico = texto
    else:
        texto_numerico = texto.replace(".", "")
    try:
        numero = float(texto_numerico)
    except ValueError:
        return texto

    if numero.is_integer():
        return int(numero)
    return numero


def dividir(numerador, denominador):
    """Divide dois valores e evita erro quando o denominador e zero."""
    if denominador in (0, "", None):
        return 0
    return numerador / denominador


def categorizar_populacao(populacao):
    """Classifica um municipio por faixa de populacao atendida."""
    if populacao < 100_000:
        return "Ate 100 mil"
    if populacao < 200_000:
        return "100 mil a 199 mil"
    if populacao < 300_000:
        return "200 mil a 299 mil"
    return "300 mil ou mais"


def categorizar_ubs(habitantes_por_ubs):
    """Classifica a disponibilidade de UBS pela relacao habitantes por UBS."""
    if habitantes_por_ubs <= 10_000:
        return "Alta disponibilidade"
    if habitantes_por_ubs <= 20_000:
        return "Disponibilidade media"
    return "Baixa disponibilidade"


def categorizar_medicos(medicos_por_10k):
    """Classifica a disponibilidade medica por 10 mil habitantes."""
    if medicos_por_10k >= 4:
        return "Alta disponibilidade"
    if medicos_por_10k >= 2:
        return "Disponibilidade media"
    return "Baixa disponibilidade"


def adicionar_indicadores(registro):
    """Inclui no registro os indicadores calculados usados pela dashboard."""
    ubs = registro.get("ubs", 0)
    medicos = registro.get("medicos", 0)
    enfermeiros = registro.get("enfermeiros", 0)
    populacao = registro.get("populacao_atendida", 0)
    total_profissionais = medicos + enfermeiros

    # Indicadores absolutos e proporcionais facilitam comparacoes entre municipios.
    registro["total_profissionais"] = total_profissionais
    registro["profissionais_por_ubs"] = dividir(total_profissionais, ubs)
    registro["medicos_por_10k"] = dividir(medicos * 10_000, populacao)
    registro["enfermeiros_por_10k"] = dividir(enfermeiros * 10_000, populacao)
    registro["profissionais_por_10k"] = dividir(total_profissionais * 10_000, populacao)
    registro["habitantes_por_ubs"] = dividir(populacao, ubs)
    registro["habitantes_por_medico"] = dividir(populacao, medicos)
    registro["habitantes_por_profissional"] = dividir(populacao, total_profissionais)

    # Categorias transformam numeros continuos em grupos faceis de consultar.
    registro["faixa_populacao"] = categorizar_populacao(populacao)
    registro["nivel_ubs"] = categorizar_ubs(registro["habitantes_por_ubs"])
    registro["nivel_medicos_10k"] = categorizar_medicos(registro["medicos_por_10k"])


def carregar_dados(caminho_csv):
    """Le o CSV e devolve uma lista de dicionarios com indicadores extras."""
    dados = []
    with caminho_csv.open("r", encoding="utf-8-sig", newline="") as arquivo:
        # DictReader usa a primeira linha do CSV como nome das chaves do dicionario.
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            registro = {}
            for chave, valor in linha.items():
                # strip remove espacos do nome da coluna; converter_valor prepara os dados.
                registro[chave.strip()] = converter_valor(valor)
            adicionar_indicadores(registro)
            dados.append(registro)
    return dados


def valor_formatado(valor):
    """Formata numeros no padrao brasileiro para mostrar ao usuario."""
    if isinstance(valor, float):
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if isinstance(valor, int):
        return f"{valor:,}".replace(",", ".")
    return str(valor)


def percentual(parte, total):
    """Calcula qual percentual uma parte representa do total."""
    if total == 0:
        return 0
    return (parte / total) * 100


def valores_numericos(dados, campo):
    """Pega apenas os valores numericos de uma coluna."""
    valores = []
    for registro in dados:
        valor = registro.get(campo)
        if isinstance(valor, (int, float)):
            valores.append(valor)
    return valores


def estatisticas_coluna(dados, campo):
    """Calcula soma, media, mediana, minimo e maximo de uma coluna."""
    valores = valores_numericos(dados, campo)
    if not valores:
        return None

    return {
        "quantidade": len(valores),
        "soma": sum(valores),
        "media": mean(valores),
        "mediana": median(valores),
        "minimo": min(valores),
        "maximo": max(valores),
    }


def colunas_numericas(dados):
    """Descobre quais colunas possuem pelo menos um valor numerico."""
    if not dados:
        return []

    colunas = []
    for campo in dados[0]:
        encontrou_numero = False
        for registro in dados:
            if isinstance(registro.get(campo), (int, float)):
                encontrou_numero = True
                break

        if encontrou_numero:
            colunas.append(campo)
    return colunas


def frequencia(dados, campo):
    """Conta frequencia e percentual de cada categoria em uma coluna."""
    contador = {}
    for registro in dados:
        categoria = registro.get(campo, "Nao informado")
        contador[categoria] = contador.get(categoria, 0) + 1

    total = len(dados)
    itens = []
    for categoria, qtd in contador.items():
        item = {
            "categoria": categoria,
            "frequencia": qtd,
            "percentual": percentual(qtd, total),
        }
        itens.append(item)

    return sorted(itens, key=pegar_frequencia, reverse=True)


def pegar_frequencia(item):
    """Retorna a frequencia de um item para ajudar na ordenacao."""
    return item["frequencia"]


def ranking(dados, campo, reverso=True, limite=10):
    """Ordena os registros por um campo e retorna os primeiros colocados."""
    def pegar_valor(registro):
        return registro.get(campo, 0)

    dados_ordenados = sorted(dados, key=pegar_valor, reverse=reverso)
    return dados_ordenados[:limite]


def agrupar_media(dados, categoria, campo):
    """Agrupa registros por categoria e calcula a media de um campo numerico."""
    grupos = {}
    for registro in dados:
        valor = registro.get(campo)
        if isinstance(valor, (int, float)):
            nome_grupo = registro.get(categoria, "Nao informado")
            if nome_grupo not in grupos:
                grupos[nome_grupo] = []
            grupos[nome_grupo].append(valor)

    medias = []
    for nome_grupo, valores in grupos.items():
        medias.append((nome_grupo, mean(valores), len(valores)))
    return sorted(medias, key=pegar_media_do_grupo, reverse=True)


def pegar_media_do_grupo(item):
    """Retorna a media guardada na tupla criada por agrupar_media."""
    return item[1]


def cortar_texto(texto, limite=28):
    """Corta textos muito longos para nao quebrar a tabela."""
    texto = str(texto)
    if len(texto) <= limite:
        return texto
    return texto[: limite - 3] + "..."


def texto_tabela(registros, campos=None, limite=20):
    """Monta uma tabela em texto para exibir no terminal ou no relatorio."""
    if not registros:
        return "Nenhum registro encontrado."

    campos = campos or CAMPOS_TABELA
    registros_exibidos = registros[:limite]
    linhas = []

    # Primeiro os valores sao formatados como texto para calcular a largura das colunas.
    for registro in registros_exibidos:
        linha = {}
        for campo in campos:
            valor = valor_formatado(registro.get(campo, ""))
            linha[campo] = cortar_texto(valor)
        linhas.append(linha)

    # A largura de cada coluna respeita o maior texto encontrado, com limite de 28.
    larguras = {}
    for campo in campos:
        maior_largura = len(campo)
        for linha in linhas:
            largura_texto = len(str(linha[campo]))
            if largura_texto > maior_largura:
                maior_largura = largura_texto
        larguras[campo] = min(28, maior_largura)

    # Cabecalho, separador e corpo sao montados separadamente para formar a tabela final.
    partes_cabecalho = []
    partes_separador = []
    for campo in campos:
        partes_cabecalho.append(campo.ljust(larguras[campo]))
        partes_separador.append("-" * larguras[campo])

    cabecalho = " | ".join(partes_cabecalho)
    separador = "-+-".join(partes_separador)

    corpo = []
    for linha in linhas:
        partes_linha = []
        for campo in campos:
            partes_linha.append(str(linha[campo]).ljust(larguras[campo]))
        corpo.append(" | ".join(partes_linha))

    rodape = ""
    if len(registros) > limite:
        rodape = f"\nMostrando {limite} de {len(registros)} registros."

    tabela = [cabecalho, separador]
    tabela.extend(corpo)
    return "\n".join(tabela) + rodape


def imprimir_tabela(registros, campos=None, limite=20):
    """Mostra no terminal uma tabela gerada por texto_tabela."""
    print(texto_tabela(registros, campos, limite))


def mostrar_estatisticas_gerais(dados):
    """Exibe estatisticas gerais e indicadores derivados no terminal."""
    print("\n=== Estatisticas Gerais ===")
    print(f"Quantidade de registros: {len(dados)}")

    for campo in CAMPOS_BASE:
        stats = estatisticas_coluna(dados, campo)
        if not stats:
            continue

        print(f"\n{campo}")
        print(f"  Soma:    {valor_formatado(stats['soma'])}")
        print(f"  Media:   {valor_formatado(stats['media'])}")
        print(f"  Mediana: {valor_formatado(stats['mediana'])}")
        print(f"  Minimo:  {valor_formatado(stats['minimo'])}")
        print(f"  Maximo:  {valor_formatado(stats['maximo'])}")

    print("\nIndicadores de saude derivados")
    for campo in CAMPOS_INDICADORES:
        stats = estatisticas_coluna(dados, campo)
        if stats:
            print(f"  {campo}: media {valor_formatado(stats['media'])}")


def mostrar_distribuicoes(dados):
    """Exibe distribuicao, frequencia e percentual das categorias da analise."""
    print("\n=== Distribuicao, frequencia e percentual ===")

    for campo in CAMPOS_CATEGORICOS_ANALISE:
        print(f"\n{campo}")
        print("Categoria                    | Frequencia | Percentual")
        print("-----------------------------+------------+-----------")
        for item in frequencia(dados, campo):
            print(
                f"{item['categoria']:<28} | "
                f"{item['frequencia']:>10} | "
                f"{valor_formatado(item['percentual']):>9}%"
            )


def buscar_municipios_por_nome(dados, termo):
    """Retorna municipios que possuem o termo informado no nome."""
    termo = termo.strip().lower()
    encontrados = []
    for registro in dados:
        municipio = str(registro.get("municipio", "")).lower()
        if termo in municipio:
            encontrados.append(registro)
    return encontrados


def mostrar_municipios_prioritarios(dados):
    """Mostra rankings que ajudam a localizar municipios com maior atencao."""
    print("\n=== Municipios que merecem atencao ===")

    print("\nMenor disponibilidade de medicos por 10 mil habitantes")
    imprimir_tabela(
        ranking(dados, "medicos_por_10k", reverso=False),
        campos=["municipio", "medicos", "populacao_atendida", "medicos_por_10k"],
        limite=10,
    )

    print("\nMaior numero de habitantes por UBS")
    imprimir_tabela(
        ranking(dados, "habitantes_por_ubs", reverso=True),
        campos=["municipio", "ubs", "populacao_atendida", "habitantes_por_ubs"],
        limite=10,
    )

    print("\nMaior populacao atendida")
    imprimir_tabela(
        ranking(dados, "populacao_atendida", reverso=True),
        campos=["municipio", "populacao_atendida", "ubs", "total_profissionais"],
        limite=10,
    )


def mostrar_consultas(dados):
    """Mostra consultas principais sem abrir um segundo menu."""
    print("\n=== Consultas ===")
    print(f"Total de registros disponiveis para consulta: {len(dados)}")

    mostrar_municipios_prioritarios(dados)

    termo = input("\nBuscar municipio por nome (enter para voltar): ").strip()
    if not termo:
        return

    encontrados = buscar_municipios_por_nome(dados, termo)
    print(f"\nRegistros encontrados: {len(encontrados)}")
    imprimir_tabela(encontrados, limite=30)


def linhas_analise_exploratoria(dados):
    """Cria as linhas de texto da analise exploratoria da base."""
    linhas = []
    linhas.append("=== Analise exploratoria dos dados ===")
    linhas.append(f"Quantidade de registros: {len(dados)}")
    linhas.append(f"Quantidade de colunas: {len(dados[0]) if dados else 0}")
    linhas.append("")

    if not dados:
        return linhas

    # Compara a lista de municipios com um set para descobrir nomes duplicados.
    municipios = []
    for registro in dados:
        municipios.append(registro.get("municipio"))
    repetidos = len(municipios) - len(set(municipios))
    linhas.append(f"Municipios repetidos: {repetidos}")
    linhas.append("")

    linhas.append("Valores ausentes por coluna:")
    for campo in dados[0]:
        # Considera vazio quando o valor e string vazia ou None.
        ausentes = 0
        for registro in dados:
            if registro.get(campo) in ("", None):
                ausentes += 1
        linhas.append(f"- {campo}: {ausentes}")

    linhas.append("")
    linhas.append("Colunas numericas e intervalos:")
    for campo in colunas_numericas(dados):
        # Reaproveita apenas os valores numericos para evitar erro em min, max e media.
        valores = valores_numericos(dados, campo)
        linhas.append(
            f"- {campo}: minimo {valor_formatado(min(valores))}, "
            f"maximo {valor_formatado(max(valores))}, "
            f"media {valor_formatado(mean(valores))}"
        )

    linhas.append("")
    linhas.append("Filtros recomendados para a dashboard:")
    linhas.append("- municipio: busca textual por nome.")
    linhas.append("- faixa_populacao: compara municipios por porte de atendimento.")
    linhas.append("- nivel_ubs: identifica pressao sobre a estrutura de UBS.")
    linhas.append("- nivel_medicos_10k: identifica disponibilidade medica relativa.")
    linhas.append("- habitantes_por_ubs e medicos_por_10k: bons campos para ranking.")

    return linhas


def gerar_descobertas(dados):
    """Gera frases com informacoes relevantes encontradas na base."""
    if not dados:
        return ["Nao ha dados carregados."]

    # Calcula os principais extremos e medias uma vez para montar as frases finais.
    total = len(dados)
    total_populacao = 0
    baixa_medicos = 0
    baixa_ubs = 0

    for registro in dados:
        total_populacao += registro["populacao_atendida"]
        if registro["nivel_medicos_10k"] == "Baixa disponibilidade":
            baixa_medicos += 1
        if registro["nivel_ubs"] == "Baixa disponibilidade":
            baixa_ubs += 1

    maior_populacao = ranking(dados, "populacao_atendida")[0]
    maior_equipe = ranking(dados, "total_profissionais")[0]
    menor_medicos = ranking(dados, "medicos_por_10k", reverso=False)[0]
    maior_pressao_ubs = ranking(dados, "habitantes_por_ubs")[0]
    media_ubs = mean(valores_numericos(dados, "ubs"))
    media_medicos_10k = mean(valores_numericos(dados, "medicos_por_10k"))
    faixa_mais_frequente = frequencia(dados, "faixa_populacao")[0]
    melhor_faixa_medicos = agrupar_media(dados, "faixa_populacao", "medicos_por_10k")[0]

    # A funcao devolve textos prontos para uso no terminal e no relatorio.
    descobertas = []
    descobertas.append(
        f"A base possui {total} municipios e soma {valor_formatado(total_populacao)} pessoas atendidas."
    )
    descobertas.append(f"A media geral e de {valor_formatado(media_ubs)} UBS por municipio.")
    descobertas.append(
        f"A media de medicos por 10 mil habitantes e {valor_formatado(media_medicos_10k)}."
    )
    descobertas.append(
        f"{valor_formatado(percentual(baixa_medicos, total))}% dos municipios "
        "estao em baixa disponibilidade medica pela classificacao interna."
    )
    descobertas.append(
        f"{valor_formatado(percentual(baixa_ubs, total))}% dos municipios "
        "tem baixa disponibilidade de UBS pela relacao habitantes por unidade."
    )
    descobertas.append(
        f"O municipio com maior populacao atendida e {maior_populacao['municipio']} "
        f"({valor_formatado(maior_populacao['populacao_atendida'])} pessoas)."
    )
    descobertas.append(
        f"O municipio com maior equipe de saude e {maior_equipe['municipio']} "
        f"({valor_formatado(maior_equipe['total_profissionais'])} profissionais)."
    )
    descobertas.append(
        f"O menor indicador de medicos por 10 mil habitantes aparece em "
        f"{menor_medicos['municipio']} ({valor_formatado(menor_medicos['medicos_por_10k'])})."
    )
    descobertas.append(
        f"A maior pressao sobre UBS aparece em {maior_pressao_ubs['municipio']}, "
        f"com {valor_formatado(maior_pressao_ubs['habitantes_por_ubs'])} habitantes por UBS."
    )
    descobertas.append(
        f"A faixa de populacao mais frequente e '{faixa_mais_frequente['categoria']}', "
        f"com {faixa_mais_frequente['frequencia']} municipios "
        f"({valor_formatado(faixa_mais_frequente['percentual'])}%)."
    )
    descobertas.append(
        f"A faixa '{melhor_faixa_medicos[0]}' possui a maior media de medicos por 10 mil "
        f"habitantes ({valor_formatado(melhor_faixa_medicos[1])})."
    )
    return descobertas


def mostrar_descobertas(dados):
    """Mostra no terminal as descobertas geradas pela analise."""
    print("\n=== Descobertas sobre os dados ===")
    for descoberta in gerar_descobertas(dados):
        print(f"- {descoberta}")


def mostrar_estatisticas(dados):
    """Mostra um bloco unico com estatisticas, distribuicoes e descobertas."""
    mostrar_estatisticas_gerais(dados)
    mostrar_distribuicoes(dados)
    mostrar_descobertas(dados)


def linhas_estatisticas(dados):
    """Cria as linhas de texto da secao de estatisticas do relatorio."""
    linhas = []
    linhas.append("=== Estatisticas Gerais ===")
    linhas.append(f"Quantidade de registros: {len(dados)}")

    for campo in CAMPOS_BASE:
        stats = estatisticas_coluna(dados, campo)
        if not stats:
            continue
        linhas.append("")
        linhas.append(campo)
        linhas.append(f"- Soma: {valor_formatado(stats['soma'])}")
        linhas.append(f"- Media: {valor_formatado(stats['media'])}")
        linhas.append(f"- Mediana: {valor_formatado(stats['mediana'])}")
        linhas.append(f"- Minimo: {valor_formatado(stats['minimo'])}")
        linhas.append(f"- Maximo: {valor_formatado(stats['maximo'])}")

    linhas.append("")
    linhas.append("Indicadores derivados")
    for campo in CAMPOS_INDICADORES:
        stats = estatisticas_coluna(dados, campo)
        if stats:
            linhas.append(
                f"- {campo}: media {valor_formatado(stats['media'])}, "
                f"minimo {valor_formatado(stats['minimo'])}, "
                f"maximo {valor_formatado(stats['maximo'])}"
            )

    return linhas


def linhas_distribuicao(dados):
    """Cria as linhas de texto com frequencias e percentuais do relatorio."""
    linhas = ["=== Distribuicao, frequencia e percentual ==="]
    for campo in CAMPOS_CATEGORICOS_ANALISE:
        linhas.append("")
        linhas.append(campo)
        for item in frequencia(dados, campo):
            linhas.append(
                f"- {item['categoria']}: {item['frequencia']} "
                f"({valor_formatado(item['percentual'])}%)"
            )
    return linhas


def linhas_rankings(dados):
    """Cria as linhas de texto com os rankings do relatorio."""
    linhas = ["=== Ranking ==="]

    for titulo, campo, reverso in RANKINGS_RELATORIO:
        linhas.append("")
        linhas.append(titulo)
        for posicao, registro in enumerate(ranking(dados, campo, reverso=reverso), start=1):
            linhas.append(
                f"{posicao:02d}. {registro['municipio']} - "
                f"{campo}: {valor_formatado(registro[campo])}"
            )

    return linhas


def gerar_relatorio(dados, caminho_saida, caminho_csv):
    """Gera o arquivo TXT final reunindo analise, estatisticas e rankings."""
    # Garante que a pasta reports exista antes de tentar salvar o TXT.
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    linhas = []
    linhas.append("=" * 72)
    linhas.append("RELATORIO DA DASHBOARD DE SAUDE")
    linhas.append("=" * 72)
    linhas.append(f"Gerado em: {agora}")
    linhas.append(f"Base analisada: {caminho_csv}")
    linhas.append("")
    linhas.append("Observacao: classificacoes de disponibilidade sao operacionais para analise exploratoria")
    linhas.append("e nao substituem parametros oficiais de saude publica.")
    linhas.append("")

    linhas.extend(linhas_analise_exploratoria(dados))
    linhas.append("")
    linhas.extend(linhas_estatisticas(dados))
    linhas.append("")
    linhas.extend(linhas_distribuicao(dados))
    linhas.append("")
    linhas.extend(linhas_rankings(dados))
    linhas.append("")

    linhas.append("=== Descobertas sobre os dados ===")
    for descoberta in gerar_descobertas(dados):
        linhas.append(f"- {descoberta}")

    linhas.append("")
    linhas.append("=" * 72)
    linhas.append("FIM DO RELATORIO")
    linhas.append("=" * 72)

    caminho_saida.write_text("\n".join(linhas), encoding="utf-8")
    return caminho_saida


def menu_principal(dados, caminho_csv):
    """Controla o menu principal da dashboard no terminal."""
    while True:
        print("\n" + "=" * 50)
        print("DASHBOARD DE SAUDE - TERMINAL")
        print("=" * 50)
        print("1. Consultas")
        print("2. Estatisticas")
        print("3. Relatorio TXT")
        print("0. Sair")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            mostrar_consultas(dados)
        elif opcao == "2":
            mostrar_estatisticas(dados)
        elif opcao == "3":
            caminho = gerar_relatorio(dados, RELATORIO_PADRAO, caminho_csv)
            print(f"Relatorio gerado em: {caminho}")
        elif opcao == "0":
            print("Encerrando dashboard.")
            break
        else:
            print("Opcao invalida. Tente novamente.")


def parse_args():
    """Le argumentos de linha de comando, como --csv e --relatorio."""
    parser = argparse.ArgumentParser(description="Dashboard terminal para dados de saude.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=CSV_PADRAO,
        help="Caminho do arquivo CSV. Padrao: data/08_saude.csv",
    )
    parser.add_argument(
        "--relatorio",
        action="store_true",
        help="Gera o relatorio TXT e encerra, sem abrir o menu interativo.",
    )
    return parser.parse_args()


def main():
    """Ponto de entrada: carrega os dados e abre menu ou gera relatorio."""
    args = parse_args()
    caminho_csv = args.csv.resolve()

    if not caminho_csv.exists():
        print(f"Arquivo CSV nao encontrado: {caminho_csv}")
        return

    dados = carregar_dados(caminho_csv)
    print(f"Base carregada: {len(dados)} registros de {caminho_csv}")

    if args.relatorio:
        caminho = gerar_relatorio(dados, RELATORIO_PADRAO, caminho_csv)
        print(f"Relatorio gerado em: {caminho}")
        return

    menu_principal(dados, caminho_csv)


if __name__ == "__main__":
    main()
