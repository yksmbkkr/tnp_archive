from django import forms
from .models import *
from management import models as m_models
from django.core.validators import RegexValidator
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

custom_validator = RegexValidator(r'^[-\w\s+]*$', 'Only alphanumeric characters including space and hyphen are allowed')
mobile_number_validator = RegexValidator(r'^[0-9]{10}$', 'Only 10 digit number is accepteable.')

gender_choice = (
    ('male','Male'),
    ('female','Female')
    )

category_choice = (
    ('general','General'),
    ('obc','OBC'),
    ('sc','SC'),
    ('st','ST')
    )

class student_activate_form(forms.Form):
    rollno = forms.CharField(required = True,max_length=11,widget=forms.TextInput(attrs={'class':'validate','data-length':'11'}))

#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr

class forgot_passoword_form(forms.Form):
    username = forms.CharField(required = True, max_length=20)

class student_profile_form(forms.ModelForm):
    f_name = forms.CharField(label='First Name',required = True,max_length=50,widget=forms.TextInput(attrs={'class':'validate'}))
    l_name = forms.CharField(label='Last Name',required = True,max_length=50,widget=forms.TextInput(attrs={'class':'validate'}))
    father = forms.CharField(label="Father's Name",required = True,max_length=50,widget=forms.TextInput(attrs={'class':'validate'}))
    mother = forms.CharField(label="Mother's Name",required = True,max_length=50,widget=forms.TextInput(attrs={'class':'validate'}))
    address = forms.CharField(label="Correspondence Address",required = True, widget = forms.Textarea(attrs = {'class':'materialize-textarea'}))
    mobile = forms.CharField(label="Mobile Number",validators=[mobile_number_validator], required = True, max_length=10,min_length=10, widget = forms.TextInput(attrs={'class':'validate', 'pattern':'[0-9]{10}','title':'10 digit mobile number only'}))
    branch = forms.ModelChoiceField(queryset = m_models.branches.objects.all(), empty_label = 'Select Branch', required = True)
    #be_marks = forms.DecimalField(max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'validate'}))
    marks_12 = forms.DecimalField(label="XII Percentage",max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'validate'}))
    marks_11 = forms.DecimalField(label="X Percentage",max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'validate'}))
    gender = forms.ChoiceField(choices = gender_choice, required = True)
    father_occupation = forms.CharField(label="Father's Occupation",required = True,max_length=150,widget=forms.TextInput(attrs={'class':'validate'}))
    mother_occupation = forms.CharField(label="Mother's Occupation", required = True,max_length=150,widget=forms.TextInput(attrs={'class':'validate'}))
    alternate_mobile = forms.CharField(label="Alternate Mobile Number",validators=[mobile_number_validator], required = True, max_length=10,min_length=10, widget = forms.TextInput(attrs={'class':'validate', 'pattern':'[0-9]{10}','title':'10 digit mobile number only'}))
    # backlogs = forms.DecimalField(max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'validate'}))
    intern_company = forms.CharField(label="Company You have Interned With (Name only)",required = True,max_length=200,widget=forms.TextInput(attrs={'class':'validate'}))
    permanent_address = forms.CharField(label="Permanent Address",required = True, widget = forms.Textarea(attrs = {'class':'materialize-textarea'}))
    category = forms.ChoiceField(choices = category_choice, required = True)
    passing_year_10 = forms.IntegerField(label="X Passing Year",required = True, widget = forms.TextInput(attrs = {'class':'validate', 'pattern':'[0-9]{4}','title':'4 digit year only'}))
    passing_year_12 = forms.IntegerField(label="XII Passing Year",required = True, widget = forms.TextInput(attrs = {'class':'validate', 'pattern':'[0-9]{4}','title':'4 digit year only'}))


    class Meta:
        model = student_profile
        fields = (
            'f_name',
            'l_name',
            'branch',
            'intern_company',
            'father',
            'father_occupation',
            'mother',
            'mother_occupation',
            'address',
            'permanent_address',
            'mobile',
            'alternate_mobile',
            'marks_11',
            'passing_year_10',
            'marks_12',
            'passing_year_12',
            'gender',
            'category',
            )

class home_search_form(forms.Form):
    slug = forms.CharField(validators=[custom_validator], required = True, max_length=20, widget = forms.TextInput(attrs={'class':'form-control'}))

class resume_drive_form(forms.ModelForm):
    resume1 = forms.FileField()
    resume2 = forms.FileField(required = False)
    resume3 = forms.FileField(required = False)
    
    def clean_resume1(self):
            resume1 = self.cleaned_data['resume1']
            if resume1:
                if '.com' in resume1.name:
                    raise forms.ValidationError(_('Unable to save : File name should not contain ".com"'),
                                                code='InvalidFileName', )
            try:
                content_type = resume1.content_type.split('/')[1]
                if content_type in settings.CONTENT_TYPES_PDF:
                    if resume1._size > settings.MAX_UPLOAD_SIZE:
                        raise forms.ValidationError(_('Please keep filesize under %(permitsize)s. Current filesize %(thissize)s'), code='InvalidFileSize', params ={'permitsize' : filesizeformat(settings.MAX_UPLOAD_SIZE), 'thissize':filesizeformat(resume1._size)},)
                else:
                    raise forms.ValidationError(_('File type is not supported. Only PDF supported.'), code = 'InvalidFileType',)
            except AttributeError:
                pass
            return resume1
    def clean_resume2(self):
            resume2 = self.cleaned_data['resume2']
            if resume2:
                if '.com' in resume2.name:
                    raise forms.ValidationError(_('Unable to save : File name should not contain ".com"'),
                                                code='InvalidFileName', )
            try:
                content_type = resume2.content_type.split('/')[1]
                if content_type in settings.CONTENT_TYPES_PDF:
                    if resume2._size > settings.MAX_UPLOAD_SIZE:
                        raise forms.ValidationError(_('Please keep filesize under %(permitsize)s. Current filesize %(thissize)s'), code='InvalidFileSize', params ={'permitsize' : filesizeformat(settings.MAX_UPLOAD_SIZE), 'thissize':filesizeformat(resume2._size)},)
                else:
                    raise forms.ValidationError(_('File type is not supported. Only PDF supported.'), code = 'InvalidFileType',)
            except AttributeError:
                pass
            return resume2
    def clean_resume3(self):
            resume3 = self.cleaned_data['resume3']
            if resume3:
                if '.com' in resume3.name:
                    raise forms.ValidationError(_('Unable to save : File name should not contain ".com"'),
                                                code='InvalidFileName', )
            try:
                content_type = resume3.content_type.split('/')[1]
                if content_type in settings.CONTENT_TYPES_PDF:
                    if resume3._size > settings.MAX_UPLOAD_SIZE:
                        raise forms.ValidationError(_('Please keep filesize under %(permitsize)s. Current filesize %(thissize)s'), code='InvalidFileSize', params ={'permitsize' : filesizeformat(settings.MAX_UPLOAD_SIZE), 'thissize':filesizeformat(resume3._size)},)
                else:
                    raise forms.ValidationError(_('File type is not supported. Only PDF supported.'), code = 'InvalidFileType',)
            except AttributeError:
                pass
            return resume3
    class Meta:
        model = resume_drive
        fields = {
            'resume1',
            'resume2',
            'resume3',
            }


class student_profile_edit_form(forms.ModelForm):
    f_name = forms.CharField(label='First Name',required = True,max_length=50,widget=forms.TextInput(attrs={'class':'validate'}))
    l_name = forms.CharField(label='Last Name',required = True,max_length=50,widget=forms.TextInput(attrs={'class':'validate'}))
    father = forms.CharField(label="Father's Name",required = True,max_length=50,widget=forms.TextInput(attrs={'class':'validate'}))
    mother = forms.CharField(label="Mother's Name",required = True,max_length=50,widget=forms.TextInput(attrs={'class':'validate'}))
    address = forms.CharField(label="Correspondence Address",required = True, widget = forms.Textarea(attrs = {'class':'materialize-textarea'}))
    mobile = forms.CharField(label="Mobile Number",validators=[mobile_number_validator], required = True, max_length=10,min_length=10, widget = forms.TextInput(attrs={'class':'validate', 'pattern':'[0-9]{10}','title':'10 digit mobile number only'}))
    #be_marks = forms.DecimalField(max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'validate'}))
    marks_12 = forms.DecimalField(label="XII Percentage",max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'validate'}))
    marks_11 = forms.DecimalField(label="X Percentage",max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'validate'}))
    gender = forms.ChoiceField(choices = gender_choice, required = True)
    father_occupation = forms.CharField(label="Father's Occupation",required = True,max_length=150,widget=forms.TextInput(attrs={'class':'validate'}))
    mother_occupation = forms.CharField(label="Mother's Occupation", required = True,max_length=150,widget=forms.TextInput(attrs={'class':'validate'}))
    alternate_mobile = forms.CharField(label="Alternate Mobile Number",validators=[mobile_number_validator], required = True, max_length=10,min_length=10, widget = forms.TextInput(attrs={'class':'validate', 'pattern':'[0-9]{10}','title':'10 digit mobile number only'}))
    # backlogs = forms.DecimalField(max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'validate'}))
    intern_company = forms.CharField(label="Company You have Interned With (Name only)",required = True,max_length=200,widget=forms.TextInput(attrs={'class':'validate'}))
    permanent_address = forms.CharField(label="Permanent Address",required = True, widget = forms.Textarea(attrs = {'class':'materialize-textarea'}))
    category = forms.ChoiceField(choices = category_choice, required = True)
    passing_year_10 = forms.IntegerField(label="X Passing Year",required = True, widget = forms.TextInput(attrs = {'class':'validate', 'pattern':'[0-9]{4}','title':'4 digit year only'}))
    passing_year_12 = forms.IntegerField(label="XII Passing Year",required = True, widget = forms.TextInput(attrs = {'class':'validate', 'pattern':'[0-9]{4}','title':'4 digit year only'}))


    class Meta:
        model = student_profile
        fields = (
            'f_name',
            'l_name',
            'intern_company',
            'father',
            'father_occupation',
            'mother',
            'mother_occupation',
            'address',
            'permanent_address',
            'mobile',
            'alternate_mobile',
            'marks_11',
            'passing_year_10',
            'marks_12',
            'passing_year_12',
            'gender',
            'category',
            )