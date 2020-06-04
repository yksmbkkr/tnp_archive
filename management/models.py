from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr

def validate_batch_name(name):
    if not str(name) in ['Internship', 'Placement']:
         raise ValidationError(
            _('Name can either be "Placement" or "Internship"'),
        )

class current_batch_year(models.Model):
    year = models.PositiveIntegerField()
    name = models.CharField(max_length = 20)

    def clean(self, *args, **kwargs):
        if current_batch_year.objects.all().count() > 1 :
            raise ValidationError(
            _('There can not be more than 2 entries in this table. It already contains 2 so you can not add more.'),
        )
        str1 = self.name
        if not str(str1) in ['Internship', 'Placement']:
            raise ValidationError(
            _('Name can either be "Placement" or "Internship"'),
        )
        super(current_batch_year, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(current_batch_year, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class profile_set(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    check = models.BooleanField(default = False)
    def __str__(self):
        return self.user.get_username()

class user_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    be_marks = models.CharField(max_length = 5)

class managers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    email = models.EmailField(unique = True)
    creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.get_username()

class branch_type(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name


class branches(models.Model):
    code = models.CharField(max_length = 3, unique = True)
    name = models.CharField(max_length = 5, unique=True)
    branchType = models.ForeignKey(branch_type, on_delete=models.CASCADE)
    def __str__(self):
        return self.name



class company_grade(models.Model):
    grade = models.IntegerField(primary_key=True)
    grade_name = models.CharField(unique = True, max_length = 10)
    def __str__(self):
        return self.grade_name

class company(models.Model):
    name = models.CharField(max_length = 50)
    for_batch = models.ForeignKey(current_batch_year, on_delete=models.CASCADE)
    slug_name = models.CharField(max_length = 70, null = True)
    ctc = models.IntegerField(default = 0)
    grade = models.ForeignKey(company_grade,on_delete = models.CASCADE)
    cutoff = models.DecimalField(max_digits=5,decimal_places=2, verbose_name = "Cut-off")
    branch_allowed = models.ManyToManyField(branches,db_table="branchElligibleForCompany")
    backlogs_allowed = models.IntegerField()
    closing_date = models.DateField()
    cap = models.IntegerField(default = -1,blank = False)
    open_reg = models.BooleanField(default = True)
    creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.for_batch is None:
            return self.name
        return self.name + " ( "+self.for_batch.name+" )"

    class Meta:
        ordering = ['name']

class student_email_db(models.Model):
    rollno = models.CharField(max_length = 20, unique = True,primary_key = True)
    email = models.CharField(max_length = 150, unique = True)
    cgpa = models.CharField(max_length = 150,default = '0')
    backlog = models.CharField(max_length=10,default = '0')
    sem1 = models.CharField(max_length = 15,default = '0')
    sem2 = models.CharField(max_length = 15,default = '0')
    sem3 = models.CharField(max_length = 15,default = '0')
    sem4 = models.CharField(max_length = 15,default = '0')
    sem5 = models.CharField(max_length = 15,default = '0')
    sem6 = models.CharField(max_length = 15,default = '0')
    batch = models.CharField(max_length = 15, default = '2020')
    def __str__(self):
        return self.rollno

class ban(models.Model):
    rollno = models.CharField(max_length = 20, unique = True)
    till_date = models.DateField(null = True)
    companies = models.ManyToManyField(company,db_table="bannedInCompany",blank=True)
    company_count = models.IntegerField(default = 0)
    banned_by = models.ForeignKey(User,on_delete = models.PROTECT)
    banned_on = models.DateTimeField()
    def __str__(self):
        return self.rollno

class sms_logs(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sms_logs_receiver')
    message_body = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username+' - '+self.receiver.username