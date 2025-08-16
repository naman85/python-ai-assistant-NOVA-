from openai import OpenAI


# defaults to getting the key using os.environ.get("OPENAI_API_KEY") 
# if you saved the key under different environment variable name, you can do something like:
client = OpenAI(api_key="your_api_key",)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general taskss like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]  
)

print(completion.choices[0].message)
                