from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar_songs(df, input_artist, input_track, top_n=5):
    # Ensure that there are no NaN values in the relevant columns
    df = df.dropna(subset=['artists', 'track_name'])
    
    # Combine artist and track name into a single string and calculate TF-IDF
    df['combined'] = df['artists'] + " " + df['track_name']
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['combined'])

    # Input processing
    input_combined = input_artist + " " + input_track
    input_tfidf = tfidf.transform([input_combined])

    # Compute cosine similarity between input and all entries in the dataset
    cosine_similarities = cosine_similarity(input_tfidf, tfidf_matrix
                                            ).flatten()

    # Check for exact matches
    if cosine_similarities.max() > 0.99:
        top_indices = cosine_similarities.argsort()[-top_n:][::-1]
        return df.iloc[top_indices].drop_duplicates().head(top_n).iloc[1:,
                                                                       0:2]
    else:
        return "No similar songs found. Try adjusting your search terms."
