from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from src.const import get_constants

from src.dash1 import generate_visualizations as generate_visualizations1
from src.dash2 import generate_visualizations as generate_visualizations2
from src.dash3 import generate_visualizations as generate_visualizations3
from src.dash4 import generate_visualizations as generate_visualizations4

movies = pd.read_csv('./movie_after_cleaning.csv')
movies_splits = pd.read_excel("./splits_movie.xlsx", sheet_name=None)
series = pd.read_csv('./series_after_cleaning.csv')
series_splits = pd.read_excel("./splits_series.xlsx", sheet_name=None)

# Define function to load data based on tab selection
def load_data(tab):
    if tab == 'movie':
        return movies, movies_splits
    elif tab == 'series':
        return series, series_splits

num_of_works,num_of_countries,num_of_lang,avg_votes = get_constants(movies, series, movies_splits, series_splits)


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

def generate_stats_card (title, value, image_path):
    return html.Div(
        dbc.Card([
            dbc.CardImg(src=image_path, top=True, style={'width': '50px','alignSelf': 'center'}),
            dbc.CardBody([
                html.P(value, className="card-value", style={'margin': '0px','fontSize': '22px','fontWeight': 'bold'}),
                html.H4(title, className="card-title", style={'margin': '0px','fontSize': '18px','fontWeight': 'bold'})
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

MAX_OPTIONS_DISPLAY = 3300

# Generate options for the dropdown
dropdown_options_movie = [{'label': title, 'value': title} for title in movies['title'][:MAX_OPTIONS_DISPLAY]]
dropdown_options_series = [{'label': title, 'value': title} for title in series['title'][:MAX_OPTIONS_DISPLAY]]


offcanvas = html.Div(
    [
        dbc.Button("Movie Recommendation", id="open-movie-offcanvas", n_clicks=0, style={'backgroundColor':'#deb522','color':'black','fontWeight': 'bold','border':'none'}),
        dbc.Offcanvas(html.Div([
            dcc.Dropdown(
            id='movie-dropdown',
            options=dropdown_options_movie,
            placeholder='Select a movie...',
            searchable=True,
            style={'color':'black'}
            ),
            dcc.Loading(html.Div(id='movie-recommendation-content'),type='circle',color='#deb522',style={'marginTop': '60px'})]),
            id="movie-recommendation-offcanvas",
            title="Movie Recommendations",
            is_open=False,
            style={'backgroundColor':"black",'color':'#deb522'}
        ),
        dbc.Button("Series Recommendation", id="open-series-offcanvas", n_clicks=0, style={'backgroundColor':'#deb522','color':'black','fontWeight': 'bold','border':'none'}),
        dbc.Offcanvas(html.Div([
            dcc.Dropdown(
            id='series-dropdown',
            options=dropdown_options_series,
            placeholder='Select a series...',
            searchable=True,
            style={'color':'black'}
            ),
            dcc.Loading(html.Div(id='series-recommendation-content'),type='circle',color='#deb522',style={'marginTop': '60px'})]),
            id="series-recommendation-offcanvas",
            title="Series Recommendations",
            is_open=False,
            style={'backgroundColor':"black",'color':'#deb522'}
        )
    ],
    style={'display': 'flex', 'justifyContent': 'space-between','marginTop': '20px'}
)

# Define the layout of the app
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Img(src="./assets/imdb.png",width=150), width=2),
            dbc.Col(
                dcc.Tabs(id='graph-tabs', value='overview', children=[
                    dcc.Tab(label='Overview', value='overview',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='Content creators', value='content_creators',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='Parental Guide', value='parental',style=tab_style['idle'],selected_style=tab_style['active']),
                    dcc.Tab(label='Year', value='year',style=tab_style['idle'],selected_style=tab_style['active'])
                ], style={'marginTop': '15px', 'width':'600px','height':'50px'})
            ,width=6),
            dbc.Col(offcanvas, width=4)
        ]),
        dbc.Row([
            
            dbc.Col(generate_stats_card("Work",num_of_works,"./assets/movie-icon.png"), width=3),
            dbc.Col(generate_stats_card("Language", num_of_lang,"./assets/language-icon.svg"), width=3),
            dbc.Col(generate_stats_card("Country",num_of_countries,"./assets/country-icon.png"), width=3),
            dbc.Col(generate_stats_card("Average Votes",avg_votes,"./assets/vote-icon.png"), width=3),
        ],style={'marginBlock': '10px'}),
        dbc.Row([
            dcc.Tabs(id='tabs', value='movie', children=[
                dcc.Tab(label='Movie', value='movie',style={'border':'1px line white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold'},selected_style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold','textDecoration': 'underline'}),
                dcc.Tab(label='Series', value='series',style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold'},selected_style={'border':'1px solid white','backgroundColor':'black','color': '#deb522','fontWeight': 'bold','textDecoration': 'underline'}),
            ], style={'padding': '0px'})
        ]),
        dbc.Row([
            dcc.Loading([
                html.Div(id='tabs-content')
            ],type='default',color='#deb522')
        ])
    ], style={'padding': '0px'})
],style={'backgroundColor': 'black', 'minHeight': '100vh'})

@app.callback(
    Output("movie-recommendation-offcanvas", "is_open"),
    Input("open-movie-offcanvas", "n_clicks"),
    [State("movie-recommendation-offcanvas", "is_open")],
)
def toggle_offcanvas_movie(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    Output("series-recommendation-offcanvas", "is_open"),
    Input("open-series-offcanvas", "n_clicks"),
    [State("series-recommendation-offcanvas", "is_open")],
)
def toggle_offcanvas_series(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Function to get recommendations
def get_recommendations(df, indices, title, cosine_sim):
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:6]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df['title'].iloc[movie_indices]

# Callback to update image container based on dropdown selection
@app.callback(
    Output('movie-recommendation-content', 'children'),
    [Input('movie-dropdown', 'value')]
)
def update_recommendation_movie(selected_movie):
    df = movies.copy()
    df["word_cloud"]=movies["description"]+" "+movies["genre"]+" "+movies["director"]+" "+movies["writer"]+" "+movies["country"]
    tfidf = TfidfVectorizer(stop_words='english')
    df["word_cloud"] = df["word_cloud"].fillna('')  
    tfidf_matrix = tfidf.fit_transform(df['word_cloud'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    if selected_movie:
        x = []
        for i in range(0, 5):
            x.append(movies[movies["title"] == get_recommendations(movies,indices,selected_movie,cosine_sim).iloc[i]][["link","title"]])
    else:
        return []
    
    return html.Div(children=[
            dcc.Link(f"{i+1} - {data['title'].values[0]}", href=data['link'].values[0], style={'display':'block','color':'#deb522','marginBlock':'10px'}
                    ,target='_blank') for i, data in enumerate(x)
    ],style={'marginTop': '10px','textAlign': 'center','color': '#deb522'})

@app.callback(
    Output('series-recommendation-content', 'children'),
    [Input('series-dropdown', 'value')]
)
def update_recommendation_series(selected_series):
    df = series.copy()
    df["word_cloud"]=series["description"]+" "+series["genre"]+" "+series["creators"]+" "+series["stars"]+" "+series["country"] +" "+ series['production_company'] +" "+ series['parentalguide']
    tfidf = TfidfVectorizer(stop_words='english')
    df["word_cloud"] = df["word_cloud"].fillna('')  
    tfidf_matrix = tfidf.fit_transform(df['word_cloud'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    
    if selected_series:
        x = []
        for i in range(0, 5):
            x.append(series[series["title"] == get_recommendations(series,indices,selected_series,cosine_sim).iloc[i]][["link", "title"]])
    else:
        return []
    return html.Div(children=[
            dcc.Link(f"{i+1} - {data['title'].values[0]}", href=data['link'].values[0], style={'display':'block','color':'#deb522','marginBlock':'10px'}
                    ,target='_blank') for i, data in enumerate(x)
    ],style={'marginTop': '10px','textAlign': 'center','color': '#deb522'})


@app.callback(
    Output('tabs-content', 'children'),
    [Input('graph-tabs', 'value'),Input('tabs', 'value')]
)
def update_tab(tab,tab2):
    data, splits = load_data(tab2)

    if tab == 'overview':
        fig1, fig2, fig3, fig4 = generate_visualizations1(data, splits)
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
    elif tab == 'parental':
        fig1, fig2 = generate_visualizations3(data, splits)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph2', figure=fig2),
        ], style={'width': '50%', 'display': 'inline-block'}),
        ])
    elif tab == 'year':
        fig1, fig2 = generate_visualizations4(data, splits)
        return html.Div([
        html.Div([
            dcc.Graph(id='graph1', figure=fig1),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(id='graph2', figure=fig2),
        ], style={'width': '50%', 'display': 'inline-block'}),
        ])


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)