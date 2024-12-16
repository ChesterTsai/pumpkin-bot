import random
import time
import datetime
import json

# default goes with the easy one
min, max = 1, 100   # 猜數字的範圍
chances = 5         # 擁有的機會
timeoutTime = 4.0   # 多久後會觸發過久提示
giveHint = 5        # 與正確數差距多少時給予提示

# 簡單模式
def easy():
    global min, max, chances, timeoutTime
    min, max = 1, 100
    chances = 5
    timeoutTime = 4.0
    giveHint = 5

# 一般模式
def normal():
    global min, max, chances, timeoutTime
    min, max = 1, 200
    chances = 4
    timeoutTime = 5.0
    giveHint = 10

# 困難模式
def hard():
    global min, max, chances, timeoutTime
    min, max = 1, 1000
    chances = 25
    timeoutTime = 10.0
    giveHint = 50

def guessGameAnswer():
    
    with open("variables.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        f.close()
    for guessGameVariables in data:
        old_ans = data[guessGameVariables]["old_ans"]
    
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
        
        data[str(guessGameVariables)]["old_ans"] = old_ans
        with open("variables.json", "w", encoding='utf-8') as f:
            json.dump(data, f)
    
    return ans