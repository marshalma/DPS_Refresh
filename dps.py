import requests
import smtplib
import time
from email.mime.text import MIMEText
import email.utils
import http_post_fields

url = 'https://booknow.securedata-trans.com/1qed83ds/'
timeout = 15.0

def send_mail(body, client_email):
    msg = MIMEText(body+'\r\nhttps://booknow.securedata-trans.com/1qed83ds/')
    msg['To'] = email.utils.formataddr(('client', client_email))
    msg['From'] = email.utils.formataddr(('Shuo', 'mashuo93@gmail.com'))
    msg['Subject'] = 'Test Spot!'
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('mashuo93@gmail.com', '4NX-KXG-6fz-Zm2')
    mail.sendmail('mashuo93@gmail.com', client_email, msg.as_string())
    mail.close()


def view_available_time(day):
    data_view = http_post_fields.fields_view_time
    data_view['starting_date'] = day
    data_view['date_ymd'] = day

    try:
        r_view_time = requests.post(url, data=data_view, timeout=timeout)
    except Exception:
        print('time out')
        return

    html_view_time_str = r_view_time.text
    _index1 = html_view_time_str.find('0am')
    _index2 = html_view_time_str.find('0pm')
    if _index2 > 0: #pm
        _index3 = _index2-6 + html_view_time_str[_index2-6:].find('b>')
        hour = int(html_view_time_str[_index3+2:_index2-2]) + 12
        minite = int(html_view_time_str[_index2-1:_index2+1])
    elif _index1 > 0: #am
        _index3 = _index1-6 + html_view_time_str[_index1-6:].find('b>')
        hour = int(html_view_time_str[_index3+2:_index1-2])
        minite = int(html_view_time_str[_index1-1:_index1+1])

    r_view_time.close()
    return hour*60+minite


def submit_appt(day,time):
    data_submit = http_post_fields.fields_submit_appt
    data_submit['starting_date'] = day
    data_submit['appt_date'] = day
    data_submit['appt_start_time'] = str(time)
    data_submit['appt_end_time'] = str(time+20)
    try:
        r_submit_appt = requests.post(url, data=data_submit, timeout=timeout)
    except Exception:
        print('time out')
        return
    r_submit_appt.close()
    print('success! day: %s, time: %d' %(day, time))

# main


def main(client_email, client_user_id, client_password, client_month, client_date):
    
    http_post_fields.field_checking_spots['prev_date'] = client_month
    http_post_fields.fields_submit_appt['loginname'] = client_user_id
    http_post_fields.fields_submit_appt['password'] = client_password

    iteration = 0
    while 1:
        # http post request and decode the page file
        try:
            r_check = requests.post(url, data = http_post_fields.field_checking_spots, timeout=timeout)
        except Exception:
            print('iter: %d, time out' % iteration, end='\n')
            iteration += 1
            r_check.close()
            continue
        html_str = r_check.text

        # search for first available spot in html file
        index1 = html_str.find('calendar-available')
        while index1 > 0:
            index2 = index1 + html_str[index1:].find('dosubmit')
            index3 = index2 + html_str[index2:].find('\'')
            index4 = index3 + 1 + html_str[index3+1:].find('\'')
            day = html_str[index3+1:index4]

            if day in client_date:
                send_mail(day, client_email)
                time = view_available_time(day)
                submit_appt(day,time)
                return
            else:
                index1 = html_str.find('calendar-available', index1+1)

        print('iter: %d, not found' % iteration, end='\n')
        iteration += + 1
        r_check.close()


# write html to file
# file = open('page.html','w')
# file.write(html_str)
# print('write success!')
