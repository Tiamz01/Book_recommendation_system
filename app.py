import streamlit as st
import joblib
import numpy as np
import sklearn


# Load the User-Book Ratings DataFrame
user_book_ratings = joblib.load('user_book_ratings.joblib')

# Load the Pivot Table
book_pivot = joblib.load('book_pivot_table.joblib')

# Load the k-Nearest Neighbors model
model = joblib.load('model.joblib')


def recommend_book(book_name):
    try:
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

        print(f'The book suggestions for {book_name} are:')
        for i in range(len(suggestions[0])):
            print(book_pivot.index[suggestions[0][i]])

    except IndexError:
        print(f'{book_name} is not available. You can check out the books below instead')


# Display
st.title('Book recommendation system')
input_book_name = st.text_input('Find your favorite book')
if st.button('Search'):
    print(recommend_book(input_book_name))
