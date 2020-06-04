from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^activation/$',views.student_activation, name='s_activation'),
    url(r'^forgot-password/$',views.forgot_password, name='s_forgot_pass'),
    url(r'^change-password/$',views.s_changepass, name='s_change_pass'),
    url(r'^create-profile/$',views.create_profile, name='s_create_profile'),
    url(r'^profile/$',views.student_profile_visit, name='s_profile'),
    url(r'^registration/(?P<cid>[\d]+)/$',views.registration_redirects, name='company_reg'),
    url(r'^placement-registration/(?P<cid>[\d]+)/$',views.placement_registeration, name='p_reg'),
    url(r'^placement-registration/(?P<cid>[\d]+)/(?P<rid>[\d]+)/$',views.placement_registeration, name='s_p_reg'),
    url(r'^internship-registration/(?P<cid>[\d]+)/$',views.internship_registeration, name='i_reg'),
    url(r'^internship-registration/(?P<cid>[\d]+)/(?P<rid>[\d]+)/$',views.internship_registeration, name='s_i_reg'),
    url(r'^login/$', auth_views.login, {'template_name': 's_login.html'}, name='s_login'),
    url(r'^logout/$',auth_views.logout, {'next_page': 'student:s_login'}, name = 's_logout'),
    url(r'^companies/$',views.s_home, name='s_home'),
    url(r'^$',views.all_home, name='all_home'),
    url(r'^alumni/$',views.alumni_s, name='alumni_s'),
    url(r'^courses/$',views.courses_s, name='courses_s'),
    url(r'^faculty/$',views.faculty_s, name='faculty_s'),
    url(r'^history/$',views.history_s, name='history_s'),
    url(r'^policy/$',views.policy_s, name='policy_s'),
    url(r'^procedure/$',views.procedure_s, name='procedure_s'),
    url(r'^students/$',views.students_life_s, name='students_s'),
    url(r'^resume-drive/$',views.resume_management_student, name='s_resume'),
    url(r'^contact-us/$',views.contact_us, name='contact_us'),
    url(r'^search/(?P<slug>[-\w\s+]+)/$',views.s_home, name='s_home_search'),
    url(r'^my-registrations/$',views.my_reg_list, name='my_reg'),
    url(r'^cancel-registrations/(?P<reg_id>[\d]+)/$',views.delete_registration, name='del_reg'),
    ]

#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr