from PATH import is_user_verified, send_verification
# PATH = actual path of the functions 


'''@Client.on_message(filters.command("anything") & ~filters.channel)
async def start(bot, message):'''
    if not await is_user_verified(message.from_user.id):
        await send_verification(bot, message)
        return



'''
Add This Code Anywhere You Wants The User To Verify.
Credit @GK-BOTZ
'''
