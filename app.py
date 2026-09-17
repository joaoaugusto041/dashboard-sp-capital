import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 1. CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Evolução Regional — SP Capital",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. BASE DE DADOS
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

    lojas_map = {
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

    df["Nome_Loja"] = df["Loja"].map(lojas_map)

    ordem_semanas = {
        "W36": 1,
        "W37": 2,
        "W38": 3
    }

    df["Ordem_Semana"] = df["Semana"].map(ordem_semanas)

    return df


df = load_data()

# =========================================================
# 3. CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    color: #666;
    font-size: 15px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 10px;
}

.kpi-title {
    font-size: 13px;
    color: #666;
}

.kpi-value {
    font-size: 27px;
    font-weight: 700;
}

.kpi-sub {
    font-size: 12px;
    color: #777;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 4. SIDEBAR
# =========================================================

st.sidebar.title("Filtros")

lojas = sorted(df["Nome_Loja"].unique())

loja_selecionada = st.sidebar.selectbox(
    "Loja em análise",
    options=["Todas as lojas"] + lojas
)

semanas = ["W36", "W37", "W38"]

semanas_selecionadas = st.sidebar.multiselect(
    "Semanas",
    options=semanas,
    default=semanas
)

st.sidebar.divider()

st.sidebar.caption(
    f"{len(lojas)} lojas disponíveis"
)

st.sidebar.caption(
    f"{len(semanas_selecionadas)} semanas selecionadas"
)

# =========================================================
# 5. FILTRO
# =========================================================

df_filtered = df[
    df["Semana"].isin(semanas_selecionadas)
].copy()

if loja_selecionada != "Todas as lojas":
    df_filtered = df_filtered[
        df_filtered["Nome_Loja"] == loja_selecionada
    ]

df_filtered = df_filtered.sort_values(
    ["Ordem_Semana"]
)

# =========================================================
# 6. CABEÇALHO
# =========================================================

st.markdown(
    '<div class="main-title">EVOLUÇÃO REGIONAL — SP CAPITAL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Acompanhamento semanal dos principais indicadores por loja | YTD 2026</div>',
    unsafe_allow_html=True
)

# =========================================================
# 7. RESUMO DA LOJA SELECIONADA
# =========================================================

if loja_selecionada != "Todas as lojas" and not df_filtered.empty:

    ultima = df_filtered.sort_values("Ordem_Semana").iloc[-1]

    vendas = ultima["Vendas"]
    base = ultima["% Base"]
    vendas_ly = ultima["Vendas Vs LY %"]
    fluxo = ultima["Fluxo Vs LY %"]
    conversao = ultima["Conversão Vs LY %"]

    st.markdown(
        f"### {loja_selecionada}"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Vendas",
            f"R$ {vendas:,.0f}".replace(",", ".")
        )

    with c2:
        st.metric(
            "% Base",
            f"{base:.1%}".replace(".", ",")
        )

    with c3:
        st.metric(
            "Vendas Vs LY",
            "N/A" if pd.isna(vendas_ly)
            else f"{vendas_ly:+.1%}".replace(".", ",")
        )

    with c4:
        st.metric(
            "Fluxo Vs LY",
            "N/A" if pd.isna(fluxo)
            else f"{fluxo:+.1%}".replace(".", ",")
        )

    with c5:
        st.metric(
            "Conversão Vs LY",
            "N/A" if pd.isna(conversao)
            else f"{conversao:+.1%}".replace(".", ",")
        )

# =========================================================
# 8. VISÃO GERAL — TODAS AS LOJAS
# =========================================================

if loja_selecionada == "Todas as lojas":

    st.markdown(
        '<div class="section-title">Visão Geral — Evolução por Loja</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # VENDAS
    # -----------------------------------------------------

    fig = px.line(
        df_filtered.sort_values("Ordem_Semana"),
        x="Semana",
        y="Vendas",
        color="Loja",
        markers=True,
        hover_data=["Nome_Loja"]
    )

    fig.update_layout(
        height=430,
        xaxis_title="Semana",
        yaxis_title="Vendas (R$)",
        legend_title="Loja",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # INDICADORES VS LY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">Indicadores Vs LY</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_fluxo = px.line(
            df_filtered.dropna(subset=["Fluxo Vs LY %"]),
            x="Semana",
            y="Fluxo Vs LY %",
            color="Loja",
            markers=True,
            hover_data=["Nome_Loja"]
        )

        fig_fluxo.add_hline(
            y=0,
            line_dash="dash"
        )

        fig_fluxo.update_layout(
            height=380,
            xaxis_title="Semana",
            yaxis_title="Fluxo Vs LY"
        )

        st.plotly_chart(
            fig_fluxo,
            use_container_width=True
        )

    with col2:

        fig_conv = px.line(
            df_filtered.dropna(subset=["Conversão Vs LY %"]),
            x="Semana",
            y="Conversão Vs LY %",
            color="Loja",
            markers=True,
            hover_data=["Nome_Loja"]
        )

        fig_conv.add_hline(
            y=0,
            line_dash="dash"
        )

        fig_conv.update_layout(
            height=380,
            xaxis_title="Semana",
            yaxis_title="Conversão Vs LY"
        )

        st.plotly_chart(
            fig_conv,
            use_container_width=True
        )

# =========================================================
# 9. VISÃO DETALHADA DA LOJA
# =========================================================

else:

    if df_filtered.empty:

        st.warning(
            "Não existem dados para os filtros selecionados."
        )

    else:

        st.markdown(
            '<div class="section-title">Evolução dos Indicadores</div>',
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # VENDAS
        # -------------------------------------------------

        st.markdown("#### Vendas")

        fig_vendas = px.line(
            df_filtered,
            x="Semana",
            y="Vendas",
            markers=True,
            text="Vendas"
        )

        fig_vendas.update_traces(
            texttemplate="R$ %{text:,.0f}",
            textposition="top center"
        )

        fig_vendas.update_layout(
            height=350,
            xaxis_title="",
            yaxis_title="R$",
            showlegend=False
        )

        st.plotly_chart(
            fig_vendas,
            use_container_width=True
        )

        # -------------------------------------------------
        # % BASE
        # -------------------------------------------------

        st.markdown("#### % Base")

        fig_base = px.line(
            df_filtered,
            x="Semana",
            y="% Base",
            markers=True,
            text="% Base"
        )

        fig_base.update_traces(
            texttemplate="%{text:.1%}",
            textposition="top center"
        )

        fig_base.update_layout(
            height=300,
            xaxis_title="",
            yaxis_title="% Base",
            showlegend=False
        )

        st.plotly_chart(
            fig_base,
            use_container_width=True
        )

        # -------------------------------------------------
        # VENDAS VS LY
        # -------------------------------------------------

        st.markdown("#### Vendas Vs LY")

        dados = df_filtered.dropna(
            subset=["Vendas Vs LY %"]
        )

        if not dados.empty:

            fig = px.line(
                dados,
                x="Semana",
                y="Vendas Vs LY %",
                markers=True,
                text="Vendas Vs LY %"
            )

            fig.add_hline(
                y=0,
                line_dash="dash"
            )

            fig.update_traces(
                texttemplate="%{text:.1%}",
                textposition="top center"
            )

            fig.update_layout(
                height=300,
                xaxis_title="",
                yaxis_title="Vs LY",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Não há histórico LY disponível para esta loja."
            )

        # -------------------------------------------------
        # FLUXO
        # -------------------------------------------------

        st.markdown("#### Fluxo Vs LY")

        dados = df_filtered.dropna(
            subset=["Fluxo Vs LY %"]
        )

        if not dados.empty:

            fig = px.line(
                dados,
                x="Semana",
                y="Fluxo Vs LY %",
                markers=True,
                text="Fluxo Vs LY %"
            )

            fig.add_hline(
                y=0,
                line_dash="dash"
            )

            fig.update_traces(
                texttemplate="%{text:.1%}",
                textposition="top center"
            )

            fig.update_layout(
                height=300,
                xaxis_title="",
                yaxis_title="Vs LY",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------------------------------
        # CONVERSÃO
        # -------------------------------------------------

        st.markdown("#### Conversão Vs LY")

        dados = df_filtered.dropna(
            subset=["Conversão Vs LY %"]
        )

        if not dados.empty:

            fig = px.line(
                dados,
                x="Semana",
                y="Conversão Vs LY %",
                markers=True,
                text="Conversão Vs LY %"
            )

            fig.add_hline(
                y=0,
                line_dash="dash"
            )

            fig.update_traces(
                texttemplate="%{text:.1%}",
                textposition="top center"
            )

            fig.update_layout(
                height=300,
                xaxis_title="",
                yaxis_title="Vs LY",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# =========================================================
# 10. TABELA DE EVOLUÇÃO
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">Tabela de Evolução</div>',
    unsafe_allow_html=True
)

tabela = df_filtered[
    [
        "Nome_Loja",
        "Semana",
        "Vendas",
        "% Base",
        "Vendas Vs LY %",
        "Fluxo Vs LY %",
        "Conversão Vs LY %"
    ]
].copy()

tabela.columns = [
    "Loja",
    "Semana",
    "Vendas",
    "% Base",
    "Vendas Vs LY",
    "Fluxo Vs LY",
    "Conversão Vs LY"
]

tabela["Vendas"] = tabela["Vendas"].map(
    lambda x: f"R$ {x:,.0f}".replace(",", ".")
)

for coluna in [
    "% Base",
    "Vendas Vs LY",
    "Fluxo Vs LY",
    "Conversão Vs LY"
]:

    tabela[coluna] = tabela[coluna].apply(
        lambda x: ""
        if pd.isna(x)
        else f"{x:+.1%}".replace(".", ",")
    )

st.dataframe(
    tabela,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# 11. DOWNLOAD
# =========================================================

csv = df_filtered.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="Baixar dados filtrados",
    data=csv,
    file_name="evolucao_sp_capital.csv",
    mime="text/csv"
)
