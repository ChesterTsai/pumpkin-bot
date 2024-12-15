import datetime

def shutdown(reason):
    outputMessage = ''
    if reason == '':
        outputMessage = f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 睡了！晚安'
    else:
        outputMessage = f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] 基於原因:[{reason}]，所以我要睡了！晚安'
    
    return outputMessage