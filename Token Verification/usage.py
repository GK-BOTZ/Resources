from PATH import is_user_verified, send_verification
# PATH = actual path of the functions 


#async def main_function(bot, message):
    if not await is_user_verified(message.from_user.id):
        await send_verification(bot, message)
        return



'''
📝 Note :
   1) No Need If Your Are Using GLOBAL TOKEN VERIFICATION 😜.
   2) Add This Code Anywhere You Wants The User To Verify.

Credit @GK-BOTZ
'''
