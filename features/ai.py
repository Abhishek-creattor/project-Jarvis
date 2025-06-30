import openai

openai.api_key = "sk-svcacct-A-srkIoPvIdWDjYFZ3I8LwOZV-bwN4sp8lHqrVZwwgzT3BlbkFJUkEuN0I1EsmDG8JaIfdQ-c2IUPOjnMkzvz27YDbrAAA"

def ask_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "Sorry, I couldn't get a response from AI."