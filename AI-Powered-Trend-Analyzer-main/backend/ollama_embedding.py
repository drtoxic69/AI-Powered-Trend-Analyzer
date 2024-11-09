from langchain_community.embeddings.ollama import OllamaEmbeddings


def get_embedding():
    ollama = OllamaEmbeddings(model="llama3.2")
    return ollama

if __name__ == "__main__":
    llama = get_embedding()
    print(llama.embed_query("Hello world"))
