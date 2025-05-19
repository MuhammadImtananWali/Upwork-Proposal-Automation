from langchain_google_genai import ChatGoogleGenerativeAI
import os

class LLMManager:
    def __init__(self, model_type="gemini-2.0-flash"):
        self.model_type = model_type
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        if self.model_type == "gemini-2.0-flash":
            return ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                temperature=0.3,
            )
        elif self.model_type == "gemini-1.5-pro":
            return ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0.3,
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def generate_text(self, prompt, max_tokens=1000):
        try:
            # Use invoke method for ChatGoogleGenerativeAI
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error generating text: {e}")
            return None