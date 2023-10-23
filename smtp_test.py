# from dotenv import load_dotenv
# import os, smtplib

# load_dotenv('.env')

# def send_email(title, message, to_email):
#     sender = os.environ.get('smtp_email')
#     password = os.environ.get('smtp_password')

#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()

#     try:
#         server.login(sender, password)
#         server.sendmail(sender, to_email, message)
#         return "200 OK"
#     except Exception as error:
#         return f"Error: {error}"
# print(send_email('Hello', "Geeks", 'ahmatovasin@gmail.com'))

