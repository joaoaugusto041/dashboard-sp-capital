import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from loader_b3 import carregar_dados_b3

# ======================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTILOS
# ======================================================================
st.set_page_config(page_title="Dashboard Financeiro B3SA3", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .kpi {border-left: 5px solid #1f77b4; padding: 12px 16px; border-radius: 8px;
          background: rgba(128,128,128,0.08); margin-bottom: 12px; min-height: 108px;}
    .kpi-titulo {font-size: .75rem; opacity: .7; font-weight: 600; text-transform: uppercase;}
    .kpi-valor {font-size: 1.45rem; font-weight: 700; line-height: 1.5;}
    .kpi-delta {font-size: .82rem; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

COR_TOTAL, COR_QUEDA, COR_GANHO = "#1f77b4", "#d62728", "#2ca02c"
COR_OPORT = {"Alto": "#e4572e", "Médio": "#f2b134", "Baixo": "#9aa5b1", "Nulo": "#6c8ebf"}
ALIQUOTA_NOMINAL = 0.34

MAPEAMENTO_CONTAS = {}
ESCALA_PLANILHA_PARA_MI = 1.0

ANOS_REF = [2022, 2023, 2024, 2025, 2026]
REF = {
    2022: dict(receita_bruta=2420.0, deducoes=235.0, despesas=745.0, ajustes=55.0, amortizacao=118.0, financeiro=260.0, ir=118.0),
    2023: dict(receita_bruta=2590.0, deducoes=250.0, despesas=770.0, ajustes=38.0, amortizacao=121.0, financeiro=280.0, ir=112.0),
    2024: dict(receita_bruta=2740.0, deducoes=264.0, despesas=795.0, ajustes=61.0, amortizacao=123.0, financeiro=290.0, ir=109.0),
    2025: dict(receita_bruta=2868.0, deducoes=277.5, despesas=819.4, ajustes=42.0, amortizacao=125.8, financeiro=300.0, ir=105.1),
    2026: dict(receita_bruta=3010.0, deducoes=291.0, despesas=850.0, ajustes=30.0, amortizacao=128.0, financeiro=310.0, ir=108.0),
}
DET = {
    "ded": [("PIS/COFINS", 185.4, "Médio"), ("ISS municipal", 92.1, "Baixo")],
    "desp": [("Pessoal fixo", 285.0, "Baixo"), ("Remuneração variável / bônus", 110.2, "Médio"),
             ("Licenças de software e nuvem", 165.4, "Alto"), ("Processamento e links de dados", 82.1, "Médio"),
             ("Consultorias e jurídico", 95.3, "Alto"), ("Market Maker", 42.0, "Baixo"),
             ("Outras despesas", 39.4, "Médio")],
    "aj": [("Assessoria em M&A", 18.2, "Médio"), ("Rescisões e reestruturação", 14.5, "Médio"),
           ("Provisões cíveis e tributárias", 9.3, "Médio")],
    "ir": [("IRPJ", 145.2, "Médio"), ("CSLL", 58.3, "Baixo"), ("Benefício fiscal do JCP", -98.4, "Alto")],
}

# ======================================================================
# FUNÇÕES DE FORMATAÇÃO E UTILITÁRIOS
# ======================================================================
def br(v, casas=1):
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def mi(v, casas=1):
    return f"R$ {br(v, casas)} mi"

def var_pct(atual, anterior):
    return None if not anterior else (atual / anterior - 1) * 100

def mostrar_grafico(fig, **kw):
    fig.update_layout(separators=",.", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      margin=dict(t=60, b=40, l=10, r=10))
    cfg = {"displayModeBar": False}
    try:
        return st.plotly_chart(fig, width="stretch", config=cfg, **kw)
    except TypeError:
        return st.plotly_chart(fig, use_container_width=True, config=cfg, **kw)

def mostrar_tabela(df, **kw):
    try:
        return st.dataframe(df, width="stretch", hide_index=True, **kw)
    except TypeError:
        return st.dataframe(df, use_container_width=True, hide_index=True, **kw)

def card(titulo, valor, delta_txt="", cor="#1f77b4"):
    st.markdown(
        f"<div class='kpi' style='border-left-color:{cor}'><div class='kpi-titulo'>{titulo}</div>"
        f"<div class='kpi-valor'>{valor}</div><div class='kpi-delta' style='color:{cor}'>{delta_txt}</div></div>",
        unsafe_allow_html=True)

def cor_delta(delta, bom_se_subir=True):
    if delta is None or abs(delta) < 0.05:
        return "#6c757d"
    return COR_GANHO if (delta > 0) == bom_se_subir else COR_QUEDA

def txt_delta(delta, ano_ant, unidade="%"):
    if delta is None:
        return "sem ano anterior"
    seta = "▲" if delta > 0 else "▼" if delta < 0 else "■"
    return f"{seta} {br(abs(delta))}{unidade} vs {ano_ant}"

# ======================================================================
# PREPARAÇÃO E TRATAMENTO DA PLANILHA DE RI (LEITURA BLINDADA)
# ======================================================================
def para_numero(v):
    nan = float("nan")
    if v is None:
        return nan
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).strip().replace("R$", "").replace("%", "").strip()
    if t in ("", "nan", "None", "-", "—"):
        return nan
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        n = float(t)
    except ValueError:
        return nan
    return -n if neg else n

@st.cache_data(show_spinner="Carregando dados da B3...")
def preparar_planilha():
    raw = carregar_dados_b3()
    if raw is None:
        return pd.DataFrame(), pd.DataFrame()
    
    cols = [0]
    nomes = ["Conta / Indicador"]
    for c in range(1, raw.shape[1]):
        rotulo = ""
        for r in range(min(3, raw.shape[0])):
            val = str(raw.iloc[r, c]).strip()
            if val and val.lower() not in ("nan", "none", ""):
                if val.endswith(".0"):
                    val = val[:-2]
                if val.isdigit() or "20" in val or "1T" in val or "2T" in val or "3T" in val or "4T" in val:
                    rotulo = val
                    break
        if not rotulo:
            rotulo = f"Col_{c}"
            
        cols.append(c)
        nomes.append(rotulo)
            
    df = raw.iloc[3:, cols].copy()
    df.columns = nomes
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.dropna(subset=["Conta / Indicador"])
    df["Conta / Indicador"] = df["Conta / Indicador"].astype(str).str.strip()
    df = df.reset_index(drop=True)

    df_n, df_t = df.copy(), df.copy()
    for c in df.columns[1:]:
        nums = df[c].map(para_numero)
        df_n[c] = nums
        df_t[c] = [
            br(n, 2) if pd.notna(n)
            else ("" if str(o).strip().lower() in ("nan", "none", "") else str(o))
            for n, o in zip(nums, df[c])
        ]
    return df_n, df_t

df_num, df_txt = preparar_planilha()
anos_planilha = [str(c) for c in df_num.columns[1:]]
ANOS = sorted(list(set(ANOS_REF) | set([int(a) for a in anos_planilha if a.isdigit() and len(a) == 4])))

def valor_planilha(chave, ano):
    rx = MAPEAMENTO_CONTAS.get(chave)
    if not rx or df_num.empty or str(ano) not in df_num.columns:
        return None
    linha = df_num[df_num["Conta / Indicador"].str.contains(rx, case=False, regex=True, na=False)]
    if linha.empty or pd.isna(linha.iloc[0][str(ano)]):
        return None
    return abs(float(linha.iloc[0][str(ano)])) * ESCALA_PLANILHA_PARA_MI

def escalar(base, total):
    soma = sum(x[1] for x in base)
    return [(n, v * total / soma, p) for n, v, p in base]

def montar_modelo(ano):
    ref = REF[min(REF, key=lambda a: abs(a - ano))]
    v, usa_ref = {}, []
    for k in ref:
        x = valor_planilha(k, ano)
        if x is None:
            x, _ = ref[k], usa_ref.append(k)
        v[k] = x
    m = dict(v)
    m["receita_liquida"] = m["receita_bruta"] - m["deducoes"]
    m["ebitda_rec"] = m["receita_liquida"] - m["despesas"]
    m["ebitda_rep"] = m["ebitda_rec"] - m["ajustes"]
    m["lucro"] = m["ebitda_rep"] - m["amortizacao"] - m["financeiro"] - m["ir"]
    m["lucro_rec"] = m["lucro"] + m["ajustes"] * (1 - ALIQUOTA_NOMINAL)
    m["bx_total"] = m["amortizacao"] + m["financeiro"] + m["ir"]
    m["margem_ebitda"] = m["ebitda_rec"] / m["receita_liquida"] * 100
    m["margem_oper"] = (m["ebitda_rep"] - m["amortizacao"]) / m["receita_liquida"] * 100
    m["margem_liq"] = m["lucro"] / m["receita_liquida"] * 100
    m["det"] = {
        "ded": escalar(DET["ded"], m["deducoes"]),
        "desp": escalar(DET["desp"], m["despesas"]),
        "aj": escalar(DET["aj"], m["ajustes"]),
        "bx": [("Amortização do intangível (Cetip)", m["amortizacao"], "Nulo"),
               ("Resultado financeiro líquido", m["financeiro"], "Médio")] + escalar(DET["ir"], m["ir"]),
    }
    m["usa_ref"] = usa_ref
    return m

MODELOS = {a: montar_modelo(a) for a in ANOS}

# ======================================================================
# CONTROLE SUPERIOR
# ======================================================================
st.title("📊 Dashboard Financeiro B3SA3 — Auditoria de Rentabilidade")
st.caption("Clique nas barras dos gráficos para dar drill down. Utilize os seletores abaixo para personalizar a análise.")

col_a, col_b = st.columns([1, 3])
with col_a:
    ano = st.selectbox("📅 Ano de referência (KPIs e Ponte)", ANOS, index=len(ANOS) - 1, format_func=str)

m = MODELOS[ano]
ano_ant = ano - 1 if (ano - 1) in MODELOS else None
mp = MODELOS.get(ano_ant) if ano_ant else None

# ======================================================================
# SEÇÃO 1: RADAR DE ALERTAS E KPIs
# ======================================================================
st.markdown("---")
st.subheader("🚨 Radar de Alertas e Indicadores Executivos")

def d(chave):
    return var_pct(m[chave], mp[chave]) if mp else None

def dpp(chave):
    return (m[chave] - mp[chave]) if mp else None

k = st.columns(4)
with k[0]:
    card("Receita bruta", mi(m["receita_bruta"]), txt_delta(d("receita_bruta"), ano_ant), cor_delta(d("receita_bruta")))
with k[1]:
    card("Receita líquida", mi(m["receita_liquida"]), txt_delta(d("receita_liquida"), ano_ant), cor_delta(d("receita_liquida")))
with k[2]:
    card("EBITDA recorrente", mi(m["ebitda_rec"]), txt_delta(d("ebitda_rec"), ano_ant), cor_delta(d("ebitda_rec")))
with k[3]:
    card("Margem EBITDA recorrente", f"{br(m['margem_ebitda'])}%", txt_delta(dpp("margem_ebitda"), ano_ant, " p.p."), cor_delta(dpp("margem_ebitda")))

k = st.columns(4)
with k[0]:
    dd, dr = d("despesas"), d("receita_liquida")
    cor_desp = COR_QUEDA if (dd is not None and dr is not None and dd > dr) else COR_GANHO
    card("Despesas operacionais", mi(m["despesas"]), txt_delta(dd, ano_ant), cor_desp if dd is not None else "#6c757d")
with k[1]:
    if mp and dr:
        gao = d("ebitda_rec") / dr
        card("Alavancagem operacional", f"{br(gao, 2)}x", "Positiva: EBITDA cresce mais que receita" if gao > 1 else "Sem ganho de escala", COR_GANHO if gao > 1 else COR_QUEDA)
    else:
        card("Alavancagem operacional", "—", "sem ano anterior", "#6c757d")
with k[2]:
    card("Lucro líquido recorrente", mi(m["lucro_rec"]), txt_delta(d("lucro_rec"), ano_ant), cor_delta(d("lucro_rec")))
with k[3]:
    card("Margem líquida", f"{br(m['margem_liq'])}%", txt_delta(dpp("margem_liq"), ano_ant, " p.p."), cor_delta(dpp("margem_liq")))

# ======================================================================
# SEÇÃO 2: PONTE DE RESULTADO (WATERFALL INTERATIVO POR CLIQUE)
# ======================================================================
st.markdown("---")
st.subheader("🌉 Ponte de Resultado — Clique na barra para expandir os subníveis")

st.session_state.setdefault("drill", None)
st.session_state.setdefault("ver", 0)

NOMES_DRILL = {
    "ded": "Deduções e Impostos", "desp": "Despesas Operacionais",
    "aj": "Ajustes Não Recorrentes", "bx": "Amortização, Financeiro e IR",
}

def montar_passos(m, expandido):
    passos = []
    def total(rot, val):
        passos.append(dict(rotulo=rot, valor=val, tipo="total", cor=COR_TOTAL, hover=f"{rot}<br>{mi(val)}"))

    def queda(chave, val):
        if expandido == chave:
            pai = sum(x[1] for x in m["det"][chave])
            for nome, v, pot in m["det"][chave]:
                ganho = v < 0
                cor = COR_GANHO if ganho else COR_OPORT[pot]
                passos.append(dict(
                    rotulo=nome, valor=-v, tipo="filho", cor=cor,
                    hover=f"{nome}<br>{mi(abs(v))} ({br(abs(v) / pai * 100)}% de {NOMES_DRILL[chave]})"
                          f"<br>Potencial de oportunidade: {pot}"))
        else:
            rot = NOMES_DRILL[chave] + " ▸"
            passos.append(dict(rotulo=rot, valor=-val, tipo="queda", cor=COR_QUEDA, chave=chave,
                               hover=f"{NOMES_DRILL[chave]}<br>{mi(val)}<br>Clique para detalhar"))

    total("Receita Bruta", m["receita_bruta"])
    queda("ded", m["deducoes"])
    total("Receita Líquida", m["receita_liquida"])
    queda("desp", m["despesas"])
    total("EBITDA Recorrente", m["ebitda_rec"])
    queda("aj", m["ajustes"])
    total("EBITDA Reportado", m["ebitda_rep"])
    queda("bx", m["bx_total"])
    total("Lucro Líquido", m["lucro"])
    return passos

passos = montar_passos(m, st.session_state["drill"])

nivel, bases, alturas, topos = 0.0, [], [], []
for p in passos:
    if p["tipo"] == "total":
        base, alt, nivel = 0.0, p["valor"], p["valor"]
    elif p["valor"] < 0:
        base, alt = nivel + p["valor"], -p["valor"]
        nivel += p["valor"]
    else:
        base, alt = nivel, p["valor"]
        nivel += p["valor"]
    bases.append(base)
    alturas.append(alt)
    topos.append(base + alt)

x = [p["rotulo"] for p in passos]
textos = [(br(p["valor"]) if p["tipo"] == "total" else ("+" if p["valor"] > 0 else "−") + br(abs(p["valor"]))) for p in passos]

fig = go.Figure()
fig.add_bar(x=x, y=bases, marker_color="rgba(0,0,0,0)", hoverinfo="skip", showlegend=False)
fig.add_bar(x=x, y=alturas, marker_color=[p["cor"] for p in passos], hovertext=[p["hover"] for p in passos],
            hoverinfo="text", showlegend=False)
fig.add_scatter(x=x, y=topos, mode="text", text=textos, textposition="top center", hoverinfo="skip", showlegend=False)
fig.update_layout(
    barmode="stack", bargap=0.25, height=520, clickmode="event+select",
    title=f"<b>Ponte consolidada do resultado — {ano}</b>" +
          (f" · detalhando <b>{NOMES_DRILL[st.session_state['drill']]}</b>" if st.session_state["drill"] else ""),
    yaxis=dict(title="R$ milhões", range=[0, max(topos) * 1.12]),
)

if st.session_state["drill"]:
    if st.button("⬅️ Voltar à Visão Consolidada", type="primary"):
        st.session_state["drill"] = None
        st.session_state["ver"] += 1
        st.rerun()

evento = mostrar_grafico(fig, key=f"ponte_{st.session_state['ver']}", on_select="rerun", selection_mode="points")
pontos = (evento or {}).get("selection", {}).get("points", []) if evento else []
if pontos and not st.session_state["drill"]:
    clicado = pontos[0].get("x")
    chave = next((p.get("chave") for p in passos if p["rotulo"] == clicado), None)
    if chave:
        st.session_state["drill"] = chave
        st.session_state["ver"] += 1
        st.rerun()

# ======================================================================
# SEÇÃO 3: ANÁLISES COMPLEMENTARES DE MIDDLE-LINE
# ======================================================================
st.markdown("---")
st.subheader("📈 Análises Complementares de Middle-Line")

abas = st.tabs(["EBITDA", "Estrutura de custos", "Margens", "Pareto de custos", "Mapa hierárquico", "Variação anual"])
anos_txt = [str(a) for a in ANOS]
BASE_CUSTOS = m["det"]["desp"] + [("Amortização do intangível (Cetip)", m["amortizacao"], "Nulo")]

with abas[0]:
    f = go.Figure()
    f.add_bar(name="EBITDA reportado", x=anos_txt, y=[MODELOS[a]["ebitda_rep"] for a in ANOS], marker_color="#6c8ebf",
              text=[br(MODELOS[a]["ebitda_rep"], 0) for a in ANOS], textposition="outside")
    f.add_bar(name="EBITDA recorrente", x=anos_txt, y=[MODELOS[a]["ebitda_rec"] for a in ANOS], marker_color=COR_TOTAL,
              text=[br(MODELOS[a]["ebitda_rec"], 0) for a in ANOS], textposition="outside")
    f.update_layout(barmode="group", title="<b>EBITDA reportado vs. recorrente (R$ milhões)</b>",
                    yaxis_title="R$ milhões", xaxis=dict(type="category"), legend=dict(orientation="h", y=-0.15))
    mostrar_grafico(f)

with abas[1]:
    c1, c2 = st.columns([3, 2])
    with c1:
        f = go.Figure(go.Pie(
            labels=[n for n, _, _ in BASE_CUSTOS], values=[v for _, v, _ in BASE_CUSTOS], hole=0.5,
            marker=dict(colors=[COR_OPORT[p] if p != "Médio" else "#f2b134" for _, _, p in BASE_CUSTOS]),
            texttemplate="%{label}<br>R$ %{value:,.1f} mi<br>%{percent}", textposition="outside",
            hovertemplate="%{label}<br>R$ %{value:,.1f} mi (%{percent})<extra></extra>", sort=False))
        f.update_layout(title=f"<b>Estrutura de custos — {ano}</b>", showlegend=False, height=480)
        ev = mostrar_grafico(f, key="rosca", on_select="rerun", selection_mode="points")
    with c2:
        st.markdown("##### 🔍 Detalhe da fatia")
        pts = (ev or {}).get("selection", {}).get("points", []) if ev else []
        if pts:
            idx = pts[0].get("point_index", pts[0].get("point_number"))
            if idx is None:
                idx = next((i for i, (n, _, _) in enumerate(BASE_CUSTOS) if n == pts[0].get("label")), 0)
            nome, val, pot = BASE_CUSTOS[int(idx)]
            card(nome, mi(val), f"{br(val / m['receita_liquida'] * 100)}% da receita líquida · potencial: {pot}", COR_OPORT[pot])
        else:
            st.info("Clique em uma fatia da rosca para ver os detalhes.")

with abas[2]:
    f = go.Figure()
    for nome, chave, cor in [("Margem EBITDA recorrente", "margem_ebitda", COR_TOTAL),
                             ("Margem operacional", "margem_oper", "#f2b134"), ("Margem líquida", "margem_liq", COR_GANHO)]:
        f.add_scatter(name=nome, x=anos_txt, y=[MODELOS[a][chave] for a in ANOS], mode="lines+markers+text",
                      line=dict(color=cor, width=3), text=[f"{br(MODELOS[a][chave])}%" for a in ANOS],
                      textposition="top center")
    f.update_layout(title="<b>Evolução das margens sobre a receita líquida (%)</b>", yaxis=dict(ticksuffix="%"),
                    xaxis=dict(type="category"), legend=dict(orientation="h", y=-0.15), height=460)
    mostrar_grafico(f)

with abas[3]:
    ordenado = sorted(BASE_CUSTOS, key=lambda x: -x[1])
    total_c = sum(v for _, v, _ in ordenado)
    acum, soma = [], 0
    for _, v, _ in ordenado:
        soma += v
        acum.append(soma / total_c * 100)
    f = go.Figure()
    f.add_bar(x=[n for n, _, _ in ordenado], y=[v for _, v, _ in ordenado], name="Valor (R$ mi)",
              marker_color=[COR_OPORT[p] for _, _, p in ordenado], text=[br(v) for _, v, _ in ordenado], textposition="outside")
    f.add_scatter(x=[n for n, _, _ in ordenado], y=acum, name="% acumulado", yaxis="y2", mode="lines+markers",
                  line=dict(color="#333", width=2))
    f.update_layout(title=f"<b>Pareto de custos — {ano}</b>",
                    yaxis=dict(title="R$ milhões"), yaxis2=dict(title="% acumulado", overlaying="y", side="right",
                    range=[0, 105], ticksuffix="%"), legend=dict(orientation="h", y=-0.3), height=500)
    mostrar_grafico(f)

with abas[4]:
    rotulos, pais, valores = ["Receita Bruta"], [""], [m["receita_bruta"]]
    grupos = [("Deduções e impostos", m["det"]["ded"]), ("Despesas operacionais", m["det"]["desp"]),
              ("Ajustes não recorrentes", m["det"]["aj"]),
              ("Amortização, financeiro e IR", [("Amortização (Cetip)", m["amortizacao"], ""),
                                               ("Resultado financeiro", m["financeiro"], ""),
                                               ("IRPJ/CSLL (líquidos do JCP)", m["ir"], "")]),
              ("Lucro líquido", [("Lucro líquido ", m["lucro"], "")])]
    for gnome, filhos in grupos:
        rotulos.append(gnome)
        pais.append("Receita Bruta")
        valores.append(sum(v for _, v, _ in filhos))
        for n, v, _ in filhos:
            rotulos.append(n)
            pais.append(gnome)
            valores.append(v)
    f = go.Figure(go.Treemap(labels=rotulos, parents=pais, values=valores, branchvalues="total",
                           texttemplate="%{label}<br>R$ %{value:,.1f} mi", textfont=dict(size=14),
                           hovertemplate="%{label}<br>R$ %{value:,.1f} mi<extra></extra>"))
    f.update_layout(title=f"<b>Para onde vai cada real da receita bruta — {ano}</b>", height=560)
    mostrar_grafico(f)

with abas[5]:
    if mp:
        itens = [("Receita líquida", "receita_liquida", True), ("Despesas operacionais", "despesas", False),
                 ("EBITDA recorrente", "ebitda_rec", True), ("Lucro líquido", "lucro", True)]
        vals = [var_pct(m[c], mp[c]) for _, c, _ in itens]
        f = go.Figure(go.Bar(x=[n for n, _, _ in itens], y=vals, marker_color=[cor_delta(v, b) for v, (_, _, b) in zip(vals, itens)],
                             text=[f"{br(v)}%" for v in vals], textposition="outside"))
        f.update_layout(title=f"<b>Variação {ano_ant} → {ano} (%)</b>", yaxis=dict(ticksuffix="%"), height=460)
        mostrar_grafico(f)
    else:
        st.info("Selecione um ano com ano anterior disponível para ver a variação.")

# ======================================================================
# SEÇÃO 4: DRE GERENCIAL COMPLETO (COM MULTI-SELEÇÃO DE ANOS)
# ======================================================================
st.markdown("---")
st.subheader("📋 DRE Gerencial Completo — B3 (API RI)")

if df_txt.empty:
    st.warning("⚠️ Não foi possível carregar os dados gerenciais da B3 no momento.")
else:
    col_t1, col_t2, col_t3 = st.columns([3, 1.5, 2])
    
    todas_colunas_planilha = list(df_txt.columns[1:])
    
    with col_t1:
        colunas_selecionadas = st.multiselect(
            "📅 Selecione os anos/períodos para exibir na tabela:",
            options=todas_colunas_planilha,
            default=todas_colunas_planilha,
            help="Clique para adicionar ou remover anos da visualização lado a lado."
        )
    
    with col_t2:
        st.markdown("<br>", unsafe_allow_html=True)
        modo_foco = st.checkbox("🎯 Modo Foco", value=False)
        
    with col_t3:
        busca = st.text_input("🔍 Pesquisar conta", placeholder="Ex.: EBITDA, Pessoal, JCP, TI...")

    if not colunas_selecionadas:
        colunas_selecionadas = todas_colunas_planilha

    df_exibicao = df_txt[["Conta / Indicador"] + colunas_selecionadas].copy()

    if busca:
        df_exibicao = df_exibicao[df_exibicao["Conta / Indicador"].str.contains(busca, case=False, regex=False, na=False)]
    elif modo_foco:
        termos = "EBITDA|Despesa|Lucro|Receita L|Imposto|JCP|Pessoal|Tecnologia|Intang|Amortiza|Financeiro"
        df_exibicao = df_exibicao[df_exibicao["Conta / Indicador"].str.contains(termos, case=False, na=False)]

    st.caption(f"Exibindo {len(df_exibicao)} contas contábeis para {len(colunas_selecionadas)} período(s) selecionado(s).")
    mostrar_tabela(df_exibicao, height=520)

    csv = df_exibicao.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
    st.download_button("⬇️ Exportar DRE Selecionado para CSV / Excel", data=csv, file_name="B3SA3_DRE_Gerencial.csv", mime="text/csv")

# ======================================================================
# GLOSSÁRIO ANALÍTICO
# ======================================================================
with st.expander("📖 Glossário analítico"):
    st.markdown("""
**EBITDA recorrente vs. reportado:** o recorrente expurga eventos pontuais (assessorias de M&A, rescisões, provisões),
mostrando a capacidade operacional real da B3.

**Amortização de intangíveis (Cetip):** efeito contábil sem desembolso de caixa.

**Benefício fiscal do JCP:** reduz a alíquota efetiva de IRPJ/CSLL através da distribuição de proventos dedutíveis.
""")
