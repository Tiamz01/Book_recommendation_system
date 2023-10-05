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


def recommend_books(book_name):
    try:
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

        suggested_books = []
        for i in range(len(suggestions[0])):
            suggested_book = book_pivot.index[suggestions[0][i]]
            if suggested_book != book_name:  # Exclude the searched book from suggestions
                suggested_books.append(suggested_book)

        # Join the suggested book titles with line breaks
        return '\n'.join(suggested_books)

    except IndexError:
        return f'Book "{book_name}" not found in the dataset. Please try another book.'


# Streamlit UI
st.title('Book Recommendation System')
input_book_name = st.text_input('Enter a book name:')
if st.button('Recommend'):
    suggested_books = recommend_books(input_book_name)
    st.subheader('Book suggestions:')
    st.write(suggested_books)
