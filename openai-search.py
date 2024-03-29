## Declarations
import platform

f = 42 * "="
user_os = platform.system()


## Installing requirements
import subprocess

requirements = [
    'pypdf',
    'openai'#,
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
import openai

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
                

    def read_string(self, content: list, word: str) -> list: # margin: int
        instances = []
        i = 0
        for doc in Reader.docs:
            instances.extend([doc, []]) # NOT APPEND!
            #print(instances)
            n_lines = len(content[i][1])
            for x in range(n_lines):
                if word in content[i][1][x][1]:
                    #instances[i][1].append([content[i][1][x][0], content[i][1][x][1]])
                    instances[1].append(content[i][1][x])
            i+=1
            
        return instances#[0]

    @timeit
    def subject_finder_main(self, word: str, instances: list) -> list:
        evaluate = EvalAI()
        final = [instances[0], []]
        if len(instances[1]) > 0:
            for line in instances[1]:
                c_line = line[1]
                subject = evaluate.check_subject(word, c_line)
                relevants = evaluate.near_subject(subject, word)
                if evaluate.is_worth_keeping(word, c_line, relevants):
                    final[1].append(line)
        return final



class EvalAI:
    # Read openAI key from "key.txt" which should only contain the key and no other form of text
    with open('key.txt', 'r') as f:
        openai.api_key = f.read().splitlines()[0]

    def __init__(self):
        self.role = "user"


    def api_request(self, content: str) -> str:
        out = ""
    
        r = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":f"{self.role}", "content":f"{content}"}
                    ]
                )
        
        for choice in r.choices:
            out += choice.message.content
            
        return out

    
    def check_subject(self, word: str, line: str) -> str:
        general_subject = str(self.api_request(f"Quel est le sujet general du mot '{word}' dans le texte '{line}'? Reponds en un seul mot si possible ou dans le pire de cas dans une phrase tres courte"))

        return general_subject

    
    def near_subject(self, general_subject: str, word: str) -> list:
        relevants = list(str(self.api_request(f"Ecris moi une liste en python avec des mots qui s'approchent du sujet de '{general_subject}' et du mot '{word}' et reponds seulement avec la liste et PAS D'AUTRE TEXTE. AUCUN AUTRE TEXTE.")))

        return relevants

    
    def is_worth_keeping(self, word: str, line: str, sub_relevants: str) -> bool:
        #if check_subject(word,  #A FINIR
        subject_check = bool(int(self.api_request(f"Est-ce que le mot '{word}' dans la phrase '{line}' correspond au sujet general des mots dans la liste '{sub_relevants}'? Si oui, reponds seulement avec '1', sinon, reponds avec seulement '0' et RIEN d'autre.")))
        
        return subject_check


def main(word):
    content = r.read_for_n()
    instances = r.read_string(content, word)
    final = r.subject_finder_main(word, instances)
    ret = "\n".join(f" {count+1} - Line {value[0]}: '{value[1]}'" for count, value in enumerate(final[1]))
    return f'{f}\n• Document: {final[0]}\n-> Occurence(s):\n{ret}\n{f}'


if __name__ == "__main__":
    print(f"{f}\n/!\ Checking requirements...")
    install_req(requirements)
    r = Reader()
    word = input(f"{f}\nWhat's the word you're looking for?\n-> ")
    print(main(word))
