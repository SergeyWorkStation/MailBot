from imap_tools import MailBox, A
from bs4 import BeautifulSoup


class MailFilter:
    def __init__(self, email, password, from_email=None):
        self.email = email
        self.password = password
        self.from_email = from_email
        if email.split('@')[1] in ('mail.ru', 'internet.ru', 'list.ru', 'bk.ru', 'inbox.ru', 'mail.ua', 'xmail.ru'):
            self.server = 'imap.mail.ru'
        elif email.split('@')[1] in ('yandex.ru', 'yandex.ua', 'narod.ru', 'ya.ru', 'yandex.com'):
            self.server = 'imap.yandex.ru'
        else:
            raise ValueError("""В настоящее время доступно только использование почтовых серверов Mail и Yandex. 
            Для рассмотрения возможности использования вашего почтового сервера обратитесь к администратору бота ____"""
                             )

    def mail_fetch(self):
        if self.server:
            with MailBox(self.server).login(username=self.email, password=self.password) as mailbox:
                for msg in mailbox.fetch(criteria=A('NEW', f'FROM "{self.from_email}"'), reverse=True):
                    return {'date': msg.date,
                            'subject': msg.subject,
                            'html': msg.html,
                            'uid': msg.uid,
                            'attachments': msg.attachments}

    def is_connect(self):
        try:
            if MailBox(self.server).login(username=self.email, password=self.password):
                return True
        except:
            return False

    def mail_html(self):
        mail = self.mail_fetch()
        if mail:
            html_doc = mail.get('html')
            soup = BeautifulSoup(html_doc, 'html.parser')
            return soup.get_text(separator='\n')

    def mail_file(self):
        mail = self.mail_fetch()
        if mail:
            attachments = mail.get('attachments')
            return [(att.filename, att.payload) for att in attachments]

    def get_response(self, data_type_id):
        if data_type_id == 3:
            return self.mail_html()
        if data_type_id == 2:
            return self.mail_file()
        if data_type_id == 1:
            return
