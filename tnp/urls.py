"""
Definition of urls for tnp.
"""

from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from management import views as m_views
from student import views as s_views
from django.conf.urls import handler404, handler500
from . import views


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', tnp.views.home, name='home'),
    # url(r'^tnp/', include('tnp.tnp.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^ps-r558u/', include(admin.site.urls)),
    url(r'^management/',include('management.urls', namespace='management')),
    url(r'^',include('student.urls', namespace='student')),
    #url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'password_reset_form.html', 'email_template_name':'password_reset_email.html','subject_template_name':'password_reset_subject.txt','extra_context':{'pswd_nav_active':'active color-change'}}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name':'password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name':'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name':'password_reset_complete.html'}, name='password_reset_complete'),
   #url(r'^su/$', m_views.search_user_extended),
    #url(r'^mdc/$', s_views.mdc),
]

handler404 = views.error_404
handler500 = views.error_500
admin.site.site_header = "TNP Admin Portal"
admin.site.site_title = "TNP Admin Portal"
admin.site.index_title = "Welcome to TNP Admin Portal"
