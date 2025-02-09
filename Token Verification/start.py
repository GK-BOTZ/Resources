from PATH import validate_token 
# PATH = actual path of the validate_token function 



#@Client.on_message(filters.command("start") & ~filters.channel)
#async def start(bot, message):
    if hasattr(message, 'command') and len(message.command) == 2: 
       data = message.command[1]
       if data.split("-")[0] == 'verify':
           await validate_token(bot, message, data)
           return
    #Other Codes 

'''
📝 Note :
   1) No Need If Your Are Using GLOBAL TOKEN VERIFICATION 😜.
   2) Add This Code In Your /start Command Handler.
   
Credit @GK-BOTZ
'''
