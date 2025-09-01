import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Importar os dados
# 'parse_dates' converte a coluna 'date' para o tipo datetime.
# 'index_col' define a coluna 'date' como o índice do DataFrame.
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2. Limpar os dados
# Filtrar dias em que as visualizações de página estavam nos 2,5% inferiores ou 2,5% superiores.
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Criar uma cópia do dataframe para esta função
    df_line = df.copy()

    # 3. Desenhar o gráfico de linha
    # 'figsize' define o tamanho da figura para melhor visualização.
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Plota os dados: índice (datas) no eixo x, 'value' (visualizações) no eixo y.
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)
    
    # Configurar título e rótulos conforme especificado nos testes.
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Salvar imagem e retornar a figura (não mude esta parte)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # 4. Preparar dados para o gráfico de barras
    # Copiar o dataframe para evitar modificações no original.
    df_bar = df.copy()
    
    # Extrair o ano e o mês do índice. O índice é do tipo datetime.
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Agrupar por ano e mês para calcular a média de visualizações.
    # 'unstack' transforma os meses em colunas, o que é ideal para um gráfico de barras agrupado.
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Reordenar as colunas dos meses para a ordem correta (Janeiro, Fevereiro, ...).
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar = df_bar[months_order]

    # 5. Desenhar o gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(10, 6)).get_figure()
    
    ax = fig.gca() # Pega o eixo atual
    
    # Configurar rótulos e legenda conforme especificado.
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    # Salvar imagem e retornar a figura (não mude esta parte)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Preparar dados para os box plots (esta parte já estava pronta!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # 6. Desenhar os box plots usando Seaborn
    # 'fig, axes' cria uma figura com dois subplots (1 linha, 2 colunas).
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Primeiro Box Plot: Tendência Anual
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Segundo Box Plot: Sazonalidade Mensal
    # 'order' garante que os meses sejam plotados na ordem correta.
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Salvar imagem e retornar a figura (não mude esta parte)
    fig.savefig('box_plot.png')
    return fig
