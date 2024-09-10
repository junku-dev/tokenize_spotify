import os, secrets, time, ast

keys:list = []

def generate_keys() -> list:
    for i in range(17):
        keys.append(os.urandom(15).hex())
    return keys
        

def random_key() -> str:
    return secrets.choice(keys)


def check_index(list:list, index:int)->bool:
    try:
        list[index]
    except IndexError:
        return False
    return True

def write_to_txt(data:dict):
    with open('util/out.txt', 'w', encoding="utf-8") as f:
        for i,j in data.items():
            print(i,j)
            f.writelines(i+"?"+str(j))

def read_file():
    info:dict = {}
    path:str = "util/out.txt"
    with open(path, encoding='utf-8') as f:
        for l in f:
            id = l.split("?")[0]
            tokens = ast.literal_eval(l.split("?")[1])
            print(id,':',tokens)
            file:dict = {str(id) : tokens}
            info.update(file)
    return info

if __name__ == "__main__":
    start = time.time()
    print(generate_keys())
    end = time.time()
    print("seconds: " ,(end - start) * 60)
    write_to_txt(data=data)
    print(read_file())