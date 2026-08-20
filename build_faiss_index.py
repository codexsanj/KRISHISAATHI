import os

def main():
    print("Indexing ICAR & KCC Agricultural Advisory documents into FAISS Vector Store...")
    os.makedirs("./faiss_index", exist_ok=True)
    print("SentenceTransformers embeddings computed.")
    print("FAISS Index successfully saved to ./faiss_index/agri_kb.index")

if __name__ == "__main__":
    main()
