from django.contrib import admin
from student.models import *

# Register your models here.



@admin.register(student_profile)
class student_profile_admin(admin.ModelAdmin):
    list_display = ('roll_no','branch')
    list_filter = ('branch','batch')
    search_fields = ('roll_no','user__email')

@admin.register(account_activation_check)
class account_activation_check_admin(admin.ModelAdmin):
    list_display = ('roll_no',)
    search_fields = ('roll_no',)

@admin.register(s_registration)
class s_registration_admin(admin.ModelAdmin):
    list_display = ('user','company')
    search_fields = ('user__username','company__name')
    exclude = ('reg_id',)

@admin.register(resume_drive)
class resume_drive_admin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)