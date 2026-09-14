import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
import os
import requests
from pathlib import Path


load_dotenv(Path(__file__).parent / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API = os.getenv("OPENWEATHER_API_KEY")

# Define tools
def get_weather(city: str):
    """Get weather for a given city"""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


def get_location():
    """Get users current location. Use this when user asks about
    weather without specifying the city"""
    response = requests.get("https://ipapi.co/json/",
                            headers={'User-agent': 'your-bot 0.1'})
    data = response.json()
    city = data['city']
    country = data.get('country_name')
    return f"{city}, {country}"


# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.7,
    api_key=API_KEY,
)

# Create system prompt
system_prompt = """
You are a helpful weather assistant.

YOUR WORKFLOW:
1. If the user asks about weather without specialising a location, you MUST:
    - first call get_location to find there location
    - then call get)weather(city) with that location
    
2. If the user provides a city, call get_weather(city) directly.
"""

# Create Agent
agent = create_agent(
    model=llm,
    tools=[
        get_weather,
        get_location,
    ],
    system_prompt=system_prompt,
)

user_query = input("Enter your query: ")

response1 = agent.invoke(
    {"messages": [{
        "role": "user",
        "content": user_query}]}
)

print(response1["messages"][-1].text)
