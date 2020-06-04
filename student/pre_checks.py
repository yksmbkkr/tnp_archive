from management.models import ban
from management.models import company as company_model
from django.utils import timezone as django_time
import datetime

def ban_pre_check(user,company):
    date = django_time.localdate()
    try:
        ban_obj = ban.objects.get(rollno = user.student_profile.roll_no.upper())
    except ban.DoesNotExist:
        return False, "Elligible"
    if ban_obj.company_count > 0:
        t = ban_obj.banned_on
        print(company_model.objects.filter(creation__gte = t).order_by('creation')[:ban_obj.company_count])
        if company in company_model.objects.filter(creation__gte = t).order_by('creation')[:ban_obj.company_count]:
            return True, "You were barred from applying in upcoming "+str(ban_obj.company_count)+" companies. This one is one of those !"
    if ban_obj.till_date == None:
        if company in ban_obj.companies.all():
            return True, "You are barred from applying in "+company.name
    if ban_obj.companies.all().count()<1 and ban_obj.company_count < 1:
        if date <= ban_obj.till_date:
            return True, "You are barred from applying in any company till "+ban_obj.till_date.strftime("%b %d %Y")
    else:
        if company in ban_obj.companies.all() and date <= ban_obj.till_date:
            return True, "You are barred from applying in company "+company.name+" till "+ban_obj.till_date.strftime("%b %d %Y")
    return False, "Elligible"