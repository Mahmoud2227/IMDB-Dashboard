from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from src.dash1 import generate_visualizations as generate_visualizations1
from src.dash2 import generate_visualizations as generate_visualizations2
from src.dash3 import generate_visualizations as generate_visualizations3
from src.dash4 import generate_visualizations as generate_visualizations4

movies = pd.read_csv('./movie_after_cleaning.csv')
movies_splits = pd.read_excel("./splits_movie.xlsx", sheet_name=None)
series = pd.read_csv('./series_after_cleaning.csv')
series_splits = pd.read_excel("./splits_series.xlsx", sheet_name=None)

numofcountries=len(movies_splits["country"]["country"].groupby(movies_splits["country"]["country"]).count().sort_values(ascending=False).index)
numoflang=len(movies_splits["language"]["language"].groupby(movies_splits["language"]["language"]).count().sort_values(ascending=False).index)
numofmoives=movies.shape[0]+series.shape[0]
avgvotes=int(movies["votes"].mean()+series["votes"].mean())

# Define function to load data based on tab selection
def load_data(tab):
    if tab == 'movie':
        return movies, movies_splits
    elif tab == 'series':
        return series, series_splits

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

def generate_stats_card (title, value, image_path):
    return html.Div(
        dbc.Card([
            dbc.CardImg(src=image_path, top=True, style={'width': '50px','alignSelf': 'center'}),
            dbc.CardBody([
                html.P(value, className="card-value", style={'margin': '0px'}),
                html.H4(title, className="card-title")
            ], style={'textAlign': 'center'}),
        ], style={'paddingBlock':'10px',"backgroundColor":'#deb522','border':'none','borderRadius':'10px'})
    )


tab_style = {
    'idle':{
        'borderRadius': '10px',
        'padding': '0px',
        'marginInline': '5px',
        'display':'flex',
        'alignItems':'center',
        'justifyContent':'center',
        'fontWeight': 'bold',
        'backgroundColor': '#deb522',
        'border':'none'
    },
    'active':{
        'borderRadius': '10px',
        'padding': '0px',
        'marginInline': '5px',
        'display':'flex',
        'alignItems':'center',
        'justifyContent':'center',
        'fontWeight': 'bold',
        'border':'none',
        'textDecoration': 'underline',
        'backgroundColor': '#deb522'
    }
}


# Define the layout of the app
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Img(src="./assets/imdb.png",width=150), width=3),
            dbc.Col(
                dcc.Tabs(id='graph-tabs', value='overview', children=[
                    dcc.Tab(label='Overview', value='overview',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='Content creators', value='content_creators',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='Country', value='country',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='genre', value='genre',style=tab_style['idle'],selected_style=tab_style['active']),
                ], style={'marginTop': '15px', 'width':'600px','height':'50px'})
            ,width=7),
        ]),
        dbc.Row([
            dbc.Col(generate_stats_card("Work",numofmoives,"./assets/movie-icon.png"), width=3,style={'paddingRight': '5px'}),
            dbc.Col(generate_stats_card("Language", numoflang,"./assets/language-icon.svg"), width=3,style={'padding': '5px'}),
            dbc.Col(generate_stats_card("Country",numofcountries,"./assets/country-icon.png"), width=3,style={'padding': '5px'}),
            dbc.Col(generate_stats_card("Average Votes",avgvotes,"./assets/vote-icon.png"), width=3,style={'paddingLeft': '5px'}),
        ],style={'marginBlock': '10px'}),
        dbc.Row([
            dcc.Tabs(id='tabs', value='movie', children=[
                dcc.Tab(label='Movie', value='movie',style={'border':'1px line white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold'},selected_style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold','textDecoration': 'underline'}),
                dcc.Tab(label='Series', value='series',style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold'},selected_style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold','textDecoration': 'underline'}),
            ], style={'padding': '0px'})
        ]),
        dbc.Row([
            html.Div(id='tabs-content')
        ])
    ], style={'padding': '0px'})
],style={'backgroundColor': 'black', 'minHeight': '100vh'})

@app.callback(
    Output('tabs-content', 'children'),
    [Input('graph-tabs', 'value'),Input('tabs', 'value')]
)
def update_tab(tab,tab2):
    data, splits = load_data(tab2)

    if tab == 'overview':
        fig1, fig2, fig3, fig4 = generate_visualizations2(data, splits)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph2', figure=fig2),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph3', figure=fig3),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph4', figure=fig4),
        ], style={'width': '50%', 'display': 'inline-block'})
    ])
    elif tab == 'content_creators':
        fig1, fig2, fig3, fig4 = generate_visualizations2(data, splits)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph2', figure=fig2),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph3', figure=fig3),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph4', figure=fig4),
        ], style={'width': '50%', 'display': 'inline-block'})
    ])
    elif tab == 'country':
        fig1, fig2 = generate_visualizations3(data, splits)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph2', figure=fig2),
        ], style={'width': '50%', 'display': 'inline-block'}),
        ])
    elif tab == 'genre':
        fig1, fig2 = generate_visualizations4(data, splits)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph2', figure=fig2),
        ], style={'width': '50%', 'display': 'inline-block'}),
        ])

# Run the app
if __name__ == '__main__':
    # app.run_server(debug=True, dev_tools_hot_reload=True)
    app.run_server(debug=False)
