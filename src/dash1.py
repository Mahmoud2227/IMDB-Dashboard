import plotly.express as px

def generate_visualizations(series, splits):
    top_five_genres = series["parentalguide"].value_counts().head(10).reset_index(name='count')
    fig_treemap = px.treemap(top_five_genres, 
                             path=['parentalguide'],  
                             values='count', 
                             title='Top Parental Guides',
                             color='count',color_continuous_scale='viridis')
    fig_treemap.update_layout(template='plotly_dark', font=dict(color='yellow'))

    top_values_language = splits["genre"]["genre"].value_counts().head(10).reset_index(name='count')
    total_count_language = top_values_language['count'].sum()
    top_values_language['percentage'] = (top_values_language['count'] / total_count_language) * 100
    fig_bar_language = px.bar(top_values_language, x='count', y="genre", orientation='h',
                              color='count', text='percentage',
                              title='Top genres',
                              labels={'count': 'Count', 'index': 'genre', 'percentage': 'Percentage'},
                              color_continuous_scale='Viridis')
    fig_bar_language.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_bar_language.update_layout(yaxis=dict(categoryorder='total ascending'))
    fig_bar_language.update_layout(template='plotly_dark', font=dict(color='yellow'))

    top_countries = splits["country"]["country"].value_counts().head(30).reset_index(name='count')
    country_mapping = {
        'United States': 'USA',
        'United Kingdom': 'GBR',
        'France': 'FRA',
        'Canada': 'CAN',
        'Germany': 'DEU',
        'Japan': 'JPN',
        'India': 'IND',
        'Australia': 'AUS',
        'China': 'CHN',
        'Italy': 'ITA',
        'Spain': 'ESP',
        'Mexico': 'MEX',
        'Hong Kong': 'HKG',
        'Sweden': 'SWE',
        'Denmark': 'DNK',
        'New Zealand': 'NZL',
        'Belgium': 'BEL',
        'South Korea': 'KOR',
        'Ireland': 'IRL',
        'Czech Republic': 'CZE',
        'Switzerland': 'CHE',
        'Hungary': 'HUN',
        'Norway': 'NOR',
        'United Arab Emirates': 'ARE',
        'Netherlands': 'NLD',
        'South Africa': 'ZAF',
        'Poland': 'POL',
        'West Germany': 'DEU',  # Assuming you want to use 'DEU' for Germany
        'Austria': 'AUT',
        'Turkey': 'TUR'
    }
    # Assuming 'df' is your DataFrame
    top_countries['country'] = top_countries['country'].map(country_mapping)

    fig_choropleth = px.choropleth(top_countries, 
                                    locations="country",
                                    color="count",
                                    hover_name="country",
                                    title="Top Countries producing",
                                    projection="natural earth",
                                    color_continuous_scale='Viridis')
    fig_choropleth.update_layout(template='plotly_dark', font=dict(color='yellow'))
    
    # Generate box plot for ratings
    fig_boxplot = px.box(series, x="rating", title='Ratings Distribution')
    fig_boxplot.update_traces(marker=dict(color='yellow'))
    fig_boxplot.update_layout(template='plotly_dark', font=dict(color='yellow'))


    return fig_treemap, fig_bar_language, fig_choropleth, fig_boxplot