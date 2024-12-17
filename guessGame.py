import random
import time
import datetime
import json

with open("variables.json", "r", encoding='utf-8') as f:
    data = json.load(f)
    f.close()

# 簡單模式
def easy():
    min, max = data["easy"]["min"], data["easy"]["max"]
    chances = data["easy"]["chances"]
    timeGiven = data["easy"]["timeGiven"]
    giveHint = data["easy"]["giveHint"]
    
    return (min, max, chances, timeGiven, giveHint)

# 一般模式
def normal():
    min, max = data["normal"]["min"], data["normal"]["max"]
    chances = data["normal"]["chances"]
    timeGiven = data["normal"]["timeGiven"]
    giveHint = data["normal"]["giveHint"]
    
    return (min, max, chances, timeGiven, giveHint)

# 困難模式
def hard():
    min, max = data["hard"]["min"], data["hard"]["max"]
    chances = data["hard"]["chances"]
    timeGiven = data["hard"]["timeGiven"]
    giveHint = data["hard"]["giveHint"]
    
    return (min, max, chances, timeGiven, giveHint)

def guessGameAnswer(min, max):
    
    old_ans = data["old_ans"]

    ans = random.randint(min, max)
    RandomTimes = 0
    
    while ans == old_ans:
        ans = random.randint(min, max)
        RandomTimes += 1
    
    if RandomTimes == 0:
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 答案:{ans}')
    else:
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 答案:{ans} (重骰{RandomTimes}次)')
    
    old_ans = ans
    
    data["old_ans"] = old_ans
    with open("variables.json", "w", encoding='utf-8') as f:
        json.dump(data, f)
        f.close()
    
    return ans