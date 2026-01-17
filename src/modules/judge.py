import json
from .llm_client import LLMClient

class Judge:
    def __init__(self):
        self.llm = LLMClient()

    def evaluate(self, question, answer_non_rag, answer_rag, rag_context):
        system_prompt = """You are an expert LLM-as-a-Judge. Your task is to evaluate two answers to a question:
1. A Non-RAG answer (generated without external context).
2. A RAG answer (generated using retrieved context).

You must evaluate them on:
- Accuracy (1-5)
- Completeness (1-5)
- Relevance (1-5)
- Clarity (1-5)
- Grounding (1-5, only applicable for RAG)

Provide a JSON response with scores, justification, and a final winner.
"""

        user_prompt = f"""
QUESTION: {question}

---
CONTEXT USED FOR RAG:
{rag_context}
---

ANSWER 1 (Non-RAG):
{answer_non_rag}

ANSWER 2 (RAG):
{answer_rag}

---

Evaluate both answers. 
For "Grounding" in Non-RAG, put "N/A" or 0.
Determine a Final Winner based on which answer is objectively better given the question and context.

Output format MUST be valid JSON matching this structure:
{{
  "evaluation": [
    {{
      "model": "Non-RAG",
      "scores": {{
        "accuracy": <int>,
        "completeness": <int>,
        "relevance": <int>,
        "clarity": <int>
      }},
      "average_score": <float>,
      "justification": "<string>"
    }},
    {{
      "model": "RAG",
      "scores": {{
        "accuracy": <int>,
        "completeness": <int>,
        "relevance": <int>,
        "clarity": <int>,
        "grounding": <int>
      }},
      "average_score": <float>,
      "justification": "<string>"
    }}
  ],
  "final_winner": "Non-RAG" or "RAG",
  "reason": "<string>"
}}
"""
        result = self.llm.generate_json_completion(user_prompt, system_prompt)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # Basic fallback if JSON is messy
            return {
                "error": "Failed to parse JSON from judge",
                "raw_output": result
            }
