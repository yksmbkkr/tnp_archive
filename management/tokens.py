from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr

class first_pass_set_token_generator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.first_pass_set.check)
            )

first_pass_set_token = first_pass_set_token_generator()
