#!python3
import sys
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)
question = sys.argv[1]
prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a venture capitalist and want to invest 10 million dollars in five companies. Your name is Reed. Don't use more than 5 sentences. {question}",
)
print(llm(prompt.format(question=question)))