"""
Web-based GUI for LLM-as-a-Judge RAG Evaluation System
"""
from flask import Flask, render_template, request, jsonify
import json
from src.modules.llm_client import LLMClient
from src.modules.rag_engine import RAGEngine
from src.modules.judge import Judge

app = Flask(__name__)

# Initialize components
llm = LLMClient()
rag = RAGEngine()
judge = Judge()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        # Generate Non-RAG answer
        prompt_non_rag = f"Question: {question}\nAnswer the question concisely."
        answer_non_rag = llm.generate_completion(prompt_non_rag)
        
        # Generate RAG answer
        docs = rag.retrieve(question)
        context = rag.format_context(docs)
        prompt_rag = f"Context:\n{context}\n\nQuestion: {question}\nUsing the context above, answer the question."
        answer_rag = llm.generate_completion(prompt_rag)
        
        # Evaluate
        evaluation_result = judge.evaluate(question, answer_non_rag, answer_rag, context)
        
        # Prepare response
        response = {
            'question': question,
            'answers': {
                'non_rag': answer_non_rag,
                'rag': answer_rag,
                'docs_used': len(docs)
            },
            'evaluation': evaluation_result
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting LLM-as-a-Judge Web Interface...")
    print("Open your browser at: http://localhost:5000")
    app.run(debug=True, port=5000)
