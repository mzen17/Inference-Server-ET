from sentence_transformers import SentenceTransformer

def getEmbeddings(input: str):
    print("Getting Embeddings")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(input).tolist()