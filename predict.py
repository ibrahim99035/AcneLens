import sys
import json
from inference import AcneGeminiAnalyzer

GEMINI_KEY = "AIzaSyAIQEs3_bPQ_lcUX9Yv1xwvEwhN3ygokAU" 

def main():
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_name>")
        return

    image_path = sys.argv[1]
    
    # Optional: Mocking survey answers for CLI testing
    test_answers = {
        "age": "21-30",
        "painful": "Yes",
        "longDuration": "Yes"
    }

    analyzer = AcneGeminiAnalyzer(GEMINI_KEY)
    
    print(f"🧬 Gemini 3.1 AI is analyzing {image_path} with patient context...")
    res = analyzer.analyze(image_path, user_context=test_answers)

    if res["status"] == "success":
        print("\n" + "="*60)
        print(f"🩺 DIAGNOSIS : {res['diagnosis']}")
        print(f"🧠 REASONING : {res['reasoning']}")
        print("-" * 60)
        print(f"✅ SUITABLE? : {res['suitability']}")
        print(f"🧪 NOTE      : {res['explanation']}")
        print("="*60 + "\n")
    else:
        print(f"❌ {res['message']}")

if __name__ == "__main__":
    main()