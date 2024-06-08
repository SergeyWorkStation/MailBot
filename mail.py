from imap_tools import MailBox, A


def mail_fetch(email, password, from_email):
    if email.split('@')[1] in ('mail.ru', 'internet.ru', 'list.ru', 'bk.ru', 'inbox.ru', 'mail.ua', 'xmail.ru'):
        server = 'imap.mail.ru'
    elif email.split('@')[1] in ('yandex.ru', 'yandex.ua', 'narod.ru', 'ya.ru', 'yandex.com'):
        server = 'imap.yandex.ru'
    else:
        return
    with MailBox(server).login(username=email, password=password) as mailbox:
        for msg in mailbox.fetch(criteria=A('NEW', f'FROM "{from_email}"'), reverse=True):
            return {'date': msg.date,
                    'subject': msg.subject,
                    'html': msg.html,
                    'uid': msg.uid,
                    'attachments': msg.attachments}
