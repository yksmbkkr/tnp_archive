from student.models import s_registration
import random

def reg_id_generator():
    reg_no = str(random.randint(100000,999999))
    try:
        s_registration.objects.get(reg_id=reg_no)
        return reg_id_generator()
    except s_registration.DoesNotExist:
        return reg_no

#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr
