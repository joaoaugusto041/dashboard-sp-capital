import streamlit as st
import pandas as pd
from loader_b3 import carregar_dados_b3

st.set_page_config(page_title="Diagnóstico B3", layout="wide")

st.title("🔍 Diagnóstico da API de RI da B3 (`loader_b3`)")

raw = carregar_dados_b3()

if raw is None:
    st.error("A função carregar_dados_b3() retornou None. O arquivo não foi baixado ou lido.")
else:
    st.success(f"Arquivo carregado com sucesso! Dimensões brutas: {raw.shape[0]} linhas e {raw.shape[1]} colunas.")
    
    st.markdown("### Primeiras 15 linhas e 10 colunas do arquivo bruto da B3:")
    st.dataframe(raw.iloc[:15, :10].astype(str), use_container_width=True)
    
    st.markdown("### O que fazer agora:")
    st.markdown("""
    Olha a tabela acima no seu Streamlit:
    1. Em qual linha exata o **nome das contas** (como *Receita*, *Custos*) começa? (Ex: linha 3, linha 4, linha 5?)
    2. Em qual linha exata estão os **anos** (como *2022*, *2023*, *2024* ou trimestres)? (Ex: linha 1, linha 2?)
    
    Me mande uma mensagem dizendo **em quais linhas exatas** estão os anos e as contas na tabela que apareceu aí na sua tela. Com essa informação, eu ajusto o `app.py` para recortar nas coordenadas certas e os dados aparecem instantaneamente para você!
    """)
