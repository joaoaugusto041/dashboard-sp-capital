import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Executivo — SP Capital",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. BASE DE DADOS OFICIAL (27 REGISTROS)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    raw_data = [
        {"Loja": "ANF", "Vendas": 1034280, "% Base": 0.210, "Vendas Vs LY %": 0.275, "Fluxo Vs LY %": 0.232, "Conversão Vs LY %": -0.071, "Semana": "26 / W37"},
        {"Loja": "APL", "Vendas": 1058906, "% Base": 0.094, "Vendas Vs LY %": None,   "Fluxo Vs LY %": None,   "Conversão Vs LY %": None,   "Semana": "26 / W36"},
        {"Loja": "SCN", "Vendas": 1807131, "% Base": 0.075, "Vendas Vs LY %": -0.008, "Fluxo Vs LY %": -0.021, "Conversão Vs LY %": -0.016, "Semana": "26 / W37"},
        {"Loja": "ANF", "Vendas": 994493,  "% Base": 0.071, "Vendas Vs LY %": 0.169, "Fluxo Vs LY %": 0.053, "Conversão Vs LY %": 0.022,  "Semana": "26 / W36"},
        {"Loja": "MRB", "Vendas": 1448346, "% Base": 0.047, "Vendas Vs LY %": -0.104, "Fluxo Vs LY %": 0.057, "Conversão Vs LY %": -0.116, "Semana": "26 / W37"},
        {"Loja": "SCS", "Vendas": 608027,  "% Base": 0.036, "Vendas Vs LY %": 0.112, "Fluxo Vs LY %": 0.166, "Conversão Vs LY %": -0.116, "Semana": "26 / W37"},
        {"Loja": "MRB", "Vendas": 471330,  "% Base": 0.033, "Vendas Vs LY %": -0.061, "Fluxo Vs LY %": 0.047, "Conversão Vs LY %": -0.065, "Semana": "26 / W38"},
        {"Loja": "APL", "Vendas": 353081,  "% Base": 0.026, "Vendas Vs LY %": None,   "Fluxo Vs LY %": None,   "Conversão Vs LY %": None,   "Semana": "26 / W38"},
        {"Loja": "SCN", "Vendas": 1676354, "% Base": 0.010, "Vendas Vs LY %": -0.063, "Fluxo Vs LY %": -0.134, "Conversão Vs LY %": 0.090,  "Semana": "26 / W36"},
        {"Loja": "IGT", "Vendas": 600206,  "% Base": -0.002,"Vendas Vs LY %": -0.182, "Fluxo Vs LY %": -0.250, "Conversão Vs LY %": 0.066,  "Semana": "26 / W37"},
        {"Loja": "ANF", "Vendas": 256394,  "% Base": -0.029,"Vendas Vs LY %": 0.161, "Fluxo Vs LY %": 0.218, "Conversão Vs LY %": -0.128, "Semana": "26 / W38"},
        {"Loja": "SCS", "Vendas": 589146,  "% Base": -0.039,"Vendas Vs LY %": 0.123, "Fluxo Vs LY %": -0.022, "Conversão Vs LY %": 0.015,  "Semana": "26 / W36"},
        {"Loja": "SCS", "Vendas": 148215,  "% Base": -0.044,"Vendas Vs LY %": 0.156, "Fluxo Vs LY %": 0.149, "Conversão Vs LY %": -0.079, "Semana": "26 / W38"},
        {"Loja": "TBE", "Vendas": 883374,  "% Base": -0.063,"Vendas Vs LY %": 0.087, "Fluxo Vs LY %": 0.249, "Conversão Vs LY %": -0.087, "Semana": "26 / W37"},
        {"Loja": "MRB", "Vendas": 1439788, "% Base": -0.079,"Vendas Vs LY %": -0.108, "Fluxo Vs LY %": 0.003, "Conversão Vs LY %": -0.048, "Semana": "26 / W36"},
        {"Loja": "TBE", "Vendas": 851884,  "% Base": -0.106,"Vendas Vs LY %": 0.043, "Fluxo Vs LY %": 0.066, "Conversão Vs LY %": 0.025,  "Semana": "26 / W36"},
        {"Loja": "IGT", "Vendas": 601414,  "% Base": -0.124,"Vendas Vs LY %": -0.173, "Fluxo Vs LY %": -0.263, "Conversão Vs LY %": 0.212,  "Semana": "26 / W36"},
        {"Loja": "SCN", "Vendas": 478941,  "% Base": -0.161,"Vendas Vs LY %": -0.084, "Fluxo Vs LY %": -0.138, "Conversão Vs LY %": 0.072,  "Semana": "26 / W38"},
        {"Loja": "TBE", "Vendas": 240063,  "% Base": -0.184,"Vendas Vs LY %": -0.020, "Fluxo Vs LY %": 0.154, "Conversão Vs LY %": -0.100, "Semana": "26 / W38"},
        {"Loja": "SPE", "Vendas": 676235,  "% Base": -0.195,"Vendas Vs LY %": -0.031, "Fluxo Vs LY %": 0.040, "Conversão Vs LY %": -0.024, "Semana": "26 / W37"},
        {"Loja": "APL", "Vendas": 787733,  "% Base": -0.202,"Vendas Vs LY %": None,   "Fluxo Vs LY %": None,   "Conversão Vs LY %": None,   "Semana": "26 / W37"},
        {"Loja": "SBO", "Vendas": 531865,  "% Base": -0.202,"Vendas Vs LY %": -0.329, "Fluxo Vs LY %": 0.183, "Conversão Vs LY %": -0.395, "Semana": "26 / W36"},
        {"Loja": "SBO", "Vendas": 546099,  "% Base": -0.211,"Vendas Vs LY %": -0.264, "Fluxo Vs LY %": 0.231, "Conversão Vs LY %": -0.380, "Semana": "26 / W37"},
        {"Loja": "IGT", "Vendas": 228348,  "% Base": -0.223,"Vendas Vs LY %": -0.085, "Fluxo Vs LY %": -0.153, "Conversão Vs LY %": 0.087,  "Semana": "26 / W38"},
        {"Loja": "SBO", "Vendas": 158404,  "% Base": -0.243,"Vendas Vs LY %": -0.265, "Fluxo Vs LY %": 0.197, "Conversão Vs LY %": -0.385, "Semana": "26 / W38"},
        {"Loja": "SPE", "Vendas": 673999,  "% Base": -0.298,"Vendas Vs LY %": -0.053, "Fluxo Vs LY %": -0.073, "Conversão Vs LY %": 0.083,  "Semana": "26 / W36"},
        {"Loja": "SPE", "Vendas": 203512,  "% Base": -0.312,"Vendas Vs LY %": -0.093, "Fluxo Vs LY %": -0.002, "Conversão Vs LY %": -0.005, "Semana": "26 / W38"},
    ]
    
    df = pd.DataFrame(raw_data)
    
    lojas_map = {
        "ANF": "ANF - Shopping Anália Franco",
        "APL": "APL - Paulista (Nova Loja 2026)",
        "IGT": "IGT - Shopping Iguatemi SP",
        "MRB": "MRB - Shopping Morumbi",
        "SBO": "SBO - Shopping Bourbon Pompéia",
        "SCN": "SCN - Shopping Center Norte",
        "SCS": "SCS - Park Shopping São Caetano",
        "SPE": "SPE - Shopping Eldorado",
        "TBE": "TBE - Shopping Tamboré"
    }
    
    df["Nome_Loja"] = df["Loja"].map(lojas_map)
    return df

df_data = load_data()

# ---------------------------------------------------------
# 3. FILTROS NA BARRA LATERAL (SIDEBAR)
# ---------------------------------------------------------
st.sidebar.title("🔍 Filtros Executivos")
st.sidebar.markdown("**Regional SP Capital — Lojas Conceito**")

lojas_selecionadas = st.sidebar.multiselect(
    "Filtrar Lojas:",
    options=sorted(df_data["Nome_Loja"].unique()),
    default=sorted(df_data["Nome_Loja"].unique())
)

semanas_selecionadas = st.sidebar.multiselect(
    "Filtrar Semanas:",
    options=["26 / W36", "26 / W37", "26 / W38"],
    default=["26 / W36", "26 / W37", "26 / W38"]
)

# Aplicando Filtros
df_filtered = df_data[
    (df_data["Nome_Loja"].isin(lojas_selecionadas)) &
    (df_data["Semana"].isin(semanas_selecionadas))
]

# ---------------------------------------------------------
# 4. CABEÇALHO DO DASHBOARD
# ---------------------------------------------------------
st.title("📊 Evolução Regional SP Capital — Lojas Conceito")
st.caption("Visão Consolidada YTD Setembro (Semanas W36 a W38) para Diretoria")

# ---------------------------------------------------------
# 5. CARDS DE KPIS (RESUMO EXECUTIVO)
# ---------------------------------------------------------
total_vendas = df_filtered["Vendas"].sum()
loja_top_vendas = df_filtered.groupby("Loja")["Vendas"].sum().idxmax() if not df_filtered.empty else "N/A"
val_top_vendas = df_filtered.groupby("Loja")["Vendas"].sum().max() if not df_filtered.empty else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Vendas YTD Setembro", 
        value=f"R$ {total_vendas:,.0f}".replace(",", ".")
    )

with col2:
    st.metric(
        label="Maior Volume (Top Store)", 
        value=f"{loja_top_vendas}", 
        delta=f"R$ {val_top_vendas:,.0f}".replace(",", ".")
    )

with col3:
    st.metric(
        label="Destaque Crescimento", 
        value="ANF (Anália Franco)", 
        delta="+21,4% Vs LY"
    )

with col4:
    apl_vendas = df_filtered[df_filtered["Loja"] == "APL"]["Vendas"].sum()
    st.metric(
        label="Inauguração 2026 (APL)", 
        value=f"R$ {apl_vendas:,.0f}".replace(",", "."), 
        delta="Sem Histórico LY", 
        delta_color="off"
    )

st.divider()

# ---------------------------------------------------------
# 6. ABAS INTERATIVAS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Matriz Executiva & Semanal", 
    "📈 Gráficos Interativos", 
    "🗃️ Dados Brutos", 
    "🎯 Diagnóstico da Diretoria"
])

# ---------------------------------------------------------
# ABA 1: MATRIZ EXECUTIVA COMPLETA & EVOLUÇÃO SEMANAL
# ---------------------------------------------------------
with tab1:
    st.subheader("1. Matriz de Desempenho Executivo (Consolidado SP)")
    st.caption("Visão com Vendas, Share de Participação, Fluxo e Conversão Comparativos Vs LY")

    # Construindo Tabela Consolidada com Todos os Indicadores Executivos
    summary_list = []
    total_reg_vendas = df_filtered["Vendas"].sum()

    for loja, group in df_filtered.groupby("Nome_Loja"):
        vendas_tot = group["Vendas"].sum()
        share = (vendas_tot / total_reg_vendas) if total_reg_vendas > 0 else 0
        
        # Tratamento Especial para APL (Paulista)
        if "APL" in loja:
            vendas_ly = "Inauguração 2026"
            fluxo_ly = "N/A"
            conv_ly = "N/A"
            status = "🟢 Em Ramp-Up"
        else:
            v_ly = group["Vendas Vs LY %"].mean()
            f_ly = group["Fluxo Vs LY %"].mean()
            c_ly = group["Conversão Vs LY %"].mean()
            
            vendas_ly = f"{v_ly * 100:+.1f}%".replace(".", ",") if pd.notnull(v_ly) else "N/A"
            fluxo_ly = f"{f_ly * 100:+.1f}%".replace(".", ",") if pd.notnull(f_ly) else "N/A"
            conv_ly = f"{c_ly * 100:+.1f}%".replace(".", ",") if pd.notnull(c_ly) else "N/A"
            
            if c_ly < -0.15:
                status = "🔴 Alerta Conversão"
            elif v_ly > 0.10:
                status = "🟢 Destaque Crescimento"
            else:
                status = "🟡 Estável / Operando"

        summary_list.append({
            "Loja / Unidade": loja,
            "Vendas Acum. (R$)": f"R$ {vendas_tot:,.0f}".replace(",", "."),
            "Share (%)": f"{share * 100:.1f}%".replace(".", ","),
            "Vendas Vs LY": vendas_ly,
            "Fluxo Vs LY": fluxo_ly,
            "Conversão Vs LY": conv_ly,
            "Status Executivo": status
        })

    df_summary = pd.DataFrame(summary_list)
    
    # Ordenar por maior faturamento
    df_summary["sort_val"] = df_filtered.groupby("Nome_Loja")["Vendas"].sum().values
    df_summary = df_summary.sort_values(by="sort_val", ascending=False).drop(columns=["sort_val"])

    # Exibição da Tabela Principal
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.subheader("2. Evolução Semanal de Vendas (R$)")
    st.caption("Detalhamento semana a semana por unidade (Sem desalinhamento)")

    # Pivot Table limpa e corrigida (sem bug de MultiIndex)
    pivot_vendas = df_filtered.pivot_table(
        index="Nome_Loja", 
        columns="Semana", 
        values="Vendas", 
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    semanas_cols = [c for c in pivot_vendas.columns if c != "Nome_Loja"]
    pivot_vendas["Total YTD Setembro"] = pivot_vendas[semanas_cols].sum(axis=1)
    pivot_vendas = pivot_vendas.sort_values(by="Total YTD Setembro", ascending=False)

    # Formatar valores monetários para exibição
    pivot_formatted = pivot_vendas.copy()
    pivot_formatted["Nome_Loja"] = pivot_formatted["Nome_Loja"]
    for col in semanas_cols + ["Total YTD Setembro"]:
        pivot_formatted[col] = pivot_formatted[col].apply(lambda x: f"R$ {x:,.0f}".replace(",", "."))

    st.dataframe(pivot_formatted, use_container_width=True, hide_index=True)


# ---------------------------------------------------------
# ABA 2: GRÁFICOS INTERATIVOS
# ---------------------------------------------------------
with tab2:
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Faturamento Acumulado por Loja (R$)")
        vendas_por_loja = df_filtered.groupby("Loja")["Vendas"].sum().reset_index().sort_values(by="Vendas", ascending=True)
        fig_bar = px.bar(
            vendas_por_loja, 
            x="Vendas", 
            y="Loja", 
            orientation='h',
            text_auto='.2s',
            color="Vendas",
            color_continuous_scale="Blues"
        )
        fig_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.subheader("Matriz de Eficiência: Fluxo Vs Conversão (Vs LY)")
        df_ly = df_filtered.dropna(subset=["Fluxo Vs LY %", "Conversão Vs LY %"])
        
        fig_scatter = px.scatter(
            df_ly,
            x="Fluxo Vs LY %",
            y="Conversão Vs LY %",
            color="Loja",
            size="Vendas",
            hover_name="Nome_Loja",
            text="Semana",
            labels={"Fluxo Vs LY %": "Variação de Fluxo (%)", "Conversão Vs LY %": "Variação de Conversão (%)"}
        )
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_scatter.add_vline(x=0, line_dash="dash", line_color="gray")
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)


# ---------------------------------------------------------
# ABA 3: DADOS BRUTOS
# ---------------------------------------------------------
with tab3:
    st.subheader("Base de Dados Completa")
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados em CSV",
        data=csv,
        file_name="dados_regional_sp_capital.csv",
        mime="text/csv"
    )


# ---------------------------------------------------------
# ABA 4: DIAGNÓSTICO DA DIRETORIA
# ---------------------------------------------------------
with tab4:
    st.subheader("📌 Diagnóstico da Diretoria — Unidades SP Capital")
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        st.markdown("""
        ### 🟢 1. APL (Paulista)
        * **Status:** Inauguração 2026 (Ramp-up).
        * **Desempenho:** Já acumula **R$ 2,20M** no YTD Setembro, sendo a 3ª maior em faturamento.
        * **Recomendação:** Acompanhar curva de maturidade das vendas sem tentar comparar com o ano anterior.
        """)
        
    with col_d2:
        st.markdown("""
        ### 🟡 2. ANF (Anália Franco)
        * **Status:** Alta Atração / Gargalo no Caixa.
        * **Desempenho:** Vendas em forte alta (+21,4% Vs LY) com tráfego elevado (+14,9%), mas perda de conversão (-12,8% na W38).
        * **Recomendação:** Reforçar contingente de atendimento e fila rápida nos horários de pico.
        """)

    with col_d3:
        st.markdown("""
        ### 🔴 3. SBO (Bourbon Pompéia)
        * **Status:** Crítico / Perda Severa de Conversão.
        * **Desempenho:** O shopping atraiu mais público (+19,7% de fluxo), porém a conversão despencou -38,5%.
        * **Recomendação:** Auditoria imediata de equipe de loja, disponibilidade de produto (ruptura) e preços.
        """)
