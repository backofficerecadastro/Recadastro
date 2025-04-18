import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_utils import load_and_concatenate_data, preprocess_data, create_bar_chart, create_line_chart

# Configuração da Página
st.set_page_config(layout="wide")

def main():
        
    st.title("Dashboard de Visitas por hora")
        # Carregar dados
    df = load_and_concatenate_data()

    # Pré-processar dados
    df = preprocess_data(df)
    
    # Configuração de Filtro
    l0 = list(df['Localidade'].unique())
    l0.sort()
    local = ['TODAS'] + l0

    oc = ['VALIDÁVEL', 'NÃO VALIDÁVEL', 'TODAS']
    val = ['TODAS','Validado', 'Não Validado']

    #Botões
    localidade = st.sidebar.selectbox('Localidade', local)
    ano = st.sidebar.selectbox('Ano', df['Year'].unique())
    mes = st.sidebar.selectbox('Mês', df['Year'].unique())
    dia = st.sidebar.selectbox('Dia', df['Day'].unique())
    tipo_de_ocorrencia = st.sidebar.selectbox('Tipo de Ocorrência', oc)
    tipo_de_validação = st.sidebar.selectbox('Tipo de Validação', val)
    
    #Filtros
    if localidade == 'TODAS': filtro = local
    else: filtro = [localidade]
    
    if tipo_de_ocorrencia == 'TODAS': filtro2 = ['Validável', 'Não validável']
    else: filtro2 = [tipo_de_ocorrencia.capitalize()]

    if tipo_de_validação == 'TODAS': filtro3 = ['Validado', 'Não Validado', 'Aguardando Análise', 'Complemento de Fotos e Informações', 'Revisão Interna']
    else: filtro3 = [tipo_de_validação]

    df_filtrado = df[(df['Year'] == ano) & (df['Month'] == mes) & (df['Day'] == dia)]
    df_filtrado = df_filtrado[df_filtrado['Localidade'].isin(filtro)]
    df_filtrado = df_filtrado[df_filtrado['Tipo de Ocorrência'].isin(filtro2)]
    df_filtrado = df_filtrado[df_filtrado['Tipo de Validação'].isin(filtro3)]
    df_filtrado = df_filtrado.sort_values(['Data do Cadastro'], ascending=False)

    color_map = {'Validado': '#00049E', 'Não Validado': '#7275FE', 'Aguardando Análise': 'gray', 
                 'Complemento de Fotos e Informações': 'gray', 'Revisão Interna': 'gray',
                 'Validável': '#00049E', 'Não validável': 'gray', 'Total':'#706E6F'}
    color_map1 = ['#00049E','#7275FE']

    prod_dia = df_filtrado.groupby(['Hour', 'Tipo de Ocorrência'])['Matrícula'].count().reset_index()
    
    fig_date = create_line_chart(prod_dia, 'Hour', 'Matrícula', 'Tipo de Ocorrência', "Visitas por dia", color_map=color_map)
    st.plotly_chart(fig_date)
    
    pivot_table = pd.pivot_table(df_filtrado, values='Matrícula', index=['Localidade','Agente do Cadastro'], columns='Hour', aggfunc='count')#, fill_value=0)
    pivot_table['Total'] = pivot_table.sum(axis=1)
    media_valores = pivot_table.drop(columns=['Total']).mean(axis=1)
    media_valores = media_valores.round(0).astype(int)
    pivot_table['Média'] = media_valores

    df_filtrado2 = df[df['Validador']!=0]
    df_filtrado2 = df[(df['Ano de Validação'] == ano) & (df['Mês de Validação'] == mes) & (df['Dia de Validação'] == dia)]
    df_filtrado2 = df_filtrado2[df_filtrado2['Localidade'].isin(filtro)]
    df_filtrado2 = df_filtrado2[df_filtrado2['Tipo de Ocorrência'].isin(filtro2)]
    df_filtrado2 = df_filtrado2[df_filtrado2['Tipo de Validação'].isin(filtro3)]
    df_filtrado2 = df_filtrado2.sort_values(['Data da Validação'], ascending=False)

    pivot_validavel = pd.pivot_table(df_filtrado2, values='Matrícula', index=['Validador'], columns='Hora de Validação', aggfunc='count')
    pivot_validavel['Total'] = pivot_validavel.sum(axis=1)
    media_validavel = pivot_validavel.drop(columns=['Total']).mean(axis=1)
    media_validavel = media_validavel.round(0).astype(int)
    pivot_validavel['Média'] = media_validavel

    st.markdown("<h3 style='font-size:16px;'> Produção de Agentes por Hora </h3>", unsafe_allow_html=True)
    st.dataframe(pivot_table)
    st.markdown("<h3 style='font-size:16px;'> Produção de Validadores por Hora </h3>", unsafe_allow_html=True)
    st.dataframe(pivot_validavel)


if __name__ == "__main__":
    main()