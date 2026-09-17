import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Matriz de Performance — SP Capital",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

    /* ---------- GERAL ---------- */

    .stApp {
        background: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        color: #0f172a !important;
    }

    /* ---------- HEADER ---------- */

    .header-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, .04);
    }

    .header-title {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .header-subtitle {
        font-size: 14px;
        color: #64748b;
        font-weight: 500;
    }

    .info-banner {
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        color: #3730a3;
        border-radius: 9px;
        padding: 12px 16px;
        font-size: 13px;
        font-weight: 500;
        margin-top: 18px;
    }

    /* ---------- KPI ---------- */

    .kpi-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        min-height: 115px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, .04);
    }

    .kpi-label {
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .07em;
    }

    .kpi-value {
        color: #0f172a;
        font-size: 25px;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-detail {
        color: #64748b;
        font-size: 12px;
        margin-top: 3px;
        font-weight: 500;
    }

    .positive {
        color: #059669 !important;
    }

    .negative {
        color: #e11d48 !important;
    }

    .neutral {
        color: #475569 !important;
    }

    /* ---------- SEÇÕES ---------- */

    .section-title {
        font-size: 19px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 8px;
        margin-bottom: 3px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 14px;
    }

    /* ---------- MATRIZ ---------- */

    .matrix-wrapper {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(15, 23, 42, .04);
    }

    .store-name {
        font-weight: 800;
        color: #0f172a;
    }

    .new-store {
        background: #eff6ff;
        color: #0369a1;
        border: 1px solid #bae6fd;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 10px;
        font-weight: 700;
    }

    /* ---------- CONTROLES ---------- */

    div[data-testid="stSelectbox"] label,
    div[data-testid="stMultiSelect"] label {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #475569 !important;
    }

    /* ---------- BOTÕES ---------- */

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* ---------- TABS ---------- */

    button[data-baseweb="tab"] {
        font-weight: 700;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# DADOS
# ============================================================

dados = [

    # ANF
    ["ANF", "ANF — SHOPPING ANÁLIA FRANCO", "W36", 994493, 0.071, 0.169, 0.053, 0.022, False],
    ["ANF", "ANF — SHOPPING ANÁLIA FRANCO", "W37", 1034280, 0.210, 0.275, 0.232, -0.071, False],
    ["ANF", "ANF — SHOPPING ANÁLIA FRANCO", "W38", 256394, -0.029, 0.161, 0.218, -0.128, False],

    # APL
    ["APL", "APL — PAULISTA", "W36", 1058906, 0.094, None, None, None, True],
    ["APL", "APL — PAULISTA", "W37", 787733, -0.202, None, None, None, True],
    ["APL", "APL — PAULISTA", "W38", 353081, 0.026, None, None, None, True],

    # SCN
    ["SCN", "SCN — SHOPPING CENTER NORTE", "W36", 1676354, 0.010, -0.063, -0.134, 0.090, False],
    ["SCN", "SCN — SHOPPING CENTER NORTE", "W37", 1807131, 0.075, -0.008, -0.021, -0.016, False],
    ["SCN", "SCN — SHOPPING CENTER NORTE", "W38", 478941, -0.161, -0.084, -0.138, 0.072, False],

    # MRB
    ["MRB", "MRB — SHOPPING MORUMBI", "W36", 1439788, -0.079, -0.108, 0.003, -0.048, False],
    ["MRB", "MRB — SHOPPING MORUMBI", "W37", 1448346, 0.047, -0.104, 0.057, -0.116, False],
    ["MRB", "MRB — SHOPPING MORUMBI", "W38", 471330, 0.033, -0.061, 0.047, -0.065, False],

    # SCS
    ["SCS", "SCS — PARK SHOPPING SÃO CAETANO", "W36", 589146, -0.039, 0.123, -0.022, 0.015, False],
    ["SCS", "SCS — PARK SHOPPING SÃO CAETANO", "W37", 608027, 0.036, 0.112, 0.166, -0.116, False],
    ["SCS", "SCS — PARK SHOPPING SÃO CAETANO", "W38", 148215, -0.044, 0.156, 0.149, -0.079, False],

    # SPE
    ["SPE", "SPE — SHOPPING ELDORADO", "W36", 673999, -0.298, -0.053, -0.073, 0.083, False],
    ["SPE", "SPE — SHOPPING ELDORADO", "W37", 676235, -0.195, -0.031, 0.040, -0.024, False],
    ["SPE", "SPE — SHOPPING ELDORADO", "W38", 203512, -0.312, -0.093, -0.002, -0.005, False],

    # TBE
    ["TBE", "TBE — SHOPPING TAMBORÉ", "W36", 851884, -0.106, 0.043, 0.066, 0.025, False],
    ["TBE", "TBE — SHOPPING TAMBORÉ", "W37", 883374, -0.063, 0.087, 0.249, -0.087, False],
    ["TBE", "TBE — SHOPPING TAMBORÉ", "W38", 240063, -0.184, -0.020, 0.154, -0.100, False],

    # IGT
    ["IGT", "IGT — SHOPPING IGUATEMI SP", "W36", 601414, -0.124, -0.173, -0.263, 0.212, False],
    ["IGT", "IGT — SHOPPING IGUATEMI SP", "W37", 600206, -0.002, -0.182, -0.250, 0.066, False],
    ["IGT", "IGT — SHOPPING IGUATEMI SP", "W38", 228348, -0.223, -0.085, -0.153, 0.087, False],

    # SBO
    ["SBO", "SBO — SHOPPING BOURBON POMPÉIA", "W36", 531865, -0.202, -0.329, 0.183, -0.395, False],
    ["SBO", "SBO — SHOPPING BOURBON POMPÉIA", "W37", 546099, -0.211, -0.264, 0.231, -0.380, False],
    ["SBO", "SBO — SHOPPING BOURBON POMPÉIA", "W38", 158404, -0.243, -0.197, 0.197, -0.385, False],
]

df = pd.DataFrame(
    dados,
    columns=[
        "Loja",
        "Nome",
        "Semana",
        "Vendas",
        "% Base",
        "Vendas Vs LY",
        "Fluxo Vs LY",
        "Conversão Vs LY",
        "Nova"
    ]
)

ordem_lojas = [
    "ANF", "APL", "SCN", "MRB",
    "SCS", "SPE", "TBE", "IGT", "SBO"
]

ordem_semanas = ["W36", "W37", "W38"]

df["Semana"] = pd.Categorical(
    df["Semana"],
    categories=ordem_semanas,
    ordered=True
)


# ============================================================
# FUNÇÕES
# ============================================================

def dinheiro(valor):
    if pd.isna(valor):
        return "N/A"

    return f"R$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def numero(valor):
    if pd.isna(valor):
        return "N/A"

    return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def percentual(valor):
    if pd.isna(valor):
        return "N/A"

    sinal = "+" if valor > 0 else ""

    return (
        f"{sinal}{valor * 100:.2f}%"
        .replace(".", ",")
    )


def percentual_simples(valor):
    if pd.isna(valor):
        return "N/A"

    return f"{valor * 100:.2f}%".replace(".", ",")


def classe_percentual(valor):
    if pd.isna(valor):
        return "neutral"

    if valor > 0:
        return "positive"

    if valor < 0:
        return "negative"

    return "neutral"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("### 🔎 Filtros")

    lojas_selecionadas = st.multiselect(
        "Lojas",
        options=ordem_lojas,
        default=ordem_lojas,
        format_func=lambda x: x
    )

    semanas_selecionadas = st.multiselect(
        "Semanas",
        options=ordem_semanas,
        default=ordem_semanas
    )

    st.divider()

    indicador = st.selectbox(
        "Indicador para análise",
        [
            "Vendas",
            "% Base",
            "Vendas Vs LY",
            "Fluxo Vs LY",
            "Conversão Vs LY"
        ]
    )

    st.divider()

    st.caption(
        "Cada registro representa uma semana por loja."
    )


# ============================================================
# FILTRO PRINCIPAL
# ============================================================

df_filtrado = df[
    df["Loja"].isin(lojas_selecionadas) &
    df["Semana"].isin(semanas_selecionadas)
].copy()

df_filtrado = df_filtrado.sort_values(
    ["Loja", "Semana"]
)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header-box">

    <div class="header-title">
        Matriz de Performance — SP Capital
    </div>

    <div class="header-subtitle">
        Visão tabular por loja e sub-métricas operacionais · W36 a W38
    </div>

    <div class="info-banner">
        <strong>APL — Paulista:</strong>
        inaugurada em 2026. Comparativos Vs LY não se aplicam.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# KPI
# ============================================================

vendas_total = df_filtrado["Vendas"].sum()

# YTD completo para lojas selecionadas
df_ytd = df[
    df["Loja"].isin(lojas_selecionadas)
].copy()

vendas_por_loja = (
    df_ytd.groupby("Loja")["Vendas"]
    .sum()
    .sort_values(ascending=False)
)

if len(vendas_por_loja) > 0:
    maior_volume_loja = vendas_por_loja.index[0]
    maior_volume_valor = vendas_por_loja.iloc[0]
else:
    maior_volume_loja = "-"
    maior_volume_valor = 0


# Crescimento YTD
crescimento_ytd = (
    df_ytd.groupby("Loja")["Vendas Vs LY"]
    .mean()
    .dropna()
)

if len(crescimento_ytd) > 0:
    maior_crescimento_loja = crescimento_ytd.idxmax()
    maior_crescimento_valor = crescimento_ytd.max()
else:
    maior_crescimento_loja = "-"
    maior_crescimento_valor = None


# APL
apl_vendas = df[
    df["Loja"] == "APL"
]["Vendas"].sum()


c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Vendas Totais Regional</div>
        <div class="kpi-value">{dinheiro(vendas_total)}</div>
        <div class="kpi-detail">
            {len(lojas_selecionadas)} lojas selecionadas
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Maior Volume</div>
        <div class="kpi-value">{maior_volume_loja}</div>
        <div class="kpi-detail">
            {dinheiro(maior_volume_valor)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:

    if maior_crescimento_valor is not None:
        crescimento_texto = percentual(maior_crescimento_valor)
        classe = classe_percentual(maior_crescimento_valor)
    else:
        crescimento_texto = "N/A"
        classe = "neutral"

    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Maior Crescimento Vs LY</div>
        <div class="kpi-value">{maior_crescimento_loja}</div>
        <div class="kpi-detail {classe}">
            {crescimento_texto} YTD Vs LY
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Inauguração 2026</div>
        <div class="kpi-value" style="color:#0369a1">
            APL
        </div>
        <div class="kpi-detail">
            {dinheiro(apl_vendas)}
        </div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# TABS
# ============================================================

tab_matriz, tab_analises = st.tabs(
    ["▦ Matriz", "⌁ Análises"]
)


# ============================================================
# TAB MATRIZ
# ============================================================

with tab_matriz:

    st.markdown(
        '<div class="section-title">Matriz de Performance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Evolução semanal por loja e indicador'
        '</div>',
        unsafe_allow_html=True
    )

    if df_filtrado.empty:

        st.info("Nenhum dado encontrado para os filtros selecionados.")

    else:

        # ----------------------------------------------------
        # Construção da matriz
        # ----------------------------------------------------

        semanas_visiveis = [
            s for s in ordem_semanas
            if s in semanas_selecionadas
        ]

        colunas = ["Loja / Métrica"] + semanas_visiveis + ["YTD"]

        tabela_html = """
        <div class="matrix-wrapper">
        <table style="
            width:100%;
            border-collapse:collapse;
            font-size:13px;
        ">
        <thead>
        <tr style="
            background:#1e293b;
            color:white;
        ">
        """

        for coluna in colunas:

            alinhamento = "left" if coluna == "Loja / Métrica" else "right"

            tabela_html += f"""
            <th style="
                padding:13px 18px;
                text-align:{alinhamento};
                font-size:11px;
                font-weight:700;
                letter-spacing:.06em;
                text-transform:uppercase;
                border-bottom:2px solid #0f172a;
            ">
                {coluna}
            </th>
            """

        tabela_html += "</tr></thead><tbody>"

        # ----------------------------------------------------
        # Uma seção para cada loja
        # ----------------------------------------------------

        for loja in ordem_lojas:

            if loja not in lojas_selecionadas:
                continue

            dados_loja = df_ytd[
                df_ytd["Loja"] == loja
            ].sort_values("Semana")

            if dados_loja.empty:
                continue

            nome = dados_loja["Nome"].iloc[0]
            nova = bool(dados_loja["Nova"].iloc[0])

            tabela_html += """
            <tr>
                <td colspan="999" style="
                    background:#f1f5f9;
                    padding:11px 18px;
                    border-top:1px solid #e2e8f0;
                    border-bottom:1px solid #e2e8f0;
                ">
            """

            tabela_html += f"""
                <span style="
                    font-weight:800;
                    color:#0f172a;
                ">
                    {nome}
                </span>
            """

            if nova:
                tabela_html += """
                <span style="
                    margin-left:10px;
                    background:#eff6ff;
                    color:#0369a1;
                    border:1px solid #bae6fd;
                    border-radius:6px;
                    padding:3px 8px;
                    font-size:10px;
                    font-weight:700;
                ">
                    INAUGURAÇÃO 2026 · SEM LY
                </span>
                """

            tabela_html += "</td></tr>"

            # ------------------------------------------------
            # Indicadores
            # ------------------------------------------------

            indicadores = [
                ("Vendas", "Vendas", "money"),
                ("% Base", "% Base", "percent_simple"),
                ("Vendas Vs LY %", "Vendas Vs LY", "percent"),
                ("Fluxo Vs LY %", "Fluxo Vs LY", "percent"),
                ("Conversão Vs LY %", "Conversão Vs LY", "percent"),
            ]

            for nome_indicador, coluna_df, formato in indicadores:

                tabela_html += "<tr>"

                tabela_html += f"""
                <td style="
                    padding:9px 18px 9px 34px;
                    color:#475569;
                    font-weight:500;
                    border-bottom:1px solid #f1f5f9;
                ">
                    {nome_indicador}
                </td>
                """

                for semana in semanas_visiveis:

                    linha = dados_loja[
                        dados_loja["Semana"] == semana
                    ]

                    if linha.empty:
                        valor = None
                    else:
                        valor = linha.iloc[0][coluna_df]

                    if formato == "money":
                        texto = numero(valor)

                    elif formato == "percent_simple":
                        texto = percentual_simples(valor)

                    else:
                        texto = percentual(valor)

                    classe = ""

                    if formato == "percent":

                        if pd.notna(valor):

                            if valor > 0:
                                classe = "color:#059669;font-weight:700;"

                            elif valor < 0:
                                classe = "color:#e11d48;font-weight:700;"

                            else:
                                classe = "color:#475569;font-weight:600;"

                    elif pd.isna(valor):

                        classe = "color:#94a3b8;"

                    tabela_html += f"""
                    <td style="
                        padding:9px 18px;
                        text-align:right;
                        font-variant-numeric:tabular-nums;
                        border-bottom:1px solid #f1f5f9;
                        {classe}
                    ">
                        {texto}
                    </td>
                    """

                # YTD
                if formato == "money":

                    ytd = dados_loja["Vendas"].sum()
                    texto_ytd = numero(ytd)

                elif formato == "percent_simple":

                    ytd = dados_loja["% Base"].mean()
                    texto_ytd = percentual_simples(ytd)

                else:

                    valores = dados_loja[coluna_df].dropna()

                    if len(valores) > 0:
                        ytd = valores.mean()
                        texto_ytd = percentual(ytd)
                    else:
                        ytd = None
                        texto_ytd = "N/A"

                classe_ytd = ""

                if formato == "percent" and pd.notna(ytd):

                    if ytd > 0:
                        classe_ytd = "color:#059669;font-weight:800;"

                    elif ytd < 0:
                        classe_ytd = "color:#e11d48;font-weight:800;"

                tabela_html += f"""
                <td style="
                    padding:9px 18px;
                    text-align:right;
                    font-weight:800;
                    background:#fafafa;
                    border-bottom:1px solid #f1f5f9;
                    {classe_ytd}
                ">
                    {texto_ytd}
                </td>
                """

                tabela_html += "</tr>"

        tabela_html += "</tbody></table></div>"

        st.markdown(
            tabela_html,
            unsafe_allow_html=True
        )


# ============================================================
# TAB ANÁLISES
# ============================================================

with tab_analises:

    st.markdown(
        '<div class="section-title">Análises Interativas</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Explore a evolução do indicador selecionado por loja'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # CONTROLES DA ANÁLISE
    # --------------------------------------------------------

    col1, col2 = st.columns([2, 1])

    with col1:

        indicador_analise = st.radio(
            "Indicador",
            [
                "Vendas",
                "% Base",
                "Vendas Vs LY",
                "Fluxo Vs LY",
                "Conversão Vs LY"
            ],
            horizontal=True,
            index=[
                "Vendas",
                "% Base",
                "Vendas Vs LY",
                "Fluxo Vs LY",
                "Conversão Vs LY"
            ].index(indicador)
        )

    with col2:

        loja_foco = st.selectbox(
            "Loja em foco",
            options=lojas_selecionadas if lojas_selecionadas else ordem_lojas
        )

    st.write("")

    # --------------------------------------------------------
    # GRÁFICO PRINCIPAL
    # --------------------------------------------------------

    mapa_colunas = {
        "Vendas": "Vendas",
        "% Base": "% Base",
        "Vendas Vs LY": "Vendas Vs LY",
        "Fluxo Vs LY": "Fluxo Vs LY",
        "Conversão Vs LY": "Conversão Vs LY"
    }

    coluna_indicador = mapa_colunas[indicador_analise]

    dados_grafico = df_filtrado[
        df_filtrado["Loja"].isin(lojas_selecionadas)
    ].copy()

    fig = go.Figure()

    for loja in lojas_selecionadas:

        d = dados_grafico[
            dados_grafico["Loja"] == loja
        ].sort_values("Semana")

        if d.empty:
            continue

        valores = d[coluna_indicador]

        if valores.notna().sum() == 0:
            continue

        fig.add_trace(
            go.Scatter(
                x=d["Semana"],
                y=valores,
                mode="lines+markers",
                name=loja,
                connectgaps=False,
                line=dict(width=3),
                marker=dict(size=8),
                customdata=d[
                    [
                        "Vendas",
                        "% Base",
                        "Vendas Vs LY",
                        "Fluxo Vs LY",
                        "Conversão Vs LY"
                    ]
                ],
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Semana: %{x}<br><br>"
                    "Vendas: R$ %{customdata[0]:,.0f}<br>"
                    "% Base: %{customdata[1]:.2%}<br>"
                    "Vendas Vs LY: %{customdata[2]:+.2%}<br>"
                    "Fluxo Vs LY: %{customdata[3]:+.2%}<br>"
                    "Conversão Vs LY: %{customdata[4]:+.2%}"
                    "<extra></extra>"
                )
            )
        )

    if indicador_analise == "Vendas":

        titulo_eixo = "Vendas (R$)"
        eixo_format = ",.0f"

    else:

        titulo_eixo = f"{indicador_analise} (%)"
        eixo_format = ".1%"

    fig.update_layout(
        title=f"Evolução semanal — {indicador_analise}",
        height=500,
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=60, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        xaxis=dict(
            title="Semana",
            categoryorder="array",
            categoryarray=ordem_semanas
        ),
        yaxis=dict(
            title=titulo_eixo,
            tickformat=eixo_format,
            zeroline=True,
            zerolinecolor="#cbd5e1"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # LOJA EM FOCO
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Loja em foco</div>',
        unsafe_allow_html=True
    )

    loja_df = df[
        df["Loja"] == loja_foco
    ].sort_values("Semana")

    if not loja_df.empty:

        nome_loja = loja_df["Nome"].iloc[0]

        st.markdown(
            f"### {nome_loja}"
        )

        ultima = loja_df.iloc[-1]

        c1, c2, c3, c4, c5 = st.columns(5)

        # Vendas
        with c1:
            st.metric(
                "Vendas",
                dinheiro(ultima["Vendas"])
            )

        # Base
        with c2:
            st.metric(
                "% Base",
                percentual_simples(ultima["% Base"])
            )

        # Vendas LY
        with c3:

            if pd.isna(ultima["Vendas Vs LY"]):
                st.metric("Vendas Vs LY", "N/A")
            else:
                st.metric(
                    "Vendas Vs LY",
                    percentual(ultima["Vendas Vs LY"])
                )

        # Fluxo
        with c4:

            if pd.isna(ultima["Fluxo Vs LY"]):
                st.metric("Fluxo Vs LY", "N/A")
            else:
                st.metric(
                    "Fluxo Vs LY",
                    percentual(ultima["Fluxo Vs LY"])
                )

        # Conversão
        with c5:

            if pd.isna(ultima["Conversão Vs LY"]):
                st.metric("Conversão Vs LY", "N/A")
            else:
                st.metric(
                    "Conversão Vs LY",
                    percentual(ultima["Conversão Vs LY"])
                )


        # ----------------------------------------------------
        # HEATMAP
        # ----------------------------------------------------

        st.write("")

        st.markdown(
            "#### Mapa de evolução"
        )

        heat_df = loja_df[
            [
                "Semana",
                "Vendas Vs LY",
                "Fluxo Vs LY",
                "Conversão Vs LY"
            ]
        ].copy()

        heat_df = heat_df.set_index("Semana")

        heat_df.columns = [
            "Vendas Vs LY",
            "Fluxo Vs LY",
            "Conversão Vs LY"
        ]

        fig_heat = go.Figure(
            data=go.Heatmap(
                z=heat_df.T.values,
                x=heat_df.index,
                y=heat_df.columns,
                text=[
                    [
                        percentual(v)
                        for v in linha
                    ]
                    for linha in heat_df.T.values
                ],
                texttemplate="%{text}",
                colorscale=[
                    [0, "#fecdd3"],
                    [0.5, "#ffffff"],
                    [1, "#bbf7d0"]
                ],
                zmid=0,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Semana: %{x}<br>"
                    "Valor: %{text}"
                    "<extra></extra>"
                )
            )
        )

        fig_heat.update_layout(
            height=300,
            template="plotly_white",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig_heat,
            use_container_width=True
        )


# ============================================================
# DOWNLOAD
# ============================================================

st.divider()

csv = df_filtrado.to_csv(
    index=False,
    sep=";",
    decimal=","
).encode("utf-8-sig")

st.download_button(
    label="⬇ Exportar dados filtrados",
    data=csv,
    file_name="matriz_performance_sp_capital.csv",
    mime="text/csv"
)
