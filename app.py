import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


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

.stApp {
    background-color: #f8fafc;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* HEADER */

.main-title {
    font-size: 30px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 3px;
}

.subtitle {
    color: #64748b;
    font-size: 14px;
    font-weight: 500;
}

/* CARDS */

.kpi-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    min-height: 108px;
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
}

.kpi-label {
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: .07em;
}

.kpi-value {
    font-size: 25px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 8px;
}

.kpi-sub {
    font-size: 12px;
    color: #64748b;
    margin-top: 3px;
}

/* BANNER */

.info-banner {
    background: #eef2ff;
    border: 1px solid #c7d2fe;
    color: #3730a3;
    padding: 11px 15px;
    border-radius: 9px;
    font-size: 13px;
    font-weight: 500;
}

/* SECTION */

.section-title {
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 8px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 15px;
}

/* MATRIX */

.matrix-wrapper {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow-x: auto;
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
}

.matrix-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    min-width: 850px;
}

.matrix-table th {
    background: #1e293b;
    color: white;
    padding: 13px 16px;
    font-size: 12px;
    font-weight: 700;
    text-align: right;
    border-bottom: 2px solid #0f172a;
}

.matrix-table th:first-child {
    text-align: left;
}

.matrix-table td {
    padding: 9px 16px;
    border-bottom: 1px solid #f1f5f9;
    font-size: 13px;
}

.matrix-table td:not(:first-child) {
    text-align: right;
    font-variant-numeric: tabular-nums;
}

.matrix-table tbody tr:not(.store-row):hover {
    background: #f8fafc;
}

.store-row td {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    padding: 10px 16px;
    border-top: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
}

.metric-name {
    color: #475569;
    font-weight: 500;
}

.ytd {
    background: #fafafa;
    font-weight: 700;
    color: #0f172a;
}

.positive {
    color: #059669;
    font-weight: 700;
}

.negative {
    color: #e11d48;
    font-weight: 700;
}

.neutral {
    color: #475569;
    font-weight: 600;
}

.na {
    color: #94a3b8;
    font-weight: 400;
}

.new-store {
    display: inline-block;
    margin-left: 8px;
    padding: 3px 8px;
    border-radius: 5px;
    background: #eff6ff;
    color: #0369a1;
    border: 1px solid #bae6fd;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .03em;
}

/* STREAMLIT */

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DADOS
# ============================================================

dados = [
    ["ANF", "ANF — SHOPPING ANÁLIA FRANCO", False,
     994493, 1034280, 256394,
     0.071, 0.210, -0.029,
     0.169, 0.275, 0.161,
     0.053, 0.232, 0.218,
     0.022, -0.071, -0.128,
     2285168, 0.116, 0.214, 0.149, -0.039],

    ["APL", "APL — PAULISTA", True,
     1058906, 787733, 353081,
     0.094, -0.202, 0.026,
     None, None, None,
     None, None, None,
     None, None, None,
     2199720, 0.112, None, None, None],

    ["SCN", "SCN — SHOPPING CENTER NORTE", False,
     1676354, 1807131, 478941,
     0.010, 0.075, -0.161,
     -0.063, -0.008, -0.084,
     -0.134, -0.021, -0.138,
     0.090, -0.016, 0.072,
     3962426, 0.013, -0.042, -0.086, 0.039],

    ["MRB", "MRB — SHOPPING MORUMBI", False,
     1439788, 1448346, 471330,
     -0.079, 0.047, 0.033,
     -0.108, -0.104, -0.061,
     0.003, 0.057, 0.047,
     -0.048, -0.116, -0.065,
     3359464, -0.021, -0.091, 0.036, -0.076],

    ["SCS", "SCS — PARK SHOPPING SÃO CAETANO", False,
     589146, 608027, 148215,
     -0.039, 0.036, -0.044,
     0.123, 0.112, 0.156,
     -0.022, 0.166, 0.149,
     0.015, -0.116, -0.079,
     1345387, -0.007, 0.122, 0.079, -0.058],

    ["SPE", "SPE — SHOPPING ELDORADO", False,
     673999, 676235, 203512,
     -0.298, -0.195, -0.312,
     -0.053, -0.031, -0.093,
     -0.073, 0.040, -0.002,
     0.083, -0.024, -0.005,
     1553746, -0.248, -0.052, -0.012, 0.018],

    ["TBE", "TBE — SHOPPING TAMBORÉ", False,
     851884, 883374, 240063,
     -0.106, -0.063, -0.184,
     0.043, 0.087, -0.020,
     0.066, 0.249, 0.154,
     0.025, -0.087, -0.100,
     1975321, -0.101, 0.051, 0.156, -0.054],

    ["IGT", "IGT — SHOPPING IGUATEMI SP", False,
     601414, 600206, 228348,
     -0.124, -0.002, -0.223,
     -0.173, -0.182, -0.085,
     -0.263, -0.250, -0.153,
     0.212, 0.066, 0.087,
     1429968, -0.116, -0.158, -0.222, 0.122],

    ["SBO", "SBO — SHOPPING BOURBON POMPÉIA", False,
     531865, 546099, 158404,
     -0.202, -0.211, -0.243,
     -0.329, -0.264, -0.197,
     0.183, 0.231, 0.197,
     -0.395, -0.380, -0.385,
     1236368, -0.218, -0.283, 0.203, -0.387]
]


columns = [
    "ID",
    "LOJA",
    "NOVA",

    "VENDAS_W36",
    "VENDAS_W37",
    "VENDAS_W38",

    "BASE_W36",
    "BASE_W37",
    "BASE_W38",

    "VENDAS_LY_W36",
    "VENDAS_LY_W37",
    "VENDAS_LY_W38",

    "FLUXO_LY_W36",
    "FLUXO_LY_W37",
    "FLUXO_LY_W38",

    "CONVERSAO_LY_W36",
    "CONVERSAO_LY_W37",
    "CONVERSAO_LY_W38",

    "VENDAS_YTD",
    "BASE_YTD",
    "VENDAS_LY_YTD",
    "FLUXO_LY_YTD",
    "CONVERSAO_LY_YTD"
]

df = pd.DataFrame(dados, columns=columns)


# ============================================================
# FORMATAÇÃO
# ============================================================

def fmt_number(value):
    if pd.isna(value):
        return "N/A"

    return (
        f"{value:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def fmt_pct(value, signed=False):

    if pd.isna(value):
        return "N/A"

    if signed:
        return f"{value:+.2%}".replace(".", ",")

    return f"{value:.2%}".replace(".", ",")


def pct_class(value):

    if pd.isna(value):
        return "na"

    if value > 0:
        return "positive"

    if value < 0:
        return "negative"

    return "neutral"


def fmt_money(value):

    if pd.isna(value):
        return "N/A"

    return (
        "R$ "
        + f"{value:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div style="
background:white;
border:1px solid #e2e8f0;
border-radius:12px;
padding:22px;
margin-bottom:16px;
">

<div class="main-title">
Matriz de Performance — SP Capital
</div>

<div class="subtitle">
Visão tabular por loja e sub-métricas operacionais · W36 a W38
</div>

</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="info-banner">
<strong>APL — Paulista:</strong>
inaugurada em 2026. Comparativos Vs LY não se aplicam.
</div>
""", unsafe_allow_html=True)

st.write("")


# ============================================================
# FILTROS
# ============================================================

col1, col2, col3 = st.columns([1.5, 2.2, 1.3])

with col1:

    busca = st.text_input(
        "Buscar loja",
        placeholder="Código ou nome..."
    )

with col2:

    lojas_selecionadas = st.multiselect(
        "Lojas",
        options=df["ID"].tolist(),
        default=df["ID"].tolist(),
        format_func=lambda x: x
    )

with col3:

    modo = st.radio(
        "Visualização",
        ["Matriz", "Análises"],
        horizontal=True
    )


# ============================================================
# FILTRO
# ============================================================

df_filtrado = df.copy()

if busca:

    termo = busca.lower()

    df_filtrado = df_filtrado[
        df_filtrado["ID"].str.lower().str.contains(termo) |
        df_filtrado["LOJA"].str.lower().str.contains(termo)
    ]

if lojas_selecionadas:

    df_filtrado = df_filtrado[
        df_filtrado["ID"].isin(lojas_selecionadas)
    ]

else:

    df_filtrado = df.iloc[0:0]


# ============================================================
# KPIs
# ============================================================

total_vendas = df_filtrado["VENDAS_YTD"].sum()

if len(df_filtrado):

    top_store = df_filtrado.loc[
        df_filtrado["VENDAS_YTD"].idxmax()
    ]

else:

    top_store = None


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-label">
            Vendas Totais Regional
        </div>

        <div class="kpi-value">
            {fmt_money(total_vendas)}
        </div>

        <div class="kpi-sub">
            Lojas selecionadas · YTD
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    if top_store is not None:

        st.markdown(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Maior Volume
            </div>

            <div class="kpi-value">
                {top_store["ID"]}
            </div>

            <div class="kpi-sub">
                {fmt_money(top_store["VENDAS_YTD"])}
            </div>

        </div>
        """, unsafe_allow_html=True)


with c3:

    st.markdown("""
    <div class="kpi-card">

        <div class="kpi-label">
            Maior Crescimento Vs LY
        </div>

        <div class="kpi-value">
            ANF
        </div>

        <div class="kpi-sub">
            +21,40% YTD Vs LY
        </div>

    </div>
    """, unsafe_allow_html=True)


with c4:

    apl = df[df["ID"] == "APL"].iloc[0]

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-label">
            Inauguração 2026
        </div>

        <div class="kpi-value" style="color:#0369a1;">
            APL
        </div>

        <div class="kpi-sub">
            {fmt_money(apl["VENDAS_YTD"])}
        </div>

    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# MATRIZ
# ============================================================

if modo == "Matriz":

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

    if len(df_filtrado) == 0:

        st.warning(
            "Nenhuma loja encontrada com os filtros selecionados."
        )

    else:

        # ====================================================
        # CONSTRUÇÃO DA MATRIZ
        # ====================================================

        linhas = []

        for _, row in df_filtrado.iterrows():

            badge = ""

            if row["NOVA"]:

                badge = """
                <span class="new-store">
                    INAUGURAÇÃO 2026 · SEM LY
                </span>
                """

            # Loja
            linhas.append(f"""
            <tr class="store-row">
                <td colspan="5">
                    {row["LOJA"]}
                    {badge}
                </td>
            </tr>
            """)

            # Vendas
            linhas.append(f"""
            <tr>
                <td class="metric-name">Vendas</td>
                <td>{fmt_number(row["VENDAS_W36"])}</td>
                <td>{fmt_number(row["VENDAS_W37"])}</td>
                <td>{fmt_number(row["VENDAS_W38"])}</td>
                <td class="ytd">{fmt_number(row["VENDAS_YTD"])}</td>
            </tr>
            """)

            # Base
            linhas.append(f"""
            <tr>
                <td class="metric-name">% Base</td>
                <td>{fmt_pct(row["BASE_W36"])}</td>
                <td>{fmt_pct(row["BASE_W37"])}</td>
                <td>{fmt_pct(row["BASE_W38"])}</td>
                <td class="ytd">{fmt_pct(row["BASE_YTD"])}</td>
            </tr>
            """)

            # Vendas LY
            valores = [
                row["VENDAS_LY_W36"],
                row["VENDAS_LY_W37"],
                row["VENDAS_LY_W38"],
                row["VENDAS_LY_YTD"]
            ]

            html_cells = ""

            for i, value in enumerate(valores):

                classe = pct_class(value)

                if i == 3:
                    classe += " ytd"

                html_cells += f"""
                <td class="{classe}">
                    {fmt_pct(value, signed=True)}
                </td>
                """

            linhas.append(
                f"""
                <tr>
                    <td class="metric-name">
                        Vendas Vs LY %
                    </td>
                    {html_cells}
                </tr>
                """
            )

            # Fluxo LY
            valores = [
                row["FLUXO_LY_W36"],
                row["FLUXO_LY_W37"],
                row["FLUXO_LY_W38"],
                row["FLUXO_LY_YTD"]
            ]

            html_cells = ""

            for i, value in enumerate(valores):

                classe = pct_class(value)

                if i == 3:
                    classe += " ytd"

                html_cells += f"""
                <td class="{classe}">
                    {fmt_pct(value, signed=True)}
                </td>
                """

            linhas.append(
                f"""
                <tr>
                    <td class="metric-name">
                        Fluxo Vs LY %
                    </td>
                    {html_cells}
                </tr>
                """
            )

            # Conversão LY
            valores = [
                row["CONVERSAO_LY_W36"],
                row["CONVERSAO_LY_W37"],
                row["CONVERSAO_LY_W38"],
                row["CONVERSAO_LY_YTD"]
            ]

            html_cells = ""

            for i, value in enumerate(valores):

                classe = pct_class(value)

                if i == 3:
                    classe += " ytd"

                html_cells += f"""
                <td class="{classe}">
                    {fmt_pct(value, signed=True)}
                </td>
                """

            linhas.append(
                f"""
                <tr>
                    <td class="metric-name">
                        Conversão Vs LY %
                    </td>
                    {html_cells}
                </tr>
                """
            )

        tabela_html = f"""
        <div class="matrix-wrapper">

            <table class="matrix-table">

                <thead>

                    <tr>
                        <th style="text-align:left;">
                            LOJA / MÉTRICA
                        </th>

                        <th>
                            26 / W36
                        </th>

                        <th>
                            26 / W37
                        </th>

                        <th>
                            26 / W38
                        </th>

                        <th>
                            YTD SETEMBRO
                        </th>

                    </tr>

                </thead>

                <tbody>

                    {''.join(linhas)}

                </tbody>

            </table>

        </div>
        """

        # IMPORTANTE:
        # O HTML inteiro precisa estar em UM ÚNICO st.markdown
        st.markdown(
            tabela_html,
            unsafe_allow_html=True
        )


# ============================================================
# ANÁLISES
# ============================================================

else:

    st.markdown(
        '<div class="section-title">Análise Interativa</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Explore a evolução dos indicadores por loja e semana'
        '</div>',
        unsafe_allow_html=True
    )

    indicador = st.radio(
        "Indicador",
        [
            "Vendas",
            "% Base",
            "Vendas Vs LY",
            "Fluxo Vs LY",
            "Conversão Vs LY"
        ],
        horizontal=True
    )

    mapa = {

        "Vendas": [
            "VENDAS_W36",
            "VENDAS_W37",
            "VENDAS_W38"
        ],

        "% Base": [
            "BASE_W36",
            "BASE_W37",
            "BASE_W38"
        ],

        "Vendas Vs LY": [
            "VENDAS_LY_W36",
            "VENDAS_LY_W37",
            "VENDAS_LY_W38"
        ],

        "Fluxo Vs LY": [
            "FLUXO_LY_W36",
            "FLUXO_LY_W37",
            "FLUXO_LY_W38"
        ],

        "Conversão Vs LY": [
            "CONVERSAO_LY_W36",
            "CONVERSAO_LY_W37",
            "CONVERSAO_LY_W38"
        ]
    }

    campos = mapa[indicador]

    chart_rows = []

    for _, row in df_filtrado.iterrows():

        for semana, campo in zip(
            ["W36", "W37", "W38"],
            campos
        ):

            chart_rows.append({
                "Loja": row["ID"],
                "Nome": row["LOJA"],
                "Semana": semana,
                "Valor": row[campo]
            })

    chart_df = pd.DataFrame(chart_rows)

    # ========================================================
    # GRÁFICO
    # ========================================================

    fig = go.Figure()

    for loja in chart_df["Loja"].unique():

        temp = chart_df[
            chart_df["Loja"] == loja
        ].copy()

        fig.add_trace(
            go.Scatter(
                x=temp["Semana"],
                y=temp["Valor"],
                mode="lines+markers",
                name=loja,
                connectgaps=False,
                line=dict(width=3),
                marker=dict(size=8),
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Semana: %{x}<br>"
                    "Valor: R$ %{y:,.0f}"
                    "<extra></extra>"
                )
                if indicador == "Vendas"
                else (
                    "<b>%{fullData.name}</b><br>"
                    "Semana: %{x}<br>"
                    "Valor: %{y:.2%}"
                    "<extra></extra>"
                )
            )
        )

    fig.update_layout(
        height=500,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        xaxis=dict(
            categoryorder="array",
            categoryarray=["W36", "W37", "W38"]
        ),
        yaxis=dict(
            title="R$" if indicador == "Vendas" else "%",
            tickformat=", .0f" if indicador == "Vendas" else ".0%",
            gridcolor="#e2e8f0"
        )
    )

    if indicador != "Vendas":

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_width=1,
            line_color="#94a3b8"
        )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False
        }
    )


    # ========================================================
    # HEATMAP
    # ========================================================

    st.markdown(
        '<div class="section-title">Comparativo por Loja</div>',
        unsafe_allow_html=True
    )

    heatmap = chart_df.pivot(
        index="Loja",
        columns="Semana",
        values="Valor"
    )

    heatmap = heatmap.reindex(
        columns=["W36", "W37", "W38"]
    )

    if indicador == "Vendas":

        fig_heat = px.imshow(
            heatmap,
            text_auto=".0f",
            aspect="auto"
        )

    else:

        fig_heat = px.imshow(
            heatmap,
            text_auto=".1%",
            aspect="auto",
            color_continuous_midpoint=0
        )

    fig_heat.update_layout(
        height=420,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True,
        config={
            "displaylogo": False
        }
    )


# ============================================================
# EXPORTAÇÃO
# ============================================================

st.divider()

csv = df_filtrado.to_csv(
    index=False,
    sep=";",
    decimal=","
).encode("utf-8-sig")

st.download_button(
    label="⬇ Exportar dados CSV",
    data=csv,
    file_name="matriz_performance_sp_capital.csv",
    mime="text/csv"
)
