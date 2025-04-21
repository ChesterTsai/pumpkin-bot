import discord
from discord.ext import commands
import urlScanner

class Scan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def scan(self, ctx, link: str):
        """掃描可疑網址"""
        
        text = "請選擇資訊完整度\n"
        text += "(1:完整資訊/2:不管風險分數，只看是否為危險網站/3:查看是否為釣魚網站、是否有病毒及風險分數)"
        await ctx.send(text)
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        userSelection = await self.bot.wait_for("message", check = check)
        userSelection = userSelection.content
        
        if userSelection != "1" and userSelection != "2" and userSelection != "3":
            await ctx.send(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} ERROR] 錯誤選項')
            return 0
        
        strictness = 0
        
        additional_params = {
            'strictness' : strictness
        }
        
        ipqs = urlScanner.IPQS()
        result = ipqs.malicious_url_scanner_api(link, additional_params)
        
        if 'success' in result and result['success'] == False:
            await ctx.send(f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} ERROR] 不合理的網域')
            return 0
        
        respone = f'[{datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")} INFO] '
        respone += link
        respone += ':\n'
        
        if userSelection == "1":
            for x, y in result.items():
                respone += f'{x}:{y}\n'
            
        if userSelection == "2":
            if result['suspicious'] == True:
                respone += '是可疑網站'
            else:
                respone += '不是可疑網站'
        
        if userSelection == "3":
            if result['phishing'] == True:
                respone += '是釣魚網站\n'
            else:
                respone += '不是釣魚網站\n'
            
            if result['malware'] == True:
                respone += '含有病毒\n'
            else:
                respone += '不含病毒\n'
            
            respone += '風險評分為'
            respone += str(result['risk_score'])
            respone += '分，'
            if result['risk_score'] > 85:
                respone += '超過85分，高風險(0分乾淨，100分高風險)'
            else:
                respone += '未超過85分，低風險(0分乾淨，100分高風險)'
        
        await ctx.send(respone)

async def setup(bot):
    await bot.add_cog(Scan(bot))