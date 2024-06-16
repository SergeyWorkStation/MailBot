from threading import Thread
from bot_app import polling
from mail_app import check_email

mail_thread = Thread(target=check_email)
bot_thread = Thread(target=polling)

bot_thread.start()
mail_thread.start()
