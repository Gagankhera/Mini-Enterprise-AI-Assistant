from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
def analyze_logs(log_text):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
    Analyze the following security logs.

    Logs:
    {log_text}

    Provide:
    1. Summary
    2. Severity (LOW, MEDIUM, HIGH)
    3. Recommendations
    """

    response = llm.invoke(prompt)

    return {
        "summary": response.content,
        "severity": "HIGH",
        "recommendations": ["Review access logs", "Enable MFA"]
    }