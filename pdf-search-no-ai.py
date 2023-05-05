## Declarations
import platform

f = 42 * "="
user_os = platform.system()


## Installing requirements
import subprocess

requirements = [
    'pypdf'#,
    #'asyncio'
]

def install_req(req: list) -> None:
    if user_os == "Darwin":
        pip = "pip3"
    elif user_os == "Linux" or user_os == "Windows":
        pip = "pip"
        
    for requirement in requirements:
        try:
            subprocess.check_call([pip, "install", requirement])
        except subprocess.CalledProcessError as e:
            print(e)
            continue
    return


## Helper function(s)
from functools import wraps
import time

def timeit(func) -> None:
    @wraps(func)
    def timeit_wrapper(*args, **kwargs) -> func:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'{f}\n/!\ Debug:\n-> Function "{func.__name__}" defined at line {func.__code__.co_firstlineno + 1} took {total_time:.4f} seconds to execute')
        return result
    
    return timeit_wrapper


## Main 2
import pypdf as pdf

'''
Complexity in terms of OpenAI requests: O(n*3) - where n: number of instances found
- BEST CASE: 0 requests (0 instance)
- SECOND BEST CASE: 3 requests (1 instance)
'''

class Reader:
    docs = []
    def __init__(self):
        # Input
        self.r = int(input(f"{f}\nHow many docs to read?\n-> "))
        for i in range(self.r):
            while True:
                inp = input(f"{f}\nFile {i+1} location:\n-> ").lower()
                if ".pdf" in inp:
                    Reader.docs.append(inp)
                    break
                print(f"{f}\nForgetting something? Hint: file extension")
        
        
    def read_for_n(self) -> list:
        lines = []
        i = 0
        for doc in Reader.docs:
            n = 1
            ## Format list
            lines.append([doc, []])
            opnd = pdf.PdfReader(doc)
            for page in opnd.pages:
                text = page.extract_text().splitlines()
                for line in text:
                    # format: [["doc.pdf", [["Line 1", "text"], ["Line 2", "text"], ...]], ...]
                    lines[i][1].append([n, line.lower()]) # [f"Line {n}, ...]
                    n += 1
            i += 1
        return lines
                
    @timeit
    def read_string(self, content: list, word: str) -> list: # margin: int
        instances = []
        i = 0
        for doc in Reader.docs:
            instances.append([doc, []])
            n_lines = len(content[i][1])
            for x in range(n_lines):
                if word in content[i][1][x][1]:
                    #instances[i][1].append([content[i][1][x][0], content[i][1][x][1]])
                    instances[i][1].append(content[i][1][x])
            i+=1

        #print(instances)
        return instances#[0]


def main(word):
    content = r.read_for_n()
    instances = r.read_string(content, word)
    for i in range(len(Reader.docs)):
        ## FASTER ASF but needs fixing
        #ret = "\n".join(f" {count+1} - Line {value[0]}: '{value[1]}'" for count, value in enumerate(instances[i][1]))
        #print(f'{f}\n• Document: {instances[i][0]}\n-> Occurence(s):\n{ret}')

        ## SLOW AF
        print(f'{f}\n• Document: {instances[i][0]}\n-> Occurence(s):')
        for n in range(len(instances[i][1])):
            print(f" {n+1} - Line {instances[i][1][n][0]}: '{instances[i][1][n][1]}'")
    print(f)
    #return instances


if __name__ == "__main__":
    print(f"{f}\n/!\ Checking requirements...")
    install_req(requirements)
    r = Reader()
    word = input(f"{f}\nWhat's the word you're looking for?\n-> ")
    main(word)
