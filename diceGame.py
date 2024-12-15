import random
import time
import datetime

def dice(mentionAutor):
    
    min, max = 1, 6
    gameMsg = ""
    gameResult = ""

    playerDiceA = random.randint(min, max)
    botDiceA = random.randint(min, max)
    playerDiceB = random.randint(min, max)
    botDiceB = random.randint(min, max)

    playerDiceSum = playerDiceA + playerDiceB
    botDiceSum = botDiceA + botDiceB

    print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家點數:{playerDiceSum}, 機器人點數:{botDiceSum}')
    
    gameMsg += f'{mentionAutor}, 你骰到{playerDiceA}點和{playerDiceB}點' + "\n"
    gameMsg += f'而我骰到{botDiceA}點和{botDiceB}點' + "\n"

    if playerDiceSum > botDiceSum:
        gameMsg += f'{mentionAutor}, 你贏了! 恭喜'
        gameResult = "playerWin"
    elif playerDiceSum == botDiceSum:
        gameMsg += f'{mentionAutor}, 我們平手囉!'
        gameResult = "tie"
    else:
        gameMsg += f'{mentionAutor}, 你輸了! 接受懲罰吧'
        gameResult = "playerLose"
    
    return (gameMsg, gameResult)