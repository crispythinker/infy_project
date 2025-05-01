import pywhatkit



def send_msg(phone,msg):
    pywhatkit.sendwhatmsg_instantly(f'+{phone}',msg)
    print("messege sent")

# phone = '91 9665785718'
# response = "What message do you want to send?"
# msg = "something"
# send_msg(phone, msg)