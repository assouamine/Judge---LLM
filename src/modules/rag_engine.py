import os
import glob

class RAGEngine:
    def __init__(self, docs_path="data/documents"):
        self.docs_path = docs_path
        self.documents = []
        self.load_documents()

    def load_documents(self):
        """Loads text files from the documents directory."""
        self.documents = []
        if not os.path.exists(self.docs_path):
            os.makedirs(self.docs_path)
            # Create a sample document if empty
            with open(os.path.join(self.docs_path, "sample_ai_knowledge.txt"), "w", encoding="utf-8") as f:
                f.write("RAG (Retrieval-Augmented Generation) is a technique that enhances LLM accuracy by retrieving external data. Non-RAG models rely solely on training data.")
        
        files = glob.glob(os.path.join(self.docs_path, "*.txt"))
        for file in files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.documents.append({"source": os.path.basename(file), "content": content})
            except Exception as e:
                print(f"Error reading {file}: {e}")

    def retrieve(self, query, k=2):
        """
        Simple keyword-based retrieval for demonstration.
        In a production env, use VectorDB (Chroma/FAISS).
        """
        # Simple scoring based on word overlap
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.documents:
            score = 0
            content_lower = doc['content'].lower()
            for word in query_words:
                if word in content_lower:
                    score += 1
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        # Return top k
        return [item[1] for item in scored_docs[:k]]

    def format_context(self, retrieved_docs):
        context = ""
        for i, doc in enumerate(retrieved_docs):
            context += f"Document {i+1} ({doc['source']}):\n{doc['content']}\n\n"
        return context
