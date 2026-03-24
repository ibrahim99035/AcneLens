import os
import json
from google import genai
from PIL import Image

class AcneGeminiAnalyzer:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash" 
        
        self.clarino_data = {
            "name": "Clarino",
            "ingredients": "Basil oil, thyme oil, tea tree oil, lavender oil, Jojoba oil, aloe vera & nano-silica"
        }

    def analyze(self, image_path, user_context=None):
        if not os.path.exists(image_path):
            return {"status": "error", "message": "Image not found"}

        try:
            img = Image.open(image_path)
            context_str = json.dumps(user_context) if user_context else "No additional context provided."
            
            prompt = f"""
            Identify the acne type: BLACKHEADS, WHITEHEADS, PAPULES, PUSTULES, CYSTS, or NODULAR.
            Patient Context: {context_str}
            Product: {self.clarino_data['name']} ({self.clarino_data['ingredients']}).
            
            Evaluate suitability based on the photo AND context (e.g., if patient is pregnant or has specific allergies).
            
            Format your response exactly like this:
            DIAGNOSIS: [Type]
            REASONING: [Visual evidence + context clues]
            SUITABILITY: [Yes/No/Partial]
            EXPLANATION: [Clinical advice]
            """

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[prompt, img]
            )
            
            res_text = response.text
            lines = [l.strip() for l in res_text.split('\n') if ":" in l]
            data = {l.split(':', 1)[0].strip(): l.split(':', 1)[1].strip() for l in lines}

            return {
                "status": "success",
                "diagnosis": data.get("DIAGNOSIS", "Unknown"),
                "reasoning": data.get("REASONING", "N/A"),
                "suitability": data.get("SUITABILITY", "N/A"),
                "explanation": data.get("EXPLANATION", res_text[:200])
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}