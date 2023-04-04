from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)
text = "You are a venture capitalist and want to invest 10 million dollars in five companies, what would those be?"
print(llm(text))