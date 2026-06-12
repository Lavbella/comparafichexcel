import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Fusão Avançada de Excels", layout="wide")
st.title("📂 Fusão e Cruzamento Avançado de Ficheiros Excel")

# 1. Upload dos Ficheiros
col1, col2 = st.columns(2)
with col1:
    file_a = st.file_uploader("Carregue o Excel A", type=["xlsx", "xls"])
with col2:
    file_b = st.file_uploader("Carregue o Excel B", type=["xlsx", "xls"])

if file_a and file_b:
    # Ler os dados
    df_a = pd.read_excel(file_a)
    df_b = pd.read_excel(file_b)
    
    st.success("Ficheiros carregados com sucesso!")
    
    # 2. Configuração de Múltiplas Chaves
    st.header("🔗 Mapeamento de Colunas Chave")
    
    cols_a = list(df_a.columns)
    cols_b = list(df_b.columns)
    
    # Controlar a quantidade de chaves dinamicamente
    if 'num_keys' not in st.session_state:
        st.session_state.num_keys = 1
        
    c_btn1, c_btn2 = st.columns([1, 10])
    with c_btn1:
        if st.button("➕ Adicionar Chave"):
            st.session_state.num_keys += 1
            st.rerun()
    with c_btn2:
        if st.button("➖ Remover Chave") and st.session_state.num_keys > 1:
            st.session_state.num_keys -= 1
            st.rerun()

    keys_a = []
    keys_b = []
    
    # Criar campos de seleção para cada chave configurada
    for i in range(st.session_state.num_keys):
        col_select1, col_select2 = st.columns(2)
        with col_select1:
            k_a = st.selectbox(f"Excel A - Chave {i+1}:", cols_a, key=f"ka_{i}")
            keys_a.append(k_a)
        with col_select2:
            k_b = st.selectbox(f"Excel B - Correspondente {i+1}:", cols_b, key=f"kb_{i}")
            keys_b.append(k_b)
            
    # 3. Processamento de Dados
    if st.button("🔄 Executar Fusão e Cruzamento", type="primary"):
        df_a_proc = df_a.copy()
        df_b_proc = df_b.copy()
        
        # Limpar espaços em branco em todas as colunas chave selecionadas
        for k_a in keys_a:
            df_a_proc[k_a] = df_a_proc[k_a].astype(str).str.strip()
        for k_b in keys_b:
            df_b_proc[k_b] = df_b_proc[k_b].astype(str).str.strip()
            
        # Cruzamento utilizando a lista de múltiplas chaves
        merged_df = pd.merge(
            df_a_proc, 
            df_b_proc, 
            left_on=keys_a, 
            right_on=keys_b, 
            how="outer", 
            indicator=True
        )
        
        # Guardar resultado no estado da aplicação para permitir filtros posteriores
        status_map = {
            "both": "Encontrado em Ambos",
            "left_only": "Apenas no Excel A (Falta no B)",
            "right_only": "Apenas no Excel B (Falta no A)"
        }
        merged_df["Resultado_Match"] = merged_df["_merge"].map(status_map)
        merged_df.drop(columns=["_merge"], inplace=True)
        
        # Organizar colunas
        cols = ["Resultado_Match"] + [c for c in merged_df.columns if c != "Resultado_Match"]
        st.session_state.merged_df = merged_df[cols]
        st.session_state.processed = True

    # 4. Filtros e Downloads (Apenas visível após o processamento)
    if st.session_state.get("processed", False):
        merged_df = st.session_state.merged_df
        
        # Métricas de Resumo
        st.header("📊 Resumo do Cruzamento")
        stats = merged_df["Resultado_Match"].value_counts()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Em Ambos", stats.get("Encontrado em Ambos", 0))
        c2.metric("Apenas no Excel A (Falhas em B)", stats.get("Apenas no Excel A (Falta no B)", 0))
        c3.metric("Apenas no Excel B (Falhas em A)", stats.get("Apenas no Excel B (Falta no A)", 0))
        
        # Sistema de Filtros Avançado
        st.header("🔍 Visualização e Filtros de Exportação")
        
        opcao_filtro = st.radio(
            "Selecione o conjunto de dados que pretende visualizar e descarregar:",
            ["Todos os Registos (Completo)", 
             "Apenas Correspondências (Ambos)", 
             "Apenas Falhas (Linhas sem correspondência em A ou B)",
             "Apenas Linhas em Falta no Excel B", 
             "Apenas Linhas em Falta no Excel A"]
        )
        
        # Aplicar a lógica do filtro escolhido
        if opcao_filtro == "Apenas Correspondências (Ambos)":
            df_filtrado = merged_df[merged_df["Resultado_Match"] == "Encontrado em Ambos"]
        elif opcao_filtro == "Apenas Falhas (Linhas sem correspondência em A ou B)":
            df_filtrado = merged_df[merged_df["Resultado_Match"] != "Encontrado em Ambos"]
        elif opcao_filtro == "Apenas Linhas em Falta no Excel B":
            df_filtrado = merged_df[merged_df["Resultado_Match"] == "Apenas no Excel A (Falta no B)"]
        elif opcao_filtro == "Apenas Linhas em Falta no Excel A":
            df_filtrado = merged_df[merged_df["Resultado_Match"] == "Apenas no Excel B (Falta no A)"]
        else:
            df_filtrado = merged_df

        st.write(f"A mostrar {len(df_filtrado)} registos com base no filtro selecionado:")
        st.dataframe(df_filtrado)
        
        # Função para gerar o ficheiro de download em memória
        def criar_excel_download(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Resultado')
            return output.getvalue()
            
        excel_data = criar_excel_download(df_filtrado)
        
        # Nome do ficheiro dinâmico com base no filtro
        nome_ficheiro = "resultado_" + opcao_filtro.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".xlsx"
        
        st.download_button(
            label=f"📥 Descarregar: {opcao_filtro}",
            data=excel_data,
            file_name=nome_ficheiro,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )