import os
from mailjet_rest import Client


sender_mail = os.getenv('MJ_SENDER_MAIL')
api_key = os.getenv('MJ_APIKEY_PUBLIC')
api_secret = os.getenv('MJ_APIKEY_PRIVATE')
mailjet = Client((api_key, api_secret), version='v3.1')


def send_mail(recipient_mail, content={}):
    subject = content.get('subject', None)
    textpart = content.get('text', None)
    html = content.get('html', None)
    data = {
    'Messages': [
        {
            "From": {
                "Email": sender_mail,
            },
            "To": [
                {
                    "Email": recipient_mail,
                }
            ],
            "Subject": subject if subject else "Mail from threading",
            "TextPart": textpart if textpart else "Greetings from Mailjet!",
            "HTMLPart": html if html else "<h3>Hello MM</h3>"
        }
        ]
    }
    result = mailjet.send.create(data=data)
    return result
  