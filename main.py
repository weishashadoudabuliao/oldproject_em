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

sent_count = 0
subject_index_offset = 0
last_subject_reset_date = datetime.datetime.now().date()
EMAIL_USE_SSL = True
server = smtplib.SMTP_SSL("smtp.qq.com")


def mail():
    print("mail_sending")
    ret = True
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
        

        msg = MIMEText(messages, 'plain', 'utf-8')
        msg['From'] = formataddr(["Your son", my_sender])
        msg['To'] = formataddr(["FK", my_user])
        msg['Subject'] = f"{subjects[subject_index]} ({sent_count + 1}/{180})"

        server = smtplib.SMTP_SSL("smtp.qq.com")
        server.connect("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user], msg.as_string())
        server.quit()

        sent_count += 1
        print(f"Email sent successfully. Total emails sent: {sent_count}")

        # Save the current state to a file
        with open("email_state.txt", "w") as f:
            f.write(f"{sent_count},{subject_index_offset},{last_subject_reset_date.isoformat()}")
            print("writing success")
        return sent_count, subject_index_offset, last_subject_reset_date

    except Exception as e:
        ret = False
        print(f"Email sending failed. Error message: {str(e)}")

    return ret


print("Start_running")
server.quit()
# Load the previous state if available
try:
    with open("email_state.txt", "r") as f:
        sent_count_str, subject_index_offset_str, last_subject_reset_date_str = f.read().split(",")
        sent_count = int(sent_count_str)
        subject_index_offset = int(subject_index_offset_str)
        last_subject_reset_date = datetime.datetime.fromisoformat(last_subject_reset_date_str).date()
        print(
            f"Loaded previous state: sent count = {sent_count}, subject index offset = {subject_index_offset}, last subject reset date = {last_subject_reset_date}")
except FileNotFoundError as ass:
    print(f"FileNotFoundError:{ass}")
    pass
print("done_setup")
# Send a start-up email
mail_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

msg = MIMEText(f"Subject: Program started at {mail_time}\n\nThe automated email program has started.", 'plain',
               'utf-8')
msg['From'] = formataddr(["sender", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
msg['To'] = formataddr(["CK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
msg['Subject'] = f"Program started at {mail_time}\n\nThe automated email program has started."  # 邮件的主题，也可以说是标题
print("cf")
server = smtplib.SMTP_SSL("smtp.qq.com")
server.connect("smtp.qq.com", 465)
server.login(my_sender, my_pass)
print("cf_logined")
server.sendmail(my_sender,
                ["285723576@qq.com"],
                msg.as_string())
server.quit()
print("Start-up email sent!")
print("done_start_up")
# Send the emails every day at 9am, 12pm, and 6pm
while True:
    now = datetime.datetime.now()

    # Send emails at 9am, 12pm, and 6pm
    if now.hour in [9, 12, 21] and now.minute == 0:
        mail()
    elif now.hour == 21 and now.minute == 10:
        print("escaping")
        msg = MIMEText(f"Subject: Program is stopped at {mail_time}",
                       'plain',
                       'utf-8')
        msg['From'] = formataddr(
            {
                "sender",
                my_sender
            }
        )  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["M", "285723576@qq.com"])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = f"Program started at {mail_time}\n\nThe automated email program has started."  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com")
        server.connect("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender,
                        ["285723576@qq.com"],
                        msg.as_string())
        server.quit()
        print("escaped")
        break
    time.sleep(60)  # Sleep for 1 minute before checking again
