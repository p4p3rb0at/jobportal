# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from jobs.models import CustomUser, Skill

class AspirantSignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_aspirant = True
        if commit:
            user.save()
        return user

class EmployerSignupForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'company_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
        return user
    

from jobs.models import AspirantProfile, WorkHistory, SideProject, Education, Certification


from django.utils.datastructures import MultiValueDict

class AspirantProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.SelectMultiple)

    class Meta:
        model = AspirantProfile
        fields = ['skills',]

class WorkHistoryForm(forms.ModelForm):
    class Meta:
        model = WorkHistory
        fields = ['job_title', 'company', 'duration']

WorkHistoryFormSet = forms.inlineformset_factory(
    AspirantProfile,
    WorkHistory,
    form=WorkHistoryForm,
    extra=1,
    can_delete=True
)

class SideProjectForm(forms.ModelForm):
    class Meta:
        model = SideProject
        fields = ['project_title', 'github_link']

SideProjectFormSet = forms.inlineformset_factory(
    AspirantProfile,
    SideProject,
    form=SideProjectForm,
    extra=1,
    can_delete=True
)

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'duration']

EducationFormSet = forms.inlineformset_factory(
    AspirantProfile,
    Education,
    form=EducationForm,
    extra=1,
    can_delete=True
)

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['certification_name', 'year']

CertificationFormSet = forms.inlineformset_factory(
    AspirantProfile,
    Certification,
    form=CertificationForm,
    extra=1,
    can_delete=True
)

from jobs.models import JobPosting

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'skills_required']

from jobs.models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter']

