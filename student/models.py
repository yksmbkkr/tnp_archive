from django.db import models
from django.contrib.auth.models import User
from management import models as m_models

def user_directory_path(instance, filename):
         return 'user_{0}/{1}'.format(instance.user.username, filename)


# Create your models here.

class account_activation_check(models.Model):
    roll_no = models.CharField(max_length = 20, primary_key = True)
    db_obj = models.OneToOneField(m_models.student_email_db, on_delete = models.CASCADE)
    check = models.BooleanField(default = False)
    def __str__(self):
        return self.roll_no

class student_profile(models.Model):
    f_name = models.CharField(max_length = 50)
    l_name = models.CharField(max_length = 50)
    father = models.CharField(max_length = 50)
    mother = models.CharField(max_length = 50)
    address = models.TextField()
    mobile = models.CharField(max_length = 10,default = '0000000000')
    branch = models.ForeignKey(m_models.branches, on_delete = models.CASCADE)
    roll_no = models.CharField(max_length = 11)
    batch = models.ForeignKey(m_models.current_batch_year, on_delete = models.CASCADE)
    be_marks = models.DecimalField(max_digits=5,decimal_places=2, verbose_name = "CGPA")
    marks_12 = models.DecimalField(max_digits=5,decimal_places=2, verbose_name = "12th Marks", default = 0)
    marks_11 = models.DecimalField(max_digits=5,decimal_places=2, verbose_name = "11th Marks", default = 0)
    gender = models.CharField(max_length = 50)
    father_occupation = models.CharField(max_length = 150)
    mother_occupation = models.CharField(max_length = 150)
    alternate_mobile = models.CharField(max_length = 10,default = '0000000000')
    backlogs = models.IntegerField(default=0)
    intern_company = models.CharField(max_length = 200)
    cgpa_drop = models.CharField(max_length = 15,default='0')
    permanent_address = models.TextField()
    category = models.CharField(max_length = 20)
    passing_year_10 = models.CharField(max_length = 20)
    passing_year_12 = models.CharField(max_length = 20)
    sem1 = models.CharField(max_length = 15,default = '0')
    sem2 = models.CharField(max_length = 15,default = '0')
    sem3 = models.CharField(max_length = 15,default = '0')
    sem4 = models.CharField(max_length = 15,default = '0')
    sem5 = models.CharField(max_length = 15,default = '0')
    sem6 = models.CharField(max_length = 15,default = '0')
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.roll_no + ' ('+self.f_name+' '+self.l_name+')'

    class Meta:
        ordering = ['f_name']
#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr
class s_registration(models.Model):
    reg_id = models.AutoField(primary_key=True)
    reg_type = models.ForeignKey(m_models.current_batch_year, on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    company = models.ForeignKey(m_models.company, on_delete=models.CASCADE)
    placed = models.BooleanField(default = False)
    r_file = models.IntegerField(verbose_name='Resume ID')
    def __str__(self):
        return str(self.reg_id)

    class Meta:
        ordering = ['reg_id']

class resume_drive(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    resume1 = models.FileField(upload_to=user_directory_path, null = True)
    resume2 = models.FileField(upload_to=user_directory_path, null = True)
    resume3 = models.FileField(upload_to=user_directory_path, null = True)
    def __str__(self):
        return self.user.username
