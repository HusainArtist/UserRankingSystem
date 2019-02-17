from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage


def html_mail(sub,emailmsg,to):

    msg = EmailMultiAlternatives(sub, emailmsg, "no_reply@game.com", to)

    msg.attach_alternative(emailmsg, "text/html")

    try:
        r = msg.send() 

    except:
        pass

    else:
        pass
