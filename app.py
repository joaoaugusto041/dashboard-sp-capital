import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Evolução Regional — SP Capital",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# BASE
# =========================================================

@st.cache_data
def load_data():

    raw_data = [
        {"Loja": "ANF", "Vendas": 1034280, "% Base": 0.210, "Vendas Vs LY %": 0.275, "Fluxo Vs LY %": 0.232, "Conversão Vs LY %": -0.071, "Semana": "W37"},
        {"Loja": "APL", "Vendas": 1058906, "% Base": 0.094, "Vendas Vs LY %": None, "Fluxo Vs LY %": None, "Conversão Vs LY %": None, "Semana": "W36"},
        {"Loja": "SCN", "Vendas": 1807131, "% Base": 0.075, "Vendas Vs LY %": -0.008, "Fluxo Vs LY %": -0.021, "Conversão Vs LY %": -0.016, "Semana": "W37"},
        {"Loja": "ANF", "Vendas": 994493, "% Base": 0.071, "Vendas Vs LY %": 0.169, "Fluxo Vs LY %": 0.053, "Conversão Vs LY %": 0.022, "Semana": "W36"},
        {"Loja": "MRB", "Vendas": 1448346, "% Base": 0.047, "Vendas Vs LY %": -0.104, "Fluxo Vs LY %": 0.057, "Conversão Vs LY %": -0.116, "Semana": "W37"},
        {"Loja": "SCS", "Vendas": 608027, "% Base": 0.036, "Vendas Vs LY %": 0.112, "Fluxo Vs LY %": 0.166, "Conversão Vs LY %": -0.116, "Semana": "W37"},
        {"Loja": "MRB", "Vendas": 471330, "% Base": 0.033, "Vendas Vs LY %": -0.061, "Fluxo Vs LY %": 0.047, "Conversão Vs LY %": -0.065, "Semana": "W38"},
        {"Loja": "APL", "Vendas": 353081, "% Base": 0.026, "Vendas Vs LY %": None, "Fluxo Vs LY %": None, "Conversão Vs LY %": None, "Semana": "W38"},
        {"Loja": "SCN", "Vendas": 1676354, "% Base": 0.010, "Vendas Vs LY %": -0.063, "Fluxo Vs LY %": -0.134, "Conversão Vs LY %": 0.090, "Semana": "W36"},
        {"Loja": "IGT", "Vendas": 600206, "% Base": -0.002, "Vendas Vs LY %": -0.182, "Fluxo Vs LY %": -0.250, "Conversão Vs LY %": 0.066, "Semana": "W37"},
        {"Loja": "ANF", "Vendas": 256394, "% Base": -0.029, "Vendas Vs LY %": 0.161, "Fluxo Vs LY %": 0.218, "Conversão Vs LY %": -0.128, "Semana": "W38"},
        {"Loja": "SCS", "Vendas": 589146, "% Base": -0.039, "Vendas Vs LY %": 0.123, "Fluxo Vs LY %": -0.022, "Conversão Vs LY %": 0.015, "Semana": "W36"},
        {"Loja": "SCS", "Vendas": 148215, "% Base": -0.044, "Vendas Vs LY %": 0.156, "Fluxo Vs LY %": 0.149, "Conversão Vs LY %": -0.079, "Semana": "W38"},
        {"Loja": "TBE", "Vendas": 883374, "% Base": -0.063, "Vendas Vs LY %": 0.087, "Fluxo Vs LY %": 0.249, "Conversão Vs LY %": -0.087, "Semana": "W37"},
        {"Loja": "MRB", "Vendas": 1439788, "% Base": -0.079, "Vendas Vs LY %": -0.108, "Fluxo Vs LY %": 0.003, "Conversão Vs LY %": -0.048, "Semana": "W36"},
        {"Loja": "TBE", "Vendas": 851884, "% Base": -0.106, "Vendas Vs LY %": 0.043, "Fluxo Vs LY %": 0.066, "Conversão Vs LY %": 0.025, "Semana": "W36"},
        {"Loja": "IGT", "Vendas": 601414, "% Base": -0.124, "Vendas Vs LY %": -0.173, "Fluxo Vs LY %": -0.263, "Conversão Vs LY %": 0.212, "Semana": "W36"},
        {"Loja": "SCN", "Vendas": 478941, "% Base": -0.161, "Vendas Vs LY %": -0.084, "Fluxo Vs LY %": -0.138, "Conversão Vs LY %": 0.072, "Semana": "W38"},
        {"Loja": "TBE", "Vendas": 240063, "% Base": -0.184, "Vendas Vs LY %": -0.020, "Fluxo Vs LY %": 0.154, "Conversão Vs LY %": -0.100, "Semana": "W38"},
        {"Loja": "SPE", "Vendas": 676235, "% Base": -0.195, "Vendas Vs LY %": -0.031, "Fluxo Vs LY %": 0.040, "Conversão Vs LY %": -0.024, "Semana": "W37"},
        {"Loja": "APL", "Vendas": 787733, "% Base": -0.202, "Vendas Vs LY %": None, "Fluxo Vs LY %": None, "Conversão Vs LY %": None, "Semana": "W37"},
        {"Loja": "SBO", "Vendas": 531865, "% Base": -0.202, "Vendas Vs LY %": -0.329, "Fluxo Vs LY %": 0.183, "Conversão Vs LY %": -0.395, "Semana": "W36"},
        {"Loja": "SBO", "Vendas": 546099, "% Base": -0.211, "Vendas Vs LY %": -0.264, "Fluxo Vs LY %": 0.231, "Conversão Vs LY %": -0.380, "Semana": "W37"},
        {"Loja": "IGT", "Vendas": 228348, "% Base": -0.223, "Vendas Vs LY %": -0.085, "Fluxo Vs LY %": -0.153, "Conversão Vs LY %": 0.087, "Semana": "W38"},
        {"Loja": "SBO", "Vendas": 158404, "% Base": -0.243, "Vendas Vs LY %": -0.265, "Fluxo Vs LY %": 0.197, "Conversão Vs LY %": -0.385, "Semana": "W38"},
        {"Loja": "SPE", "Vendas": 673999, "% Base": -0.298, "Vendas Vs LY %": -0.053, "Fluxo Vs LY %": -0.073, "Conversão Vs LY %": 0.083, "Semana": "W36"},
        {"Loja": "SPE", "Vendas": 203512, "% Base": -0.312, "Vendas Vs LY %": -0.093, "Fluxo Vs LY %": -0.002, "Conversão Vs LY %": -0.005, "Semana": "W38"},
    ]

    df = pd.DataFrame(raw_data)

    nomes = {
        "ANF": "ANF — Anália Franco",
        "APL": "APL — Paulista",
        "IGT": "IGT — Iguatemi",
        "MRB": "MRB — Morumbi",
        "SBO": "SBO — Bourbon Pompéia",
        "SCN": "SCN — Center Norte",
        "SCS": "SCS — São Caetano",
        "SPE": "SPE — Eldorado",
        "TBE": "TBE — Tamboré"
    }

    df["Nome_Loja"] = df["Loja"].map(nomes)

    df["Ordem"] = df["Semana"].map({
        "W36": 1,
        "W37": 2,
        "W38": 3
    })

    return df


df = load_data()

# =========================================================
# TÍTULO
# =========================================================

st.title("Evolução Regional — SP Capital")

st.caption(
    "Acompanhamento semanal dos principais indicadores | YTD 2026"
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Filtros")

todas_lojas = sorted(df["Nome_Loja"].unique())

lojas_selecionadas = st.sidebar.multiselect(
    "Lojas",
    todas_lojas,
    default=todas_lojas
)

semanas_selecionadas = st.sidebar.multiselect(
    "Semanas",
    ["W36", "W37", "W38"],
    default=["W36", "W37", "W38"]
)

st.sidebar.divider()

indicador = st.sidebar.selectbox(
    "Indicador principal",
    [
        "Vendas",
        "% Base",
        "Vendas Vs LY",
        "Fluxo Vs LY",
        "Conversão Vs LY"
    ]
)

df_f = df[
    df["Nome_Loja"].isin(lojas_selecionadas)
    & df["Semana"].isin(semanas_selecionadas)
].copy()

df_f = df_f.sort_values("Ordem")

# =========================================================
# MAPA DOS INDICADORES
# =========================================================

indicadores = {
    "Vendas": {
        "coluna": "Vendas",
        "titulo": "Vendas",
        "formato": "R$"
    },
    "% Base": {
        "coluna": "% Base",
        "titulo": "% Base",
        "formato": "%"
    },
    "Vendas Vs LY": {
        "coluna": "Vendas Vs LY %",
        "titulo": "Vendas Vs LY",
        "formato": "%"
    },
    "Fluxo Vs LY": {
        "coluna": "Fluxo Vs LY %",
        "titulo": "Fluxo Vs LY",
        "formato": "%"
    },
    "Conversão Vs LY": {
        "coluna": "Conversão Vs LY %",
        "titulo": "Conversão Vs LY",
        "formato": "%"
    }
}

config = indicadores[indicador]

coluna = config["coluna"]

# =========================================================
# CARDS
# =========================================================

if not df_f.empty:

    ultima_semana = df_f["Ordem"].max()

    df_ultima = df_f[
        df_f["Ordem"] == ultima_semana
    ]

    c1, c2, c3, c4 = st.columns(4)

    # -----------------------------------------------------
    # TOTAL
    # -----------------------------------------------------

    if indicador == "Vendas":

        valor = df_ultima["Vendas"].sum()

        c1.metric(
            "Vendas — última semana",
            f"R$ {valor:,.0f}".replace(",", ".")
        )

    else:

        valor = df_ultima[coluna].mean()

        if pd.isna(valor):

            c1.metric(
                config["titulo"],
                "N/A"
            )

        else:

            c1.metric(
                config["titulo"],
                f"{valor:+.1%}".replace(".", ",")
            )

    # -----------------------------------------------------
    # SEMANA
    # -----------------------------------------------------

    semana_nome = df_ultima["Semana"].iloc[0]

    c2.metric(
        "Última semana",
        semana_nome
    )

    # -----------------------------------------------------
    # QUANTIDADE DE LOJAS
    # -----------------------------------------------------

    c3.metric(
        "Lojas analisadas",
        df_f["Loja"].nunique()
    )

    # -----------------------------------------------------
    # VARIAÇÃO W36 → ÚLTIMA
    # -----------------------------------------------------

    if len(semanas_selecionadas) >= 2:

        primeira_ordem = min(
            df_f["Ordem"].unique()
        )

        df_primeira = df_f[
            df_f["Ordem"] == primeira_ordem
        ]

        if indicador == "Vendas":

            primeiro = df_primeira["Vendas"].sum()
            ultimo = df_ultima["Vendas"].sum()

        else:

            primeiro = df_primeira[coluna].mean()
            ultimo = df_ultima[coluna].mean()

        if primeiro != 0 and not pd.isna(primeiro):

            variacao = ultimo - primeiro

            if indicador == "Vendas":

                c4.metric(
                    "Variação no período",
                    f"R$ {variacao:,.0f}".replace(",", ".")
                )

            else:

                c4.metric(
                    "Variação no período",
                    f"{variacao:+.1%}".replace(".", ",")
                )

# =========================================================
# GRÁFICO PRINCIPAL
# =========================================================

st.divider()

st.subheader(
    f"Evolução semanal — {config['titulo']}"
)

df_chart = df_f.dropna(
    subset=[coluna]
)

if not df_chart.empty:

    fig = px.line(
        df_chart,
        x="Semana",
        y=coluna,
        color="Loja",
        markers=True,
        custom_data=["Nome_Loja"]
    )

    # -----------------------------------------------------
    # FORMATAÇÃO
    # -----------------------------------------------------

    if config["formato"] == "%":

        fig.update_yaxes(
            tickformat=".1%"
        )

        fig.update_traces(
            hovertemplate=
            "<b>%{customdata[0]}</b><br>"
            "Semana: %{x}<br>"
            f"{config['titulo']}: %{{y:.1%}}"
            "<extra></extra>"
        )

    else:

        fig.update_yaxes(
            tickprefix="R$ ",
            tickformat=",.0f"
        )

        fig.update_traces(
            hovertemplate=
            "<b>%{customdata[0]}</b><br>"
            "Semana: %{x}<br>"
            "Vendas: R$ %{y:,.0f}"
            "<extra></extra>"
        )

    # Linha zero para indicadores %
    if config["formato"] == "%":

        fig.add_hline(
            y=0,
            line_dash="dash",
            annotation_text="0%"
        )

    fig.update_layout(
        height=520,
        hovermode="x unified",
        xaxis_title="",
        yaxis_title="",
        legend_title="Lojas",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="grafico_principal"
    )

else:

    st.info(
        "Não existem dados para o indicador selecionado."
    )

# =========================================================
# TABELA INTERATIVA
# =========================================================

st.divider()

st.subheader(
    f"Detalhamento — {config['titulo']}"
)

# Pivot para colocar as semanas lado a lado

if not df_f.empty:

    tabela = df_f.pivot(
        index="Nome_Loja",
        columns="Semana",
        values=coluna
    )

    # Ordenação das semanas
    ordem_colunas = [
        s for s in ["W36", "W37", "W38"]
        if s in tabela.columns
    ]

    tabela = tabela[ordem_colunas]

    # -----------------------------------------------------
    # FORMATAÇÃO
    # -----------------------------------------------------

    if config["formato"] == "%":

        tabela_formatada = tabela.style.format(
            lambda x:
            "" if pd.isna(x)
            else f"{x:+.1%}".replace(".", ",")
        )

    else:

        tabela_formatada = tabela.style.format(
            lambda x:
            "" if pd.isna(x)
            else f"R$ {x:,.0f}".replace(",", ".")
        )

    st.dataframe(
        tabela_formatada,
        use_container_width=True,
        height=400
    )

# =========================================================
# VISÃO MULTI-INDICADORES
# =========================================================

st.divider()

st.subheader("Evolução dos indicadores")

st.caption(
    "Selecione uma loja para analisar todos os indicadores simultaneamente."
)

loja_detalhe = st.selectbox(
    "Loja para detalhamento",
    sorted(df_f["Nome_Loja"].unique())
    if not df_f.empty else []
)

if loja_detalhe:

    df_loja = df_f[
        df_f["Nome_Loja"] == loja_detalhe
    ].sort_values("Ordem")

    col1, col2 = st.columns(2)

    # =====================================================
    # VENDAS
    # =====================================================

    with col1:

        fig_vendas = px.line(
            df_loja,
            x="Semana",
            y="Vendas",
            markers=True
        )

        fig_vendas.update_traces(
            hovertemplate=
            "Semana: %{x}<br>"
            "Vendas: R$ %{y:,.0f}"
            "<extra></extra>"
        )

        fig_vendas.update_layout(
            title="Vendas",
            height=330,
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig_vendas,
            use_container_width=True
        )

    # =====================================================
    # % BASE
    # =====================================================

    with col2:

        fig_base = px.line(
            df_loja,
            x="Semana",
            y="% Base",
            markers=True
        )

        fig_base.update_yaxes(
            tickformat=".1%"
        )

        fig_base.update_layout(
            title="% Base",
            height=330,
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig_base,
            use_container_width=True
        )

    col3, col4 = st.columns(2)

    # =====================================================
    # VENDAS VS LY
    # =====================================================

    with col3:

        dados = df_loja.dropna(
            subset=["Vendas Vs LY %"]
        )

        if not dados.empty:

            fig = px.line(
                dados,
                x="Semana",
                y="Vendas Vs LY %",
                markers=True
            )

            fig.add_hline(
                y=0,
                line_dash="dash"
            )

            fig.update_yaxes(
                tickformat=".1%"
            )

            fig.update_layout(
                title="Vendas Vs LY",
                height=330,
                xaxis_title="",
                yaxis_title=""
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # =====================================================
    # FLUXO
    # =====================================================

    with col4:

        dados = df_loja.dropna(
            subset=["Fluxo Vs LY %"]
        )

        if not dados.empty:

            fig = px.line(
                dados,
                x="Semana",
                y="Fluxo Vs LY %",
                markers=True
            )

            fig.add_hline(
                y=0,
                line_dash="dash"
            )

            fig.update_yaxes(
                tickformat=".1%"
            )

            fig.update_layout(
                title="Fluxo Vs LY",
                height=330,
                xaxis_title="",
                yaxis_title=""
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # =====================================================
    # CONVERSÃO
    # =====================================================

    dados = df_loja.dropna(
        subset=["Conversão Vs LY %"]
    )

    if not dados.empty:

        fig = px.line(
            dados,
            x="Semana",
            y="Conversão Vs LY %",
            markers=True
        )

        fig.add_hline(
            y=0,
            line_dash="dash"
        )

        fig.update_yaxes(
            tickformat=".1%"
        )

        fig.update_layout(
            title="Conversão Vs LY",
            height=330,
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================================================
# EXPORTAÇÃO
# =========================================================

st.divider()

csv = df_f.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    "Baixar dados filtrados",
    csv,
    "evolucao_sp_capital.csv",
    "text/csv"
)
