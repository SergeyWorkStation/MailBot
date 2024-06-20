import fetch_tables
import mail
import bot_app


def check_email():
    while True:
        try:
            for msg in fetch_tables.get_data_massage():
                if int(msg[4]) == 3:
                    mail_text = mail.MailText(msg[1], msg[2], msg[3])
                    text = mail_text.get_response()
                    if text:
                        bot_app.bot.send_message(chat_id=msg[0], text=text)
                if int(msg[4]) == 2:
                    mail_files = mail.MailFile(msg[1], msg[2], msg[3])
                    files = mail_files.get_response()
                    if files:
                        for file_name, file in files:
                            bot_app.bot.send_document(chat_id=msg[0], document=file, caption=file_name)
        except Exception as e:
            print(e)
