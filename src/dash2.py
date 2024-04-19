import plotly.express as px
def generate_visualizations(series, splits):
    top_five_genres = splits["creators"]["creators"].value_counts().head(3).reset_index(name='count')
    fig_donut1 = px.pie(top_five_genres, 
                             names='creators',  
                             values='count', 
                             title='Top creators',
                             
                             hole=0.5)
    fig_donut1.update_layout(template='plotly_dark', font=dict(color='yellow'))

    top_values_country = splits["production_company"]["production_company"].value_counts().head(10).reset_index(name='count')
    total_count_country = top_values_country['count'].sum()
    top_values_country['percentage'] = (top_values_country['count'] / total_count_country) * 100
    fig_bar_country = px.bar(top_values_country, x='count', y="production_company", orientation='h',
                             color='count', text='percentage',
                             title='Top Productions Company',
                             labels={'count': 'Count', 'index': 'Production Company', 'percentage': 'Percentage'})
    fig_bar_country.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_bar_country.update_layout(yaxis_title='Production Company')
    fig_bar_country.update_layout(yaxis=dict(categoryorder='total ascending'))
    fig_bar_country.update_layout(template='plotly_dark', font=dict(color='yellow'))

    top_values_language = splits["stars"]["stars"].value_counts().head(10).reset_index(name='count')
    total_count_language = top_values_language['count'].sum()
    top_values_language['percentage'] = (top_values_language['count'] / total_count_language) * 100
    fig_bar_language = px.bar(top_values_language, y='count', x="stars", orientation='v',
                              color='count', text='percentage',
                              title='Top stars',
                              labels={'count': 'Count', 'index': 'stars', 'percentage': 'Percentage'})
    fig_bar_language.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_bar_language.update_layout(yaxis=dict(categoryorder='total ascending'))
    fig_bar_language.update_layout(template='plotly_dark', font=dict(color='yellow'))

    top_values = splits["language"]["language"].value_counts().head(10).reset_index(name='count')
    # Calculate percentage
    total_count = top_values['count'].sum()
    top_values['percentage'] = (top_values['count'] / total_count) * 100

    fig_bar_language2 = px.bar(top_values, y='count', x="language", orientation='v',
                               color='count', text='percentage',
                               title='Top Languages',
                               labels={'count': 'Count', 'index': 'Language', 'percentage': 'Percentage'})

    fig_bar_language2.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_bar_language2.update_layout(yaxis=dict(categoryorder='total ascending'))
    fig_bar_language2.update_layout(template='plotly_dark', font=dict(color='yellow'))

    return fig_donut1, fig_bar_country, fig_bar_language, fig_bar_language2