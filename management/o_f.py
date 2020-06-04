from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
import string
from random import randint, choice

#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr

def user_creator_(username, email,request):
        try:
                min_char = 12
                max_char = 20
                allchar = string.ascii_letters + string.punctuation + string.digits
                passwd = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
                user = User.objects.create_user(username = username, email = email, password=passwd)                
                pass_form = PasswordResetForm({'email':email})
                assert pass_form.is_valid()
                pass_form.save(request=request, subject_template_name = 'first_pass.txt', email_template_name='first_pass_email.html', from_email="no-reply@tnp.nsutonline.in", )
        except Exception as e:
                e_dict = {'rollno':username,'exception':e}
                return e_dict
        return None

def user_creator_2(username, email,request):
        try:
                min_char = 12
                max_char = 20
                allchar = string.ascii_letters + string.punctuation + string.digits
                passwd = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
                user = User.objects.create_user(username = username, email = email, password=passwd)                
                pass_form = PasswordResetForm({'email':email})
                assert pass_form.is_valid()
                pass_form.save(request=request, subject_template_name = 'first_pass.txt', email_template_name='first_pass_email.html', from_email="no-reply@tnp.nsutonline.in", )
        except Exception as e:
                e_dict = {'rollno':username,'exception':e}
                return e_dict
        return user

                
