import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def latent_recommended_urls(n, url):
    # Load the latent factors DataFrame
    file_path = os.path.join(os.path.dirname(__file__), 'trained_article_latent_matrix.pkl')
    with open(file_path, 'rb') as f:
        article_latent_df = pickle.load(f)

    # Ensure the URL exists in the DataFrame
    if url not in article_latent_df.index:
        raise ValueError(f"URL {url} not found in the latent factors dataset.")

    # Extract the latent factors of the input URL
    input_vector = article_latent_df.loc[url].values.reshape(1, -1)

    # Calculate cosine similarity for all URLs
    similarities = cosine_similarity(input_vector, article_latent_df.values).flatten()

    # Create a DataFrame to store similarity scores with URLs
    similarity_df = pd.DataFrame({
        'url': article_latent_df.index,
        'similarity': similarities
    })

    # Exclude the input URL and sort by similarity in descending order
    similar_urls = similarity_df[similarity_df['url'] != url].sort_values(by='similarity', ascending=False)
    selected_urls = [s['url'] for s in similar_urls.head(n).to_dict(orient='records')]

    # 해당 URL의 정보를 찾아 최종 반환
    article_info_file_path = os.path.join(os.path.dirname(__file__), 'article_infos.pkl')
    with open(article_info_file_path, 'rb') as f:
        article_info_df = pickle.load(f)

    result = []

    for url in selected_urls:
        row = article_info_df.loc[article_info_df['url'] == url].iloc[0]
        result.append(row.to_dict())
    
    return result