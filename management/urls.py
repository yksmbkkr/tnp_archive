from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #url(r'^check/$', views.check),
    #url(r'^xlsx/$', views.xlxs_try),
    #url(r'^user_xlsx/$', views.user_xlsx,name='user_xlsx'),
    url(r'^add-student-db/$', views.student_db_add,name='student_db'),
    url(r'^update-student-db/$', views.student_db_update,name='student_db_update'),
    url(r'^$', views.home, name= 'm_home' ),
    #url(r'^trial/$', views.trial,),
    url(r'^add_user/$', views.add_user, name= 'add_user' ),
    url(r'^download_resume/$', views.get_resume_zip, name= 'r_downloader' ),
    url(r'^add_manager/$', views.create_manager, name= 'add_manager' ),
    url(r'^add_company/$', views.add_company, name= 'add_company' ),
    url(r'^login/$', auth_views.login, {'template_name': 'new/login.html', 'extra_context':{'log_nav_active':'active'}}, name='login'),
    url(r'^logout/$',auth_views.logout, {'next_page': 'management:login'}, name = 'logout'),
    url(r'^mod_pass/$', views.changepass, name= 'mod_pass' ),
    url(r'^search_company/$', views.search_company, name= 'search_company' ), 
    url(r'^search_user/$', views.search_user_extended, name= 'search_user' ), 
    url(r'^view-reg/$', views.view_registrations, name= 'view_reg' ),
    url(r'^view-reg-2/$', views.view_registrations_new, name= 'view_reg_new' ),
    url(r'^edit_company/(?P<id>[\d]+)/$', views.edit_company, name= 'edit_company' ),
    url(r'^search_company/(?P<field_type>[a-z]{4})/(?P<slug>[-\w+]+)/$', views.search_company, name= 'search_company_result' ),    
    url(r'^search_user/(?P<field_type>[_\w+]+)/(?P<slug>[-\w\s+]+)/$', views.search_user, name= 'search_user_result' ),    
    url(r'^view-reg/(?P<slug>[-\w\s+]+)/(?P<f_choice>[-\w\s+]+)/$', views.view_registrations, name= 'view_reg_search' ),    
    url(r'^view-reg-2/(?P<slug>[-\w\s+]+)/(?P<f_choice>[-\w\s+]+)/$', views.view_registrations_new, name= 'view_reg_search_new' ),
    url(r'^add-placement/$', views.add_placement_ajax, name= 'add_placement' ),
    url(r'^add-ppo/$', views.add_ppo_view, name= 'add_ppo' ),
    url(r'^get-ajax/$', views.load_user, name= 'ajax_user' ),
    url(r'^ban/$', views.ban_select, name= 'ban_select' ),
    url(r'^batch-email/$', views.batch_email_view, name= 'batch_emails' ),
    url(r'^send-sms/$', views.send_sms_view, name= 'send_sms' ),
    url(r'^batch-email-get-email-ajax/$', views.get_email_address_list, name= 'batch_email_get_email_ajax' ),
    url(r'^batch-email-boto-call-ajax/$', views.send_mail_boto_call_ajax, name= 'email_boto_call_ajax' ),
    url(r'^get-rej-ajax/$', views.get_registration_ajax, name= 'get_reg_ajax' ),
    url(r'^batch-email-template-preview-ajax/$', views.batch_email_template_preview_ajax, name= 'get_email_preview_ajax' ),
    url(r'^batch-email-select-ajax/$', views.batch_email_select_ajax, name= 'get_select_ajax' ),
    url(r'^ban/(?P<roll_no>[0-9]{1,4}[a-zA-Z]{1,5}[0-9]{1,4})/$', views.ban_proceed, name= 'ban_proceed' ),
    url(r'^revoke-ban/(?P<roll_no>[0-9]{1,4}[a-zA-Z]{1,5}[0-9]{1,4})/$', views.revoke_ban, name= 'revoke_ban' ),
    url(r'^modify-user/(?P<uid>[0-9]{1,20})/$', views.modify_user, name= 'modify_user' ),
    #url(r'^company_search/(?P<field_type>[a-z]{4})/(?P<slug>[-\w]+)')
    #This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr
    ]
