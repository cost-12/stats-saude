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
    registros_municipios = []
    with caminho_csv.open("r", encoding="utf-8-sig", newline="") as arquivo:
        # DictReader usa a primeira linha do CSV como nome das chaves do dicionario.
        leitor = csv.DictReader(arquivo)
        for linha_csv in leitor:
            registro = {}
            for nome_coluna_csv, valor_csv in linha_csv.items():
                # strip remove espacos do nome da coluna; converter_valor prepara os valores.
                registro[nome_coluna_csv.strip()] = converter_valor(valor_csv)
            adicionar_indicadores(registro)
            registros_municipios.append(registro)
    return registros_municipios


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


def valores_numericos(registros, nome_coluna):
    """Pega apenas os valores numericos de uma coluna."""
    valores_da_coluna = []
    for registro in registros:
        valor_da_coluna = registro.get(nome_coluna)
        if isinstance(valor_da_coluna, (int, float)):
            valores_da_coluna.append(valor_da_coluna)
    return valores_da_coluna


def estatisticas_coluna(registros, nome_coluna):
    """Calcula soma, media, mediana, minimo e maximo de uma coluna."""
    valores_da_coluna = valores_numericos(registros, nome_coluna)
    if not valores_da_coluna:
        return None

    return {
        "quantidade": len(valores_da_coluna),
        "soma": sum(valores_da_coluna),
        "media": mean(valores_da_coluna),
        "mediana": median(valores_da_coluna),
        "minimo": min(valores_da_coluna),
        "maximo": max(valores_da_coluna),
    }


def colunas_numericas(registros):
    """Descobre quais colunas possuem pelo menos um valor numerico."""
    if not registros:
        return []

    colunas_com_numeros = []
    for nome_coluna in registros[0]:
        encontrou_numero = False
        for registro in registros:
            if isinstance(registro.get(nome_coluna), (int, float)):
                encontrou_numero = True
                break

        if encontrou_numero:
            colunas_com_numeros.append(nome_coluna)
    return colunas_com_numeros


def frequencia(registros, nome_coluna):
    """Conta frequencia e percentual de cada categoria em uma coluna."""
    contagem_por_categoria = {}
    for registro in registros:
        categoria = registro.get(nome_coluna, "Nao informado")
        contagem_por_categoria[categoria] = contagem_por_categoria.get(categoria, 0) + 1

    total = len(registros)
    resumo_frequencias = []
    for categoria, quantidade in contagem_por_categoria.items():
        resumo_categoria = {
            "categoria": categoria,
            "frequencia": quantidade,
            "percentual": percentual(quantidade, total),
        }
        resumo_frequencias.append(resumo_categoria)

    return sorted(resumo_frequencias, key=pegar_frequencia, reverse=True)


def pegar_frequencia(item_frequencia):
    """Retorna a frequencia de um item para ajudar na ordenacao."""
    return item_frequencia["frequencia"]


def ranking(registros, nome_coluna, reverso=True, limite=10):
    """Ordena os registros por uma coluna e retorna os primeiros colocados."""
    def pegar_valor(registro):
        return registro.get(nome_coluna, 0)

    registros_ordenados = sorted(registros, key=pegar_valor, reverse=reverso)
    return registros_ordenados[:limite]


def agrupar_media(registros, categoria, nome_coluna):
    """Agrupa registros por categoria e calcula a media de uma coluna numerica."""
    valores_por_grupo = {}
    for registro in registros:
        valor_da_coluna = registro.get(nome_coluna)
        if isinstance(valor_da_coluna, (int, float)):
            nome_grupo = registro.get(categoria, "Nao informado")
            if nome_grupo not in valores_por_grupo:
                valores_por_grupo[nome_grupo] = []
            valores_por_grupo[nome_grupo].append(valor_da_coluna)

    medias_por_grupo = []
    for nome_grupo, valores_do_grupo in valores_por_grupo.items():
        medias_por_grupo.append((nome_grupo, mean(valores_do_grupo), len(valores_do_grupo)))
    return sorted(medias_por_grupo, key=pegar_media_do_grupo, reverse=True)


def pegar_media_do_grupo(grupo_com_media):
    """Retorna a media guardada na tupla criada por agrupar_media."""
    return grupo_com_media[1]


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

    colunas_tabela = campos or CAMPOS_TABELA
    registros_exibidos = registros[:limite]
    linhas_formatadas = []

    # Primeiro os valores sao formatados como texto para calcular a largura das colunas.
    for registro in registros_exibidos:
        linha_formatada = {}
        for nome_coluna in colunas_tabela:
            valor_formatado_coluna = valor_formatado(registro.get(nome_coluna, ""))
            linha_formatada[nome_coluna] = cortar_texto(valor_formatado_coluna)
        linhas_formatadas.append(linha_formatada)

    # A largura de cada coluna respeita o maior texto encontrado, com limite de 28.
    larguras = {}
    for nome_coluna in colunas_tabela:
        maior_largura = len(nome_coluna)
        for linha_formatada in linhas_formatadas:
            largura_texto = len(str(linha_formatada[nome_coluna]))
            if largura_texto > maior_largura:
                maior_largura = largura_texto
        larguras[nome_coluna] = min(28, maior_largura)

    # Cabecalho, separador e corpo sao montados separadamente para formar a tabela final.
    partes_cabecalho = []
    partes_separador = []
    for nome_coluna in colunas_tabela:
        partes_cabecalho.append(nome_coluna.ljust(larguras[nome_coluna]))
        partes_separador.append("-" * larguras[nome_coluna])

    cabecalho = " | ".join(partes_cabecalho)
    separador = "-+-".join(partes_separador)

    corpo = []
    for linha_formatada in linhas_formatadas:
        partes_linha = []
        for nome_coluna in colunas_tabela:
            partes_linha.append(str(linha_formatada[nome_coluna]).ljust(larguras[nome_coluna]))
        corpo.append(" | ".join(partes_linha))

    rodape = ""
    if len(registros) > limite:
        rodape = f"\nMostrando {limite} de {len(registros)} registros."

    linhas_tabela = [cabecalho, separador]
    linhas_tabela.extend(corpo)
    return "\n".join(linhas_tabela) + rodape


def imprimir_tabela(registros, campos=None, limite=20):
    """Mostra no terminal uma tabela gerada por texto_tabela."""
    print(texto_tabela(registros, campos, limite))


def mostrar_estatisticas_gerais(registros):
    """Exibe estatisticas gerais e indicadores derivados no terminal."""
    print("\n=== Estatisticas Gerais ===")
    print(f"Quantidade de registros: {len(registros)}")

    for nome_coluna in CAMPOS_BASE:
        estatisticas = estatisticas_coluna(registros, nome_coluna)
        if not estatisticas:
            continue

        print(f"\n{nome_coluna}")
        print(f"  Soma:    {valor_formatado(estatisticas['soma'])}")
        print(f"  Media:   {valor_formatado(estatisticas['media'])}")
        print(f"  Mediana: {valor_formatado(estatisticas['mediana'])}")
        print(f"  Minimo:  {valor_formatado(estatisticas['minimo'])}")
        print(f"  Maximo:  {valor_formatado(estatisticas['maximo'])}")

    print("\nIndicadores de saude derivados")
    for nome_coluna in CAMPOS_INDICADORES:
        estatisticas = estatisticas_coluna(registros, nome_coluna)
        if estatisticas:
            print(f"  {nome_coluna}: media {valor_formatado(estatisticas['media'])}")


def mostrar_distribuicoes(registros):
    """Exibe distribuicao, frequencia e percentual das categorias da analise."""
    print("\n=== Distribuicao, frequencia e percentual ===")

    for nome_coluna in CAMPOS_CATEGORICOS_ANALISE:
        print(f"\n{nome_coluna}")
        print("Categoria                    | Frequencia | Percentual")
        print("-----------------------------+------------+-----------")
        for resumo_categoria in frequencia(registros, nome_coluna):
            print(
                f"{resumo_categoria['categoria']:<28} | "
                f"{resumo_categoria['frequencia']:>10} | "
                f"{valor_formatado(resumo_categoria['percentual']):>9}%"
            )


def buscar_municipios_por_nome(registros, texto_busca):
    """Retorna municipios que possuem o termo informado no nome."""
    texto_busca = texto_busca.strip().lower()
    municipios_encontrados = []
    for registro in registros:
        municipio = str(registro.get("municipio", "")).lower()
        if texto_busca in municipio:
            municipios_encontrados.append(registro)
    return municipios_encontrados


def mostrar_municipios_prioritarios(registros):
    """Mostra rankings que ajudam a localizar municipios com maior atencao."""
    print("\n=== Municipios que merecem atencao ===")

    print("\nMenor disponibilidade de medicos por 10 mil habitantes")
    imprimir_tabela(
        ranking(registros, "medicos_por_10k", reverso=False),
        campos=["municipio", "medicos", "populacao_atendida", "medicos_por_10k"],
        limite=10,
    )

    print("\nMaior numero de habitantes por UBS")
    imprimir_tabela(
        ranking(registros, "habitantes_por_ubs", reverso=True),
        campos=["municipio", "ubs", "populacao_atendida", "habitantes_por_ubs"],
        limite=10,
    )

    print("\nMaior populacao atendida")
    imprimir_tabela(
        ranking(registros, "populacao_atendida", reverso=True),
        campos=["municipio", "populacao_atendida", "ubs", "total_profissionais"],
        limite=10,
    )


def mostrar_consultas(registros):
    """Mostra consultas principais sem abrir um segundo menu."""
    print("\n=== Consultas ===")
    print(f"Total de registros disponiveis para consulta: {len(registros)}")

    mostrar_municipios_prioritarios(registros)

    texto_busca = input("\nBuscar municipio por nome (enter para voltar): ").strip()
    if not texto_busca:
        return

    municipios_encontrados = buscar_municipios_por_nome(registros, texto_busca)
    print(f"\nRegistros encontrados: {len(municipios_encontrados)}")
    imprimir_tabela(municipios_encontrados, limite=30)


def linhas_analise_exploratoria(registros):
    """Cria as linhas de texto da analise exploratoria da base."""
    linhas_analise = []
    linhas_analise.append("=== Analise exploratoria dos dados ===")
    linhas_analise.append(f"Quantidade de registros: {len(registros)}")
    linhas_analise.append(f"Quantidade de colunas: {len(registros[0]) if registros else 0}")
    linhas_analise.append("")

    if not registros:
        return linhas_analise

    # Compara a lista de municipios com um set para descobrir nomes duplicados.
    nomes_municipios = []
    for registro in registros:
        nomes_municipios.append(registro.get("municipio"))
    municipios_repetidos = len(nomes_municipios) - len(set(nomes_municipios))
    linhas_analise.append(f"Municipios repetidos: {municipios_repetidos}")
    linhas_analise.append("")

    linhas_analise.append("Valores ausentes por coluna:")
    for nome_coluna in registros[0]:
        # Considera vazio quando o valor e string vazia ou None.
        valores_ausentes = 0
        for registro in registros:
            if registro.get(nome_coluna) in ("", None):
                valores_ausentes += 1
        linhas_analise.append(f"- {nome_coluna}: {valores_ausentes}")

    linhas_analise.append("")
    linhas_analise.append("Colunas numericas e intervalos:")
    for nome_coluna in colunas_numericas(registros):
        # Reaproveita apenas os valores numericos para evitar erro em min, max e media.
        valores_da_coluna = valores_numericos(registros, nome_coluna)
        linhas_analise.append(
            f"- {nome_coluna}: minimo {valor_formatado(min(valores_da_coluna))}, "
            f"maximo {valor_formatado(max(valores_da_coluna))}, "
            f"media {valor_formatado(mean(valores_da_coluna))}"
        )

    linhas_analise.append("")
    linhas_analise.append("Filtros recomendados para a dashboard:")
    linhas_analise.append("- municipio: busca textual por nome.")
    linhas_analise.append("- faixa_populacao: compara municipios por porte de atendimento.")
    linhas_analise.append("- nivel_ubs: identifica pressao sobre a estrutura de UBS.")
    linhas_analise.append("- nivel_medicos_10k: identifica disponibilidade medica relativa.")
    linhas_analise.append("- habitantes_por_ubs e medicos_por_10k: bons campos para ranking.")

    return linhas_analise


def gerar_descobertas(registros):
    """Gera frases com informacoes relevantes encontradas na base."""
    if not registros:
        return ["Nao ha dados carregados."]

    # Calcula os principais extremos e medias uma vez para montar as frases finais.
    total_municipios = len(registros)
    total_populacao_atendida = 0
    municipios_com_baixa_disponibilidade_medica = 0
    municipios_com_baixa_disponibilidade_ubs = 0

    for registro in registros:
        total_populacao_atendida += registro["populacao_atendida"]
        if registro["nivel_medicos_10k"] == "Baixa disponibilidade":
            municipios_com_baixa_disponibilidade_medica += 1
        if registro["nivel_ubs"] == "Baixa disponibilidade":
            municipios_com_baixa_disponibilidade_ubs += 1

    municipio_maior_populacao = ranking(registros, "populacao_atendida")[0]
    municipio_maior_equipe = ranking(registros, "total_profissionais")[0]
    municipio_menor_indicador_medicos = ranking(registros, "medicos_por_10k", reverso=False)[0]
    municipio_maior_pressao_ubs = ranking(registros, "habitantes_por_ubs")[0]
    media_ubs = mean(valores_numericos(registros, "ubs"))
    media_medicos_10k = mean(valores_numericos(registros, "medicos_por_10k"))
    faixa_mais_frequente = frequencia(registros, "faixa_populacao")[0]
    melhor_faixa_medicos = agrupar_media(registros, "faixa_populacao", "medicos_por_10k")[0]

    # A funcao devolve textos prontos para uso no terminal e no relatorio.
    descobertas = []
    descobertas.append(
        f"A base possui {total_municipios} municipios e soma "
        f"{valor_formatado(total_populacao_atendida)} pessoas atendidas."
    )
    descobertas.append(f"A media geral e de {valor_formatado(media_ubs)} UBS por municipio.")
    descobertas.append(
        f"A media de medicos por 10 mil habitantes e {valor_formatado(media_medicos_10k)}."
    )
    descobertas.append(
        f"{valor_formatado(percentual(municipios_com_baixa_disponibilidade_medica, total_municipios))}% "
        "dos municipios "
        "estao em baixa disponibilidade medica pela classificacao interna."
    )
    descobertas.append(
        f"{valor_formatado(percentual(municipios_com_baixa_disponibilidade_ubs, total_municipios))}% "
        "dos municipios "
        "tem baixa disponibilidade de UBS pela relacao habitantes por unidade."
    )
    descobertas.append(
        f"O municipio com maior populacao atendida e {municipio_maior_populacao['municipio']} "
        f"({valor_formatado(municipio_maior_populacao['populacao_atendida'])} pessoas)."
    )
    descobertas.append(
        f"O municipio com maior equipe de saude e {municipio_maior_equipe['municipio']} "
        f"({valor_formatado(municipio_maior_equipe['total_profissionais'])} profissionais)."
    )
    descobertas.append(
        f"O menor indicador de medicos por 10 mil habitantes aparece em "
        f"{municipio_menor_indicador_medicos['municipio']} "
        f"({valor_formatado(municipio_menor_indicador_medicos['medicos_por_10k'])})."
    )
    descobertas.append(
        f"A maior pressao sobre UBS aparece em {municipio_maior_pressao_ubs['municipio']}, "
        f"com {valor_formatado(municipio_maior_pressao_ubs['habitantes_por_ubs'])} habitantes por UBS."
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


def mostrar_descobertas(registros):
    """Mostra no terminal as descobertas geradas pela analise."""
    print("\n=== Descobertas sobre os dados ===")
    for descoberta in gerar_descobertas(registros):
        print(f"- {descoberta}")


def mostrar_estatisticas(registros):
    """Mostra um bloco unico com estatisticas, distribuicoes e descobertas."""
    mostrar_estatisticas_gerais(registros)
    mostrar_distribuicoes(registros)
    mostrar_descobertas(registros)


def linhas_estatisticas(registros):
    """Cria as linhas de texto da secao de estatisticas do relatorio."""
    linhas_estatisticas_relatorio = []
    linhas_estatisticas_relatorio.append("=== Estatisticas Gerais ===")
    linhas_estatisticas_relatorio.append(f"Quantidade de registros: {len(registros)}")

    for nome_coluna in CAMPOS_BASE:
        estatisticas = estatisticas_coluna(registros, nome_coluna)
        if not estatisticas:
            continue
        linhas_estatisticas_relatorio.append("")
        linhas_estatisticas_relatorio.append(nome_coluna)
        linhas_estatisticas_relatorio.append(f"- Soma: {valor_formatado(estatisticas['soma'])}")
        linhas_estatisticas_relatorio.append(f"- Media: {valor_formatado(estatisticas['media'])}")
        linhas_estatisticas_relatorio.append(f"- Mediana: {valor_formatado(estatisticas['mediana'])}")
        linhas_estatisticas_relatorio.append(f"- Minimo: {valor_formatado(estatisticas['minimo'])}")
        linhas_estatisticas_relatorio.append(f"- Maximo: {valor_formatado(estatisticas['maximo'])}")

    linhas_estatisticas_relatorio.append("")
    linhas_estatisticas_relatorio.append("Indicadores derivados")
    for nome_coluna in CAMPOS_INDICADORES:
        estatisticas = estatisticas_coluna(registros, nome_coluna)
        if estatisticas:
            linhas_estatisticas_relatorio.append(
                f"- {nome_coluna}: media {valor_formatado(estatisticas['media'])}, "
                f"minimo {valor_formatado(estatisticas['minimo'])}, "
                f"maximo {valor_formatado(estatisticas['maximo'])}"
            )

    return linhas_estatisticas_relatorio


def linhas_distribuicao(registros):
    """Cria as linhas de texto com frequencias e percentuais do relatorio."""
    linhas_distribuicao_relatorio = ["=== Distribuicao, frequencia e percentual ==="]
    for nome_coluna in CAMPOS_CATEGORICOS_ANALISE:
        linhas_distribuicao_relatorio.append("")
        linhas_distribuicao_relatorio.append(nome_coluna)
        for resumo_categoria in frequencia(registros, nome_coluna):
            linhas_distribuicao_relatorio.append(
                f"- {resumo_categoria['categoria']}: {resumo_categoria['frequencia']} "
                f"({valor_formatado(resumo_categoria['percentual'])}%)"
            )
    return linhas_distribuicao_relatorio


def linhas_rankings(registros):
    """Cria as linhas de texto com os rankings do relatorio."""
    linhas_rankings_relatorio = ["=== Ranking ==="]

    for titulo, nome_coluna, reverso in RANKINGS_RELATORIO:
        linhas_rankings_relatorio.append("")
        linhas_rankings_relatorio.append(titulo)
        for posicao, registro in enumerate(ranking(registros, nome_coluna, reverso=reverso), start=1):
            linhas_rankings_relatorio.append(
                f"{posicao:02d}. {registro['municipio']} - "
                f"{nome_coluna}: {valor_formatado(registro[nome_coluna])}"
            )

    return linhas_rankings_relatorio


def gerar_relatorio(registros, caminho_saida, caminho_csv):
    """Gera o arquivo TXT final reunindo analise, estatisticas e rankings."""
    # Garante que a pasta reports exista antes de tentar salvar o TXT.
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    linhas_relatorio = []
    linhas_relatorio.append("=" * 72)
    linhas_relatorio.append("RELATORIO DA DASHBOARD DE SAUDE")
    linhas_relatorio.append("=" * 72)
    linhas_relatorio.append(f"Gerado em: {agora}")
    linhas_relatorio.append(f"Base analisada: {caminho_csv}")
    linhas_relatorio.append("")
    linhas_relatorio.append("Observacao: classificacoes de disponibilidade sao operacionais para analise exploratoria")
    linhas_relatorio.append("e nao substituem parametros oficiais de saude publica.")
    linhas_relatorio.append("")

    linhas_relatorio.extend(linhas_analise_exploratoria(registros))
    linhas_relatorio.append("")
    linhas_relatorio.extend(linhas_estatisticas(registros))
    linhas_relatorio.append("")
    linhas_relatorio.extend(linhas_distribuicao(registros))
    linhas_relatorio.append("")
    linhas_relatorio.extend(linhas_rankings(registros))
    linhas_relatorio.append("")

    linhas_relatorio.append("=== Descobertas sobre os dados ===")
    for descoberta in gerar_descobertas(registros):
        linhas_relatorio.append(f"- {descoberta}")

    linhas_relatorio.append("")
    linhas_relatorio.append("=" * 72)
    linhas_relatorio.append("FIM DO RELATORIO")
    linhas_relatorio.append("=" * 72)

    caminho_saida.write_text("\n".join(linhas_relatorio), encoding="utf-8")
    return caminho_saida


def menu_principal(registros, caminho_csv):
    """Controla o menu principal da dashboard no terminal."""
    while True:
        print("\n" + "=" * 50)
        print("DASHBOARD DE SAUDE - TERMINAL")
        print("=" * 50)
        print("1. Consultas")
        print("2. Estatisticas")
        print("3. Relatorio TXT")
        print("0. Sair")

        opcao_menu = input("Escolha uma opcao: ").strip()

        if opcao_menu == "1":
            mostrar_consultas(registros)
        elif opcao_menu == "2":
            mostrar_estatisticas(registros)
        elif opcao_menu == "3":
            caminho_relatorio = gerar_relatorio(registros, RELATORIO_PADRAO, caminho_csv)
            print(f"Relatorio gerado em: {caminho_relatorio}")
        elif opcao_menu == "0":
            print("Encerrando dashboard.")
            break
        else:
            print("Opcao invalida. Tente novamente.")


def parse_args():
    """Le argumentos de linha de comando, como --csv e --relatorio."""
    analisador_argumentos = argparse.ArgumentParser(description="Dashboard terminal para dados de saude.")
    analisador_argumentos.add_argument(
        "--csv",
        type=Path,
        default=CSV_PADRAO,
        help="Caminho do arquivo CSV. Padrao: data/08_saude.csv",
    )
    analisador_argumentos.add_argument(
        "--relatorio",
        action="store_true",
        help="Gera o relatorio TXT e encerra, sem abrir o menu interativo.",
    )
    return analisador_argumentos.parse_args()


def main():
    """Ponto de entrada: carrega os registros e abre menu ou gera relatorio."""
    argumentos = parse_args()
    caminho_csv = argumentos.csv.resolve()

    if not caminho_csv.exists():
        print(f"Arquivo CSV nao encontrado: {caminho_csv}")
        return

    registros = carregar_dados(caminho_csv)
    print(f"Base carregada: {len(registros)} registros de {caminho_csv}")

    if argumentos.relatorio:
        caminho_relatorio = gerar_relatorio(registros, RELATORIO_PADRAO, caminho_csv)
        print(f"Relatorio gerado em: {caminho_relatorio}")
        return

    menu_principal(registros, caminho_csv)


if __name__ == "__main__":
    main()
