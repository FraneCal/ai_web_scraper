from openai import OpenAI, RateLimitError
from langchain_core.prompts import ChatPromptTemplate

# Set up OpenRouter DeepSeek client
client = OpenAI(
    api_key="YOUR API KEY",
    base_url="https://openrouter.ai/api/v1",
)

# Prompt template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}.\n"
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response.\n"
    "3. **Empty Response:** If no information matches the description, return an empty string ('').\n"
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_deepseek(dom_chunks, parse_description, chat_history=None):
    prompt_template = ChatPromptTemplate.from_template(template)
    parsed_results = []

    if chat_history is None:
        chat_history = []

    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = prompt_template.format(dom_content=chunk, parse_description=parse_description)

        # Include chat history and current user input
        messages = chat_history + [{"role": "user", "content": prompt}]

        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-prover-v2:free",
                messages=messages
            )
            content = response.choices[0].message.content.strip()
            print(f"Parsed batch {i}/{len(dom_chunks)}")

            # Add assistant reply to history
            chat_history.append({"role": "user", "content": prompt})
            chat_history.append({"role": "assistant", "content": content})

            parsed_results.append(content)
        except RateLimitError:
            print(f"Rate limit hit during batch {i}. Skipping...")
            parsed_results.append("")

    return "\n".join(parsed_results), chat_history
