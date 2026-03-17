from fastapi import FastAPI
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

app = FastAPI(title="CineMatch Pro API")

# 1. Load the AI Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. LOAD DATASET (Updated to match your specific CSV columns)
try:
    df = pd.read_csv("movies.csv")
    df = df.rename(columns={'Title': 'title', 'Movie Info': 'description'})
    
    # Remove any rows that have empty descriptions
    df = df.dropna(subset=['description'])
    
    print(f"Successfully loaded {len(df)} movies from movies.csv")
except Exception as e:
    print(f"Error loading CSV: {e}. Using fallback data.")
    data = {
        "title": ["Inception"],
        "description": ["A thief who steals secrets through dreams."]
    }
    df = pd.DataFrame(data)

# 3. Pre-calculate Embeddings
print("Encoding movie descriptions... Please wait.")
movie_embeddings = model.encode(df['description'].tolist(), convert_to_tensor=True)

@app.get("/")
def home():
    return {"message": "Welcome to CineMatch Pro Semantic Search!"}

@app.get("/search")
def search_movies(query: str, top_k: int = 3):
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, movie_embeddings)[0]
    
    top_results = torch.topk(cos_scores, k=min(top_k, len(df)))
    
    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        results.append({
            "title": df.iloc[idx.item()]['title'],
            "description": df.iloc[idx.item()]['description'],
            "score": round(float(score), 4)
        })
    
    return {"query": query, "results": results}