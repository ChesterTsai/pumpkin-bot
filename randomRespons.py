import random

responses = ""
responMsg = ""

def _8ball(question):
    responses = ['這是當然的',
                 '絕對是的阿',
                 '不用想了，一定是',
                 '是的，完全就是',
                 '痾...也許吧',
                 '或許你得再問一次',
                 '現在無法預測',
                 '等等再問一次，我就會告訴你答案了',
                 '不',
                 '完全不可能',
                 '我的回答是「不」',
                 '看起來非常不好']
    
    responMsg = f'你問的問題是: {question}\n我的回答是: {random.choice(responses)}'
    return responMsg

def Hi():
    responses = ['安安你好',
                 '我最近感覺好讚，你呢',
                 '幹你娘閉嘴',
                 '安安阿～',
                 '嗨～',
                 '哈囉，這裡是隻再正常不過的機器人',
                 '哈囉你好嗎，衷心感謝，珍重再見',
                 '嗨，初次見面，你好']
    
    responMsg = f'{random.choice(responses)}'
    return responMsg

def choice(choices):
    responses = choices.split(',')
    
    responMsg = f'{random.choice(new_choic)} 是最棒的答案'
    return responMsg