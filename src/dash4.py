import plotly.express as px

# Define visualizations
def generate_visualizations(series, splits):
    # New visualization 1
    df1 = series.groupby("year").size().reset_index(name='count')
    fig_line_count = px.line(df1, x='year', y='count', title='Work Count Over Time')

    # Update line color to yellow
    fig_line_count.update_traces(line=dict(color='yellow'))

    # Update layout with dark template and yellow font color
    fig_line_count.update_layout(template='plotly_dark', font=dict(color='yellow'))

    # New visualization 2

    df2 = series.groupby("year")["votes"].mean().reset_index(name='votes')
    fig_line_votes = px.line(df2, x='year', y='votes', title='Work Votes Over Time')

# Update line color to yellow
    fig_line_votes.update_traces(line=dict(color='yellow'))

# Update layout with dark template and yellow font color
    fig_line_votes.update_layout(template='plotly_dark', font=dict(color='yellow'))

    return fig_line_count, fig_line_votes