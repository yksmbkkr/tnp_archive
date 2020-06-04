from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from student.models import s_registration,student_profile
from .choices import *
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from student.models import student_profile as s_profile
import re
import json
from django.utils import timezone as django_time

custom_validator = RegexValidator(r'^[-\w\s+]*$', 'Only alphanumeric characters including space and hyphen are allowed')
reg_id_validator= RegexValidator(r'^[\d]*$', 'Only alphanumeric characters including space and hyphen are allowed')
cap_validator=RegexValidator(r'^(\-?[1]{1})$|^([0-9]{1,50})$','Only integers are allowed')

class file_try_form(forms.Form):
    myfile = forms.FileField()

    def clean_myfile(self):
            myfile = self.cleaned_data['myfile']
            content_type = myfile.content_type.split('/')[1]
            if (myfile.name.split('.')[-1]).upper() != 'XLSX':
                self.add_error('myfile','Only XLSX files are supported.')
            if content_type in settings.CONTENT_TYPES:
                if myfile._size > settings.MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(_('Please keep filesize under %(permitsize)s. Current filesize %(thissize)s'), code='InvalidFileSize', params ={'permitsize' : filesizeformat(settings.MAX_UPLOAD_SIZE), 'thissize':filesizeformat(myfile._size)},)
            else:
                raise forms.ValidationError(_('File type is not supported. Only XLSX formated excel sheets are supported.'), code = 'InvalidFileType',)
            return myfile

class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder':'Old Password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder':'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder':'Confirm Password'})

#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr

class create_user_form(forms.Form):
    username = forms.CharField(max_length=11, required = True, widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'RollNumber', 'aria-describedby':'basic-addon1'}))
    email = forms.EmailField(max_length=254, required = True, widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Email', 'aria-describedby':'basic-addon1'}))

class create_manager_form(forms.Form):
    username = forms.CharField(max_length=11, required = True, widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Username', 'aria-describedby':'basic-addon1'}))
    email = forms.EmailField(max_length=254, required = True, widget = forms.EmailInput(attrs = {'class':'form-control', 'placeholder':'Email', 'aria-describedby':'basic-addon1'}))

class add_company_form(forms.ModelForm):
    name = forms.CharField(max_length=100, required = True, widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Name of Company', 'aria-describedby':'basic-addon1'}))
    for_batch = forms.ModelChoiceField(queryset=current_batch_year.objects.all(),empty_label='Select Batch', required = True, widget=forms.Select(attrs={'class':'form-control select2-single'}))
    ctc = forms.CharField(max_length=70, required = True, widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'CTC (Per Annum for Placement and Per Month for Internship.)', 'aria-describedby':'basic-addon1', 'pattern':'[0-9]{1,50}','title':'Integer Only'}))
    grade = forms.ModelChoiceField(queryset=company_grade.objects.all(),empty_label='Select Grade', required = True, widget=forms.Select(attrs={'class':'form-control select2-single'}))
    cutoff= forms.DecimalField(max_digits=5,decimal_places=2,required = True,widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Cut-Off', 'aria-describedby':'basic-addon1'}))
    branch_allowed = forms.ModelMultipleChoiceField(queryset=branches.objects.all(),required = True,
                                                   widget=forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple form-control',
                                                    'data-placeholder': 'Select Fields'}))
    backlogs_allowed = forms.IntegerField(required = True,widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Backlogs Allowed', 'aria-describedby':'basic-addon1'}))
    closing_date = forms.DateField(required = True, widget = forms.TextInput(attrs = {'class':'form-control datepicker', 'placeholder':'Closing Date', 'data-provide':'datepicker'}))
    cap = forms.CharField(validators=[cap_validator], max_length=70, required = False, initial='-1',widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Cap', 'aria-describedby':'basic-addon1', 'pattern':'\-?[0-9]{1,50}','title':'Integer Only'}))
    open_reg = forms.ChoiceField(choices= open_reg_choice, required = True, widget=forms.Select(attrs={'class': 'select form-control'}))

    class Meta:
        model = company
        fields = (
            'name',
            'for_batch',
            'ctc',
            'grade',
            'cutoff',
            'branch_allowed',
            'backlogs_allowed',
            'closing_date',
            'cap',
            'open_reg',
            )

class search_company_form(forms.Form):
    slug = forms.CharField(required = True, max_length=20, widget = forms.TextInput(attrs={'class':'form-control'}))
    field_choice = forms.ChoiceField(choices= c_search_choice, required = True, widget=forms.Select(attrs={'class': 'select form-control'}))

class search_student_form(forms.Form):
    slug = forms.CharField(validators=[custom_validator], required = True, max_length=20, widget = forms.TextInput(attrs={'class':'form-control'}))
    field_choice = forms.ChoiceField(choices= s_search_choice, required = True, widget=forms.Select(attrs={'class': 'select form-control'}))

class search_reg_form(forms.Form):
    slug = forms.CharField(validators=[custom_validator], required = True, max_length=20, widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Name of Company'}))
    field_choice = forms.ChoiceField(choices= reg_search_choice, required = True, widget=forms.Select(attrs={'class': 'select form-control'}))
    batch_choice = forms.ModelChoiceField(required=False, queryset=current_batch_year.objects.all(), empty_label = 'None Selected', widget=forms.Select(attrs={'class':'select form-control'}))


class add_placement_form(forms.Form):
    rid = forms.CharField(validators=[reg_id_validator], required = True, max_length=6, widget = forms.TextInput(attrs={'class':'form-control'}))


class trial_form(forms.Form):
    cmpn = forms.ModelChoiceField(required=True,queryset=company.objects.all(),widget=forms.Select(attrs={'class':'form-control js-example-basic-single','data-live-search':'true'}))
    roll_no = forms.ModelMultipleChoiceField(required=True,queryset=User.objects.none(), widget=forms.SelectMultiple(attrs={'class': 'js-example-basic-multiple form-control',
                                                    'data-placeholder': 'Select Roll No'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['roll_no'].queryset =User.objects.none()

        if 'cmpn' in self.data:
            try:
                cmpn_id = int(self.data.get('cmpn'))
                self.fields['roll_no'].queryset = s_registration.objects.filter(company__id=cmpn_id).order_by('reg_id')
            except (ValueError, TypeError):
                pass

class search_user_extended_form(forms.Form):
    slug = forms.CharField(required=False, validators=[custom_validator], widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Roll Number or Name'}))
    place = forms.ChoiceField(required=False, choices=place_choice,widget=forms.Select(attrs={'class':'form-control js-example-basic-single','data-live-search':'true'}))
    branch = forms.ModelMultipleChoiceField(required=False, queryset=branches.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control js-example-basic-multiple','data-live-search':'true'}))
    batch = forms.ModelChoiceField(required=False, queryset=current_batch_year.objects.all(), empty_label = 'None Selected', widget=forms.Select(attrs={'class':'form-control js-example-basic-single','data-live-search':'true'}))

class resume_download_form(forms.Form):
    cmpn = forms.ModelChoiceField(required=True,queryset=company.objects.all(), empty_label='Select Company', widget=forms.Select(attrs={'class':'form-control js-example-basic-single','data-live-search':'true'}))

class ban_select_form(forms.Form):
    rollno = forms.CharField(required = True, max_length=11, widget = forms.TextInput(attrs={'class':'form-control','pattern':'[0-9]{1,4}[a-zA-Z]{1,5}[0-9]{1,4}','title':'NSIT Roll Number Format - 0123ABC4567'}))
    #type_choice = forms.ChoiceField(choices= ban_select_choice, required = True, widget=forms.Select(attrs={'class': 'select form-control'}))

class ban_form(forms.Form):
    field1 = forms.DateField(required = False, label = 'Ban Till date :',widget = forms.TextInput(attrs = {'class':'form-control datepicker', 'placeholder':'Ban till date :', 'data-provide':'datepicker'}))
    field2 = forms.ModelMultipleChoiceField(required=False, queryset=company.objects.all(), label='Ban in companies : ',widget=forms.SelectMultiple(attrs={'class':'form-control js-example-basic-multiple','data-live-search':'true'}))
    field3 = forms.IntegerField(required = False, label = 'No. of upcoming companies to be banned for : ',widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder':'No. of upcoming companies to be banned for : ','pattern':'[0-9]{0,4}','title':'Integer Only'}))

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

class modify_user_form(forms.ModelForm):
    f_name = forms.CharField(required = True, label = 'First Name', max_length=50,widget=forms.TextInput(attrs = {'class':'form-control', 'aria-describedby':'basic-addon1'}))
    l_name = forms.CharField(required = True, label = 'Last Name', max_length=50,widget=forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    father = forms.CharField(required = True, label = "Father's Name", max_length=50,widget=forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    mother = forms.CharField(required = True, label = "Mother's name", max_length=50,widget=forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    address = forms.CharField(required = True, label = 'Current Address',  widget = forms.Textarea(attrs = {'class':'form-control', 'rows':'3'}))
    mobile = forms.CharField(validators=[mobile_number_validator], required = True, label = 'Mobile',  max_length=10,min_length=10, widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    branch = forms.ModelChoiceField(queryset = branches.objects.all(), empty_label = None, required = True, label = 'Branch', widget=forms.Select(attrs={'class': 'select form-control'}))
    batch = forms.ModelChoiceField(queryset = current_batch_year.objects.all(), empty_label = None, required = True, label = 'Batch', widget=forms.Select(attrs={'class': 'select form-control'}))
    be_marks = forms.DecimalField(max_digits=5,decimal_places=2,required = True, label = 'CGPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem1 = forms.DecimalField(max_digits=5,decimal_places=2,required = True, label = 'Sem 1 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem2 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 2 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem3 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 3 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem4 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 4 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem5 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 5 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem6 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 6 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    marks_12 = forms.DecimalField(max_digits=5,decimal_places=2,required = True, label = '12th marks', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    marks_11 = forms.DecimalField(max_digits=5,decimal_places=2,required = True, label = '10th marks', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    gender = forms.ChoiceField(choices = gender_choice, required = True, label = 'gender',  widget=forms.Select(attrs={'class': 'select form-control'}))
    father_occupation = forms.CharField(required = True, label = "Father's Occupation", max_length=150,widget=forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    mother_occupation = forms.CharField(required = True, label = "Mother's Occupation", max_length=150,widget=forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    alternate_mobile = forms.CharField(validators=[mobile_number_validator], required = True, label = 'Alternate Mobile',  max_length=10,min_length=10, widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1','pattern':'[0-9]{10}','title':'10 digit mobile number only'}))
    backlogs = forms.DecimalField(max_digits=5,decimal_places=2,required = True, label = "Backlogs", widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    intern_company = forms.CharField(required = True, label = 'Company od Internship', max_length=200,widget=forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    cgpa_drop=forms.DecimalField(max_digits=5,decimal_places=2,required = True, label = 'CGPA with drop', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    permanent_address = forms.CharField(required = True, label = 'Permanent Address',  widget = forms.Textarea(attrs = {'class':'form-control', 'rows':'3'}))
    category = forms.ChoiceField(choices = category_choice, required = True, label = 'Category',  widget=forms.Select(attrs={'class': 'select form-control'}))
    passing_year_10 = forms.IntegerField(required = True, label = '10th Passing Year',  widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1', 'pattern':'[0-9]{4}','title':'4 digit year only'}))
    passing_year_12 = forms.IntegerField(required = True, label = '12th Passing Year',  widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1', 'pattern':'[0-9]{4}','title':'4 digit year only'}))
    sem1 = forms.DecimalField(max_digits=5,decimal_places=2,required = True, label = 'Sem 1 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem2 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 2 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem3 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 3 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem4 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 4 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem5 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 5 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))
    sem6 = forms.DecimalField(max_digits=5,decimal_places=2,required = True,label = 'Sem 6 GPA', widget = forms.TextInput(attrs = {'class':'form-control',  'aria-describedby':'basic-addon1'}))


    class Meta:
        model = s_profile
        fields = (
            'f_name',
            'l_name',
            'gender',
            'branch',
            'batch',
             'category',
            'be_marks',
            'cgpa_drop',
            'sem1',
            'sem2',
            'sem3',
            'sem4',
            'sem5',
            'sem6',
            'backlogs',
            'intern_company',
            'marks_12',
            'passing_year_12',
            'marks_11',
            'passing_year_10',
            'father',
            'father_occupation',
            'mother',
            'mother_occupation',
            'address',
            'permanent_address',
            'mobile',
            'alternate_mobile',
            )


class view_reg_list_ajax_form(forms.Form):
    rList = forms.CharField(widget=forms.HiddenInput)

class batch_email_form(forms.Form):
    subject = forms.CharField(required = True, label = 'Subject of email.', max_length=150,widget=forms.TextInput(attrs = {'class':'form-control', 'aria-describedby':'basic-addon1', 'pattern':'[-0-9a-zA-Z| ]{5,}','title':'Characters allowed are "a-z","0-9"," ","|" and should have atleast 5 characters.'}))
    body = forms.CharField(required = True, label = 'Body of email.(Supports basic HTML tags.)', widget=forms.Textarea(attrs = {'class':'form-control', 'rows':'5',}))

class batch_email_select_branch_form(forms.Form):
    branch_name = forms.ModelChoiceField(required=True, queryset=branches.objects.all(), empty_label='Select Branch',label='Select Branch', widget=forms.Select(attrs={'class':'custom-select form-control select2-batch-mail'}))

class batch_email_select_company_form(forms.Form):
    company_name = forms.ModelChoiceField(required=True, queryset=company.objects.all(), empty_label='Select Company',label='Select Company', widget=forms.Select(attrs={'class':'form-control select2-batch-mail'}))

class batch_email_select_individual_form(forms.Form):
    user = forms.ModelMultipleChoiceField(required=True, queryset=User.objects.exclude(profile_set = None), label='Select Roll Nos.', widget=forms.SelectMultiple(attrs={'class':'form-control select2-batch-mail'}))

class batch_email_get_email_form(forms.Form):
    json_data_field = forms.CharField(widget=forms.HiddenInput)

    def clean_json_data_field(self):
        data_dict = json.loads(self.cleaned_data['json_data_field'])
        if not 'flag_type' in data_dict:
            self.add_error('json_data_field', 'Invalid Json Object.')
        if not 'id_list' in data_dict:
            self.add_error('json_data_field', 'Invalid Json Object.')
        return data_dict

class batch_email_boto_form(forms.Form):
    json_data = forms.CharField(widget=forms.HiddenInput)

    def clean_json_data(self):
        data_dict = json.loads(self.cleaned_data['json_data'])
        if not 'flag_type' in data_dict:
            self.add_error('json_data_field', 'Invalid Json Object.')
        if not 'id_list' in data_dict:
            self.add_error('json_data_field', 'Invalid Json Object.')
        return data_dict


class add_ppo_form(forms.Form):
    company_obj = forms.ModelChoiceField(queryset=company.objects.all(), empty_label='Select Company', required=True, label='Company',
                                   widget=forms.Select(attrs={'class': 'form-control select2-select'}))
    student_list = forms.ModelMultipleChoiceField(queryset=student_profile.objects.all(), required=True,
                                                    widget=forms.SelectMultiple(
                                                        attrs={'class': 'select2-select form-control',
                                                               'data-placeholder': 'Select Roll No'}))

    def clean_company_obj(self):
        company_obj = self.cleaned_data['company_obj']
        if not 'ppo'.upper() in company_obj.name.upper():
            self.add_error('company_obj', 'Error: Company name must contain PPO.')
        if company_obj.open_reg:
            self.add_error('company_obj', 'Error: registrations for the company selected must be disabled while addidng PPO')
        date = django_time.localdate()
        if date <= company_obj.closing_date:
            self.add_error('company_obj','Error: Last date of company selected must be in past.')
        return company_obj


class sms_form(forms.Form):
    receiver_list = forms.ModelMultipleChoiceField(queryset=student_profile.objects.all(), required=True, label = 'Select Students',
                                                    widget=forms.SelectMultiple(
                                                        attrs={'class': 'select2-select form-control',
                                                               'data-placeholder': 'Select Receiver'}))
    message_body = forms.CharField(required = True, label = 'SMS.(Max Char 140, Do not use any special character, For new line use \\n)', max_length=140,widget=forms.Textarea(attrs = {'class':'form-control', 'rows':'5', 'placeholder':"SMS.(Max Char 140, Do not use any special character, For new line use '\\n')",}))


