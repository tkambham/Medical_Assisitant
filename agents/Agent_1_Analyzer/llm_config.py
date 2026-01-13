from langchain_mistralai import ChatMistralAI

def get_medical_llm(temperature=0.3):
    
    f = open('agents/Agent_1_Analyzer/Mistral-Med_API_KEY.txt', 'r')
    api_key = f.read()
    f.close()
    
    return ChatMistralAI(
        model="mistral-large-latest",  # or "mistral-medium-latest"
        temperature=temperature,
        api_key=api_key,
        max_tokens=2000
    )