#!/usr/bin/python

import dps

#client information
client_email = "mashuo93@gmail.com"
client_user_id = "40363624"
client_password = "RNX19930521,.ab"
client_month = "20170101"
client_date = {"20170110", "20161024", "20161025", "20161026", "20161027", "20161028", "20161031"}
dps.main(client_email, client_user_id, client_password, client_month, client_date)
print("success!")

