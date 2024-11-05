import pickle

# pickle 파일에서 dataframe읽기
with open('article_infos.pkl', 'rb') as f:
    df = pickle.load(f)
print(df.describe())