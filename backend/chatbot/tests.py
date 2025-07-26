import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_nepal_specific_questions():
    """Test with Nepal-specific questions that should be in your documents"""
    
    questions = [
        # English questions about Nepal
        ("What is the legal framework for elections in Nepal?", "en"),
        ("What are the citizenship laws in Nepal?", "en"),
        ("What does the Constitution say about federal structure?", "en"),
        
        # Nepali questions
        ("नेपालको संविधानमा नागरिकताको बारेमा के भनिएको छ?", "ne"),
        ("संघीय संरचनाको बारेमा के उल्लेख छ?", "ne"),
        ("चुनावको कानूनी ढाँचा के हो?", "ne"),
    ]
    
    print("🧪 TESTING NEPAL-SPECIFIC QUESTIONS")
    print("=" * 60)
    
    for question, language in questions:
        print(f"\n🤔 Question ({language.upper()}): {question}")
        print("⏳ Processing...")
        
        try:
            response = requests.post(f"{BASE_URL}/chat/", json={
                "question": question,
                "language": language
            })
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', 'No answer')
                print(f"✅ Answer: {answer}")
                print(f"📚 Similar Documents: {len(result.get('similar_documents', []))}")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_nepal_specific_questions()