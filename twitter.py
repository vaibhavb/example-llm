#!python3
import sys, os, random
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI


llm = OpenAI(temperature=0.6)

def get_random_file(dir_path="./data/twitter/"):
    """
    Returns a random file from a directory and its subdirectories.
    """
    files = []
    for dirpath, _, filenames in os.walk(dir_path):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    random_file = random.choice(files)
    print(f"FILE: {random_file}")
    return random_file


def get_file_data(file_name, chunk_size=5000):
    """get the file text in a specificed chunk"""
    file_data = ""
    with open(file_name, 'r') as file:
        file_data = file.read(chunk_size)
    return file_data

file_name = get_random_file()
question = sys.argv[1]
file_data = get_file_data(file_name)

prompt = PromptTemplate(
    input_variables=["question", "file_data"],
    template="You are a algorithm analyst trying to find issues related to fairness in twitter's algorithm. Your name is Dana. Don't use more than 2 points. Critique the following file. {question} {file_data}",
)

print(llm(prompt.format(question=question,file_data=file_data)))