import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def latent_recommended_urls(n, url):
    # Load the latent factors DataFrame
    article_info_file_path = os.path.join(os.path.dirname(__file__), 'article_infos.pkl')
    with open(article_info_file_path, 'rb') as f:
        article_info_df = pickle.load(f)

    file_path = os.path.join(os.path.dirname(__file__), 'trained_article_latent_matrix.pkl')
    with open(file_path, 'rb') as f:
        article_latent_df = pickle.load(f)

    # Ensure the URL exists in the DataFrame index
    if url not in article_latent_df['url'].values:
        raise ValueError(f"URL {url} not found in the latent factors dataset.")

    # Extract the latent factors of the input URL
    row = article_latent_df.loc[article_latent_df['url'] == url]

    input_vector = row.values.flatten()[1:].reshape(1, -1)

    # Calculate cosine similarity for all URLs
    latent_vectors = article_latent_df.drop(columns=['url']).values

    similarities = cosine_similarity(input_vector, latent_vectors).flatten()

    # Create a DataFrame to store similarity scores with URLs
    similarity_df = pd.DataFrame({
        'url': article_latent_df['url'],
        'similarity': similarities
    })

    # Exclude the input URL and sort by similarity in descending order
    similar_urls = similarity_df[similarity_df['url'] != url].sort_values(by='similarity', ascending=False)
    selected_urls = similar_urls.head(n)['url'].tolist()

    # return
    result = []

    for url in selected_urls:
        row = article_info_df.loc[article_info_df['url'] == url].iloc[0]
        result.append(row.to_dict())

    return result
