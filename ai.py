# ai.py

import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
import threading

# Load environment variables from .env file
load_dotenv()

endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

def generate_responses(situation, global_players, current_gdp, user_tweet, callback=None):
    """
    Generates AI responses based on the situation, global players, current GDP, and user's tweet.
    
    Parameters:
        situation (str): Description of the current situation.
        global_players (list): List of global player countries.
        current_gdp (int): Current GDP value.
        user_tweet (str): The tweet sent by the user.
        callback (function): Optional callback to handle the response asynchronously.
    
    Returns:
        dict: AI responses including player tweets, GDP impact, and relationships.
    """
    text_prompt = (
        f"Situation: {situation}\n"
        f"Global Players: {', '.join(global_players)}\n"
        f"Current GDP: ${current_gdp:,}\n"
        f"User's Tweet: \"{user_tweet}\"\n\n"
        f"Please provide the following based on the above context in JSON format:\n"
        f"1. Responses from each global player. Each response should be humorous, profound, political, and comedically hateful or negative (fictional).\n"
        f"2. GDP Impact: Specify 'increase' or 'decrease' and the amount in trillions.\n"
        f"3. Relationships: For each global player, specify the relationship status as 'Good', 'Neutral', or 'Hostile'.\n\n"
        f"Structure your response as follows:\n"
        f"{{\n"
        f"  \"responses\": {{\n"
        f"    \"China\": \"Ah, the moon lottery! Time to put our giant panda teams to work. 🐼🌕 #MoonBound\",\n"
        f"    \"India\": \"May the odds be ever in your favor! Sending prayers from Bollywood to the lunar stage. 🎬🌙 #MoonLottery\",\n"
        f"    \"Russia\": \"Another slice of the moon? Perfect! Just what we needed for our space vodka distilleries. 🚀🥃 #LunarBounty\"\n"
        f"  }},\n"
        f"  \"gdp_impact\": {{\n"
        f"    \"direction\": \"increase\",\n"
        f"    \"amount_trillion\": 0.5\n"
        f"  }},\n"
        f"  \"relationships\": {{\n"
        f"    \"China\": \"Good\",\n"
        f"    \"India\": \"Neutral\",\n"
        f"    \"Russia\": \"Hostile\"\n"
        f"  }}\n"
        f"}}"
    )

    def fetch_response():
        try:
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": text_prompt},
                ],
            )
            result = response.choices[0].message.content
            print("Raw AI Response:")
            print(result)  # Debug: Print the raw response
            # Attempt to parse the JSON response
            try:
                ai_data = json.loads(result)
                if callback:
                    callback(ai_data)
            except json.JSONDecodeError:
                print("Failed to parse AI response as JSON.")
                if callback:
                    callback(None)
        except Exception as e:
            print(f"Error generating AI response: {e}")
            if callback:
                callback(None)

    # Run the AI call in a separate thread to prevent blocking
    threading.Thread(target=fetch_response, daemon=True).start()

# Testing the AI API when running ai.py directly
if __name__ == "__main__":
    # Testing GPT API
    text_prompt = "what gpt model are you"
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text_prompt},
            ],
        )
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error during AI testing: {e}")
