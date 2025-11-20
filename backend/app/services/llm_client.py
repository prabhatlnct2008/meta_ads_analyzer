import os
from openai import OpenAI
from typing import Dict, Optional

class LLMClient:
    """Client for interacting with OpenAI GPT-4"""

    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')

    def ask(self, system_prompt: str, user_prompt: str, data: Optional[Dict] = None) -> str:
        """Ask LLM a question with optional data context"""
        try:
            messages = [
                {"role": "system", "content": system_prompt}
            ]

            # Add data context if provided
            if data:
                context_message = f"Here is the relevant data:\n\n```json\n{self._format_data(data)}\n```\n\n{user_prompt}"
                messages.append({"role": "user", "content": context_message})
            else:
                messages.append({"role": "user", "content": user_prompt})

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )

            answer = response.choices[0].message.content
            return answer

        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise

    def _format_data(self, data: Dict) -> str:
        """Format data dictionary as readable JSON string"""
        import json
        return json.dumps(data, indent=2)

    def analyze_performance(self, overview: Dict, campaigns: list, question: str) -> str:
        """Analyze Meta ads performance and answer user question"""
        system_prompt = """You are an expert Meta/Facebook Ads performance analyst.
Your role is to analyze advertising data and provide clear, actionable insights.

When analyzing data:
- Focus on the most important metrics: spend, ROAS, CPA, CTR, conversions
- Identify top performers and underperformers
- Explain trends and patterns in simple terms
- Provide specific, actionable recommendations
- Be concise but thorough
- Use plain English, avoid jargon when possible

When you see wasteful spending or poor performance, point it out clearly.
When you see opportunities, highlight them."""

        # Prepare data context
        data_context = {
            "account_overview": overview,
            "campaigns": campaigns[:10]  # Limit to top 10 campaigns to save tokens
        }

        return self.ask(system_prompt, question, data_context)
