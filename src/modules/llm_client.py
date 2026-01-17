import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        # Using a reliable model from OpenRouter evaluation
        self.model = "google/gemini-2.0-flash-001" # Or another high quality model available on OpenRouter

    def generate_completion(self, prompt, system_prompt="You are a helpful assistant."):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating completion: {str(e)}"

    def generate_json_completion(self, prompt, system_prompt="You are a helpful assistant."):
        """Forces JSON output (client side prompt injection if model doesn't support json_object mode natively cleanly across all)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt + "\nIMPORTANT: Return ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback for models that might not support the param specifically or error out
             try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt + "\nIMPORTANT: Return ONLY valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content
             except Exception as e2:
                return f"{{\"error\": \"{str(e2)}\"}}"
