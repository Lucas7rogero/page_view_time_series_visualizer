import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# importa os dados e ja transforma "date" em datetime
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# remove os dias com valores outliers
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    df_line = df.copy()

    # grafico de linha mostrando a evolucao das visualizacoes
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()

    # cria colunas para ano e mes
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # media de visualizacoes por ano e mes
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # coloca os meses na ordem
    months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
    df_bar = df_bar[months_order]

    # grafico de barras agrupadas (anos x meses)
    fig = df_bar.plot(kind='bar', figsize=(10, 6)).get_figure()
    ax = fig.gca()

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy().reset_index()
    df_box['year'] = df_box.date.dt.year
    df_box['month'] = df_box.date.dt.strftime('%b')

    # dois boxplots lado a lado (tendencia anual e sazonalidade mensal)
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # boxplot por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # boxplot por mes (ordem correta dos meses)
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig('box_plot.png')
    return fig
