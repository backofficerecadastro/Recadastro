import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from utils.data_utils import load_and_concatenate_data, preprocess_data, create_bar_chart, create_line_chart

# Definir a estrutura da aplicação Streamlit
st.set_page_config(page_title="Seletor de Datas Deslizante")
st.title("Seletor de Datas Deslizante")

# Carregar os dados
df0 = load_and_concatenate_data()
df = preprocess_data(df0)

# Criar o seletor de datas deslizante
start_date = st.sidebar.date_input(
    "Data Inicial",
    datetime(2024, 6, 1),
    min_value=datetime(2024, 1, 1),
    max_value=datetime(2026, 6, 1)
)

end_date = st.sidebar.date_input(
    "Data Final",
    datetime(2024, 12, 6),
    min_value=datetime(2024, 1, 1),
    max_value=datetime(2026, 6, 1)
)

# Configuração de Filtro
l0 = list(df['Localidade'].unique())
l0.sort()
local = ['TODAS'] + l0
oc = ['VALIDÁVEL', 'NÃO VALIDÁVEL', 'TODAS']
val = ['TODAS','Validado', 'Não Validado']
localidade = st.sidebar.selectbox('Localidade', local)
tipo_de_validação = st.sidebar.selectbox('Tipo de Validação', val)
tipo_de_ocorrencia = st.sidebar.selectbox('Tipo de Ocorrência', oc)

# Converter as datas selecionadas para o formato datetime64[ns]
start_date_dt = pd.Timestamp(start_date)
end_date_dt = pd.Timestamp(end_date)

# Filtrar os dados com base no intervalo de datas selecionado
mask = (df['Data do Cadastro'] >= start_date_dt) & (df['Data do Cadastro'] <= end_date_dt)
filtered_df = df.loc[mask]
