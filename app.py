import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt

def load_data(start_date=None, end_date=None, product=None):
    url = 'http://localhost:8000/api/sales'
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    if product:
        params['product'] = product

    response = requests.get(url, params=params)
    data = response.json()
    if isinstance(data, list):
        return pd.DataFrame(data)
    else:
        st.error('Formato inesperado dos dados retornados na API')
        return pd.DataFrame()   

# Filtros
st.sidebar.header("Filtros")
start_date = st.sidebar.date_input('Data de Inicio', pd.to_datetime('2025-01-01'))
end_date = st.sidebar.date_input('Data de Fim', pd.to_datetime('2025-12-31'))
product = st.sidebar.text_input('Produto', '')


# Carregar os dados
data = load_data(start_date=start_date, end_date=end_date, product=product)

# Abas de Navegação
tab = st.selectbox("Selecione uma Aba",[
    "Tabela com Dados",
    "Gráfico de Vendas",
    "Análise Acumulada e Tendências"
])

if tab == "Tabela com Dados":
    st.title("Análise de Vendas")  
    st.subheader("Dataset de Vendas")
    st.dataframe(data, use_container_width=True)

    # Exportando Dados para CSV
    st.subheader('Exportar Dados para CSV')
    csv = data.to_csv(index=False)
    st.download_button(
        label='Baixar Dados com CSV',
        data=csv,
        file_name='dados_vendas.csv',
        mime='text/csv'
    )

elif tab == "Gráfico de Vendas":
    # Criar gráfico (Vendas por Data)
    st.subheader("Gráfico de Vendas por Data")
    fig, ax = plt.subplots()
    data['date'] = pd.to_datetime(data['date'])
    data.groupby('date')['quantity'].sum().plot(ax=ax)
    ax.set_xlabel('Data')
    ax.set_ylabel('Quantidade Vendida')
    st.pyplot(fig)

    # Gráfico (Vendas por Produto)
    st.subheader("Gráfico de Vendas por Produto")
    product_sales = data.groupby('product')['quantity'].sum().reset_index()
    fig2, ax2 = plt.subplots()
    product_sales.plot(
        kind='bar', x='product',
        y='quantity', ax=ax2
    )
    ax2.set_xlabel('Produto')
    ax2.set_ylabel('Quantidade Vendida')
    ax2.set_title('Vendas por Produto')
    st.pyplot(fig2)

elif tab == "Análise Acumulada e Tendências":
    # Analisar Tendencias de Vendas Mensais
    st.subheader('Tendências de Vendas Mensais')

    data['date'] = pd.to_datetime(data['date'])

    monthly_sales = data.resample('M', on='date')['quantity'].sum().reset_index()
    fig3, ax3 = plt.subplots()
    monthly_sales.plot(kind='line', x='date',
                    y='quantity', ax=ax3, marker='o')
    ax3.set_xlabel('Data')
    ax3.set_ylabel('Quantidade Vendida')
    ax3.set_title('Tendências de Vendas Mensais')
    st.pyplot(fig3)

    # Visualização de Vendas Acumuladas
    st.subheader('Vendas Acumuladas')
    data['cumulative_quantity'] = data.groupby('date')['quantity'].cumsum()
    fig4, ax4 = plt.subplots()
    data.groupby('date')['cumulative_quantity'].max().plot(ax=ax4)
    ax4.set_xlabel('Data')
    ax4.set_ylabel('Quantidade Vendida Acumulada')
    ax4.set_title('Vendas Acumuladas ao Longo do Tempo')
    st.pyplot(fig4)