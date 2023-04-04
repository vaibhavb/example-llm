import os
import sys
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")
prompt = sys.argv[1]

print(prompt)
response = openai.Completion.create(
  model="code-davinci-002",
  prompt=f"\"\"\"\n {prompt}\"\"\"",
  temperature=0,
  max_tokens=300,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response["choices"][0].text)