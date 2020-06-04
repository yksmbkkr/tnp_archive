from django.contrib import admin
from management.models import *

# Register your models here.

admin.site.register(branches)
admin.site.register(branch_type)
admin.site.register(managers)
admin.site.register(company_grade)


admin.site.register(current_batch_year)

@admin.register(company)
class company_admin(admin.ModelAdmin):
    list_display = ('name', 'ctc', 'grade')
    list_filter = ('branch_allowed', 'grade')
    search_fields =  ('name', )

@admin.register(student_email_db)
class student_email_db_admin(admin.ModelAdmin):
    list_display = ('rollno','email')
    list_filter = ('batch',)
    search_fields = ('rollno','email')

@admin.register(ban)
class ban_admin(admin.ModelAdmin):
    list_display = ('rollno', 'banned_by', 'banned_on')
    search_fields = ('rollno',)

@admin.register(profile_set)
class profile_set_admin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(sms_logs)
class sms_logs_admin(admin.ModelAdmin):
    list_display = ('get_from_to','message_body','timestamp')
    search_fields = ('sender','receiver','message_body')
    def get_from_to(self,obj):
        return obj.sender.username + ' - ' + obj.receiver.username