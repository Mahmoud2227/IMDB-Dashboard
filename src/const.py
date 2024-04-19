import pandas as pd

def get_constants(movies, series, movies_splits, series_splits):

    num_of_works=movies.shape[0]+series.shape[0]

    countries_movies=movies_splits["country"]["country"].groupby(movies_splits["country"]["country"]).count().sort_values(ascending=False).index 
    countries_series=series_splits["country"]["country"].groupby(movies_splits["country"]["country"]).count().sort_values(ascending=False).index 
    num_of_countries=len(countries_movies.append(countries_series).unique())

    languages_movies=movies_splits["language"]["language"].groupby(movies_splits["language"]["language"]).count().sort_values(ascending=False).index
    language_series=series_splits["language"]["language"].groupby(movies_splits["language"]["language"]).count().sort_values(ascending=False).index
    num_of_lang=len(languages_movies.append(language_series).unique())
    avg_votes=int((movies["votes"].mean()+series["votes"].mean())/2)

    return num_of_works,num_of_countries,num_of_lang,avg_votes