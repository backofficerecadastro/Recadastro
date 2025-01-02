import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from utils.data_utils import load_and_concatenate_data, preprocess_data, create_bar_chart, create_line_chart

# Configuração da Página
st.set_page_config(layout="wide")

def main():
        
    st.title("Dashboard Gerencial")

    # Carregar dados
    df = load_and_concatenate_data()

    # Pré-processar dados
    df = preprocess_data(df)
    
    # Configuração de Filtro
    l0 = list(df['Localidade'].unique())
    l0.sort()
    local = ['TODAS'] + l0

    m0 = list(df['Month'].unique())
    m0.sort(reverse=True)

    oc = ['VALIDÁVEL', 'NÃO VALIDÁVEL', 'TODAS']
    val = ['TODAS','Validado', 'Não Validado']

    #Botões
    localidade = st.sidebar.selectbox('Localidade', local)
    
    tipo_de_ocorrencia = st.sidebar.selectbox('Tipo de Ocorrência', oc)
    tipo_de_validação = st.sidebar.selectbox('Tipo de Validação', val)
    
    #Filtros
    if localidade == 'TODAS': filtro = local
    else: filtro = [localidade]
    
    if tipo_de_ocorrencia == 'TODAS': filtro2 = ['Validável', 'Não validável']
    else: filtro2 = [tipo_de_ocorrencia.capitalize()]

    if tipo_de_validação == 'TODAS': filtro3 = ['Validado', 'Não Validado', 'Aguardando Análise', 'Complemento de Fotos e Informações', 'Revisão Interna']
    else: filtro3 = [tipo_de_validação]

    
    df_filtrado = df[df['Localidade'].isin(filtro)]
    df_filtrado = df_filtrado[df_filtrado['Tipo de Ocorrência'].isin(filtro2)]
    df_filtrado = df_filtrado[df_filtrado['Tipo de Validação'].isin(filtro3)]
    df_filtrado = df_filtrado.sort_values(['Data do Cadastro'], ascending=False)

    # Criar o seletor de datas na página
    col01, col02 = st.columns(2)
    with col01:
        start_date = st.date_input(
            "Data Inicial",
            datetime(2024, 1, 1),
            min_value=datetime(2021, 6, 1),
            max_value=datetime(2026, 8, 1)
        )
    with col02:
        end_date = st.date_input(
            "Data Final",
            datetime(2025, 12, 31),
            min_value=datetime(2021, 6, 1),
            max_value=datetime(2026, 8, 1)
        )


    # Converter as datas selecionadas para o formato datetime64[ns]
    start_date_dt = pd.Timestamp(start_date)
    end_date_dt = pd.Timestamp(end_date)

    # Filtrar os dados com base no intervalo de datas selecionado

    mask = (df_filtrado['Data do Cadastro'] >= start_date_dt) & (df_filtrado['Data do Cadastro'] <= end_date_dt)
    filtered_df = df_filtrado.loc[mask]

    color_map = {'Validado': '#00049E', 'Não Validado': '#7275FE', 'Aguardando Análise': 'gray', 
                 'Complemento de Fotos e Informações': 'gray', 'Revisão Interna': 'gray',
                 'Validável': '#00049E', 'Não validável': 'gray', 'Total':'#706E6F'}
    color_map1 = ['#00049E','#7275FE']
    
    mes_total = filtered_df.groupby(['Month'])['Matrícula'].count().reset_index()
    total = mes_total['Matrícula'].sum()
    total_dia = len(list(filtered_df['Day'].unique()))
    st.markdown(f"<h3 style='font-size:18px;'> Total: {total:.0f} </h3>", unsafe_allow_html=True)
    fig_date = create_bar_chart(mes_total, 'Month', 'Matrícula',None, "Visitas por Mês", color_map1=color_map1)
    st.plotly_chart(fig_date)

    col11, col12 = st.columns(2)
    ano = col11.selectbox('Ano', df['Year'].unique())
    mes = col12.selectbox('Mês', m0)
    df_dia = df_filtrado[(df_filtrado['Year'] == ano) & (df_filtrado['Month'] == mes)]

    prod_dia = df_dia.groupby(['Day', 'Tipo de Ocorrência'])['Matrícula'].count().reset_index()
    fig_date1 = create_bar_chart(prod_dia, 'Day', 'Matrícula', None, "Visitas por dia", color_map1=color_map1)
    #prod_dia1 = df_filtrado.groupby(['Day'])['Matrícula'].count().reset_index()
    #fig_date.add_scatter(x=prod_dia1['Day'], y=prod_dia1['Matrícula'], mode='lines', name='Total')

    pivot_table = pd.pivot_table(df_dia, values='Matrícula', index=['Localidade','Agente do Cadastro'], columns='Day', aggfunc='count')#, fill_value=0)
    pivot_table['Total'] = pivot_table.sum(axis=1)
    media_valores = pivot_table.drop(columns=['Total']).mean(axis=1)
    media_valores = media_valores.round(0).astype(int)
    pivot_table['Média'] = media_valores
    total_dia = len(list(df_dia['Day'].unique()))
    total = pivot_table['Total'].sum()
    media = total/total_dia

    #Visuais da Tela
    st.markdown(f"<h3 style='font-size:18px;'> Total: {total:.0f} - Número de dias trabalhados: {total_dia} - Média: {media:.0f} </h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_date1)
    st.markdown("<h3 style='font-size:16px;'> Produção de Agentes por dia </h3>", unsafe_allow_html=True)
    st.dataframe(pivot_table)
    st.markdown("<h3 style='font-size:16px;'> Produção dos Validadores </h3>", unsafe_allow_html=True)
    st.write("")

if __name__ == "__main__":
    main()