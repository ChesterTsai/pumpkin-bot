import datetime
import random

def mora(playerChoice):
    
    botChoice = str(random.randint(1, 3))
    
    choiceName = {'1': "剪刀", '2': "石頭", '3': "布"}
    playerLoseTo = {'1': '2', '2': '3', '3': '1'}
    
    gameMsg = ""
    gameResult = ""
    
    # Quit Scenerio
    if playerChoice not in ['1', '2', '3']:
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家已放棄')
        gameMsg = "已接受遊戲中斷請求"
        gameResult = "Quit"
        return (gameMsg, gameResult)
    
    # Tie Scenerio
    if playerChoice == botChoice:
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家出{choiceName[playerChoice]}, 機器人出{choiceName[botChoice]}, 平手')
        gameMsg = f'玩家出{choiceName[playerChoice]}, 機器人出{choiceName[botChoice]}, 此局平手'
        gameResult = "Tie"
        return (gameMsg, gameResult)
    
    # Check Win or Lose
    
    # Player Lose Scenerio
    if botChoice == playerLoseTo[playerChoice]:
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家出{choiceName[playerChoice]}, 機器人出{choiceName[botChoice]}, 機器人獲勝')
        gameMsg = f'玩家出{choiceName[playerChoice]}, 機器人出{choiceName[botChoice]}, 此局機器人獲勝'
        gameResult = "Lose"
    
    # Player Win Scenerio
    else:
        print(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 玩家出{choiceName[playerChoice]}, 機器人出{choiceName[botChoice]}, 玩家獲勝')
        gameMsg = f'玩家出{choiceName[playerChoice]}, 機器人出{choiceName[botChoice]}, 此局玩家獲勝'
        gameResult = "Win"
    
    return (gameMsg, gameResult)