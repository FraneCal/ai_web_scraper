from openai import OpenAI, RateLimitError, api_key

client = OpenAI(
    api_key="YOUR API KEY",
    base_url="https://openrouter.ai/api/v1",
)

def chat_with_deepseek(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-prover-v2:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except RateLimitError:
        print("Rate limit exceeded. Please wait before making more requests.")
        return None

if __name__ == "__main__":
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_deepseek(user_input)
        print(f"Chatbot: {response}")
