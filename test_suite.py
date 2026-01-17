"""
Test script to demonstrate the LLM-as-a-Judge system with multiple questions.
This shows how the system handles different types of queries.
"""

import json
from src.modules.llm_client import LLMClient
from src.modules.rag_engine import RAGEngine
from src.modules.judge import Judge

def test_question(question, llm, rag, judge):
    print(f"\n{'='*80}")
    print(f"QUESTION: {question}")
    print('='*80)
    
    # Generate Non-RAG answer
    print("\n[1] Generating Non-RAG answer...")
    prompt_non_rag = f"Question: {question}\nAnswer the question concisely."
    answer_non_rag = llm.generate_completion(prompt_non_rag)
    print(f"Non-RAG: {answer_non_rag[:150]}...")
    
    # Generate RAG answer
    print("\n[2] Generating RAG answer...")
    docs = rag.retrieve(question)
    context = rag.format_context(docs)
    prompt_rag = f"Context:\n{context}\n\nQuestion: {question}\nUsing the context above, answer the question."
    answer_rag = llm.generate_completion(prompt_rag)
    print(f"RAG: {answer_rag[:150]}...")
    print(f"Documents used: {len(docs)}")
    
    # Evaluate
    print("\n[3] Evaluating...")
    result = judge.evaluate(question, answer_non_rag, answer_rag, context)
    
    if "error" in result:
        print(f"Error: {result}")
        return
    
    # Display results
    print("\n[4] Results:")
    for item in result.get("evaluation", []):
        print(f"\n{item['model']}:")
        print(f"  Scores: {item['scores']}")
        print(f"  Average: {item['average_score']}")
        print(f"  Justification: {item['justification'][:100]}...")
    
    print(f"\n🏆 WINNER: {result.get('final_winner')}")
    print(f"Reason: {result.get('reason')[:150]}...")

def main():
    print("="*80)
    print("LLM-as-a-Judge Test Suite")
    print("="*80)
    
    # Initialize
    print("\nInitializing system...")
    llm = LLMClient()
    rag = RAGEngine()
    judge = Judge()
    
    # Test questions
    questions = [
        "What is Retrieval-Augmented Generation?",
        "What is the capital of France?",
        "How does LLM-as-a-Judge work?",
    ]
    
    for question in questions:
        try:
            test_question(question, llm, rag, judge)
        except Exception as e:
            print(f"\nError testing question: {e}")
    
    print("\n" + "="*80)
    print("Test suite complete!")
    print("="*80)

if __name__ == "__main__":
    main()
