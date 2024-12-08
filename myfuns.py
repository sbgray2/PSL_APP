import pandas as pd
import requests
import numpy as np
# Define the URL for movie data
myurl = "https://liangfgithub.github.io/MovieData/movies.dat?raw=true"
# Fetch the data from the URL
response = requests.get(myurl)
# Split the data into lines and then split each line using "::"
movie_lines = response.text.split('\n')
movie_data = [line.split("::") for line in movie_lines if line]
# Create a DataFrame from the movie data
movies = pd.DataFrame(movie_data, columns=['movie_id', 'title', 'genres'])
movies['movie_id'] = movies['movie_id'].astype(int)
movies['movie_idm'] = movies['movie_id'].astype(int)
movies.set_index('movie_idm', inplace=True)
genres = list(
    sorted(set([genre for genres in movies.genres.unique() for genre in genres.split("|")]))
)
S_top_30 = pd.read_csv('s30.csv')
num_movie = S_top_30.shape[0]
def get_displayed_movies():
    return movies.head(100)
def get_recommended_movies(new_user_ratings):
    new_user = np.zeros(num_movie)
    new_user.fill(np.nan)
    for id, rating in new_user_ratings.items():
        column_name = f"m{id}"
        if column_name in S_top_30.columns:
            index = S_top_30.columns.get_loc(column_name)
            new_user[index] = rating
    top10 = myIBCF(new_user)
    column_mapping = [col[1:] for col in top10 if col.startswith('m')]
    print(column_mapping)
    return movies.iloc[column_mapping]
def get_popular_movies(genre: str):
    if genre == genres[1]:
        return movies.head(10)
    else: 
        return movies[10:20]
def myIBCF(newuser):
    newRanks = np.zeros(num_movie)
    movies_with_rating = ~np.isnan(newuser)
    movies_without_rating = np.where(np.isnan(newuser))[0]
    smr_zero = np.nan_to_num(S_top_30)
    for i in movies_without_rating:
        right_sum = np.dot(newuser[movies_with_rating],smr_zero[i,movies_with_rating])
        left_sum = sum(smr_zero[i,movies_with_rating])
        score = (1/left_sum)*right_sum
        newRanks[i] = score
    non_nan_indices = np.where(~np.isnan(newRanks))[0]  # Find indices of non-NA values
    sorted_indices = np.argsort(newRanks[non_nan_indices])[::-1]
    top_10_indices = non_nan_indices[sorted_indices][:10]  # Get top 10 indices
    #print(newRanks[top_10_indices])
    return S_top_30.columns[top_10_indices]