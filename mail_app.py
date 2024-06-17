import fetch_tables
import mail
import bot_app


def check_email():
    while True:
        try:
            for msg in fetch_tables.get_data_massage():
                result = mail.MailFilter(msg[1], msg[2], msg[3])
                result = result.get_response(int(msg[4]))
                if result:
                    bot_app.bot.send_message(chat_id=msg[0], text=result)
        except Exception as e:
            print(e)
