import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime
import time

my_sender = '285723576@qq.com'
my_pass = 'cugfeiqrfjsrcaac'
my_user = '2240823201@qq.com'

messages = "Testing_text"

subjects = "Testing_subject"


def sender(
        message,
        sender,
        sender_password,
        customer
        )-> str:# FOR GETTING BASIS INFORMATION
    msg = MIMEText(
        message,
        'plain',
        'utf-8'
        )# UTF-8 CODE 
    msg['From'] = formataddr(["sender", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["CK", customer])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = f"Program started at {mail_time}\n\nThe automated email program has started."  # 邮件的主题，也可以说是标题
    print("pre_msg") #PRE-MSG  INFORMATION DONE
    server = smtplib.SMTP_SSL("smtp.qq.com")
    server.connect("smtp.qq.com", 465)# SETTING EMAIL SERVER AND IT'S PROT
    server.login(sender, sender_password)
    print("msg_preprocressed")
    server.sendmail(sender,
                [customer],
                msg.as_string())# FOR INFORMATION TO SENDER
    server.quit()
    print("sent and quited")# DONE THE SENDER AND QUIT COLLECTING SERVER   

def mail():
    print("mail_sending")
    ret = True # RECORD PROGRAM RUNNING NORMALLY
    try:
        message_index = (
                                sent_count // 60
                        ) % 3  # Rotate between the three messages for every 60 emails sent
        subject_index = (
                                subject_index_offset + (
                                sent_count // 3
                        ) % 60
                        ) % 3  # Rotate between the three subjects for every 3 emails sent, and add the offset
        if int(sent_count) == 180:  # Reset the title offsets if 180 emails have been sent already
            current_date = datetime.datetime.now().date() + last_subject_reset_date
            if (current_date - last_subject_reset_date).days >= 30:  # Reset the title offsets every 30 days
                subject_index_offset = 0
                last_subject_reset_date = current_date
            else:
                subject_index_offset += 1
            sent_count = 0  # Start the loop of about 180 days again
        

        sender(
            sender=my_sender,
            sender_password=my_pass,
            customer=my_user
        )# BY SENDER FUNCTION TO SNED
        sent_count += 1 # RECORD THE SENT_COUNT

        print(f"Email sent successfully. Total emails sent: {sent_count}")
        
        # Save the current state to a file
        with open("email_state.txt", "w") as f:# TO SAVE THE PRECRESSING 
            f.write(f"{sent_count},{subject_index_offset},{last_subject_reset_date.isoformat()}")
            print("writing success")
        
        return sent_count, subject_index_offset, last_subject_reset_date


    except Exception as e:# WHILE ANY WRONG, PRINT THE INCORRECT WARNING, AND CHANGE THE RECORD TO FALSE 
        ret = False
        print(f"Email sending failed. Error message: {str(e)}")

    return ret