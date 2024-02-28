from django.db import models

# Create your models here.
from jobs.utils import CustomUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_aspirant = models.BooleanField(default=False)

    objects = CustomUserManager()

    class Meta:
        # Define unique related_names for groups and user_permissions
        permissions = (("can_view_custom_permissions", "Can view custom permissions"),)
        default_related_name = 'custom_users'
    
    # Override the related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='auth_users')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='auth_users')
    
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AspirantProfile(models.Model):
    # Other fields as needed
    skills = models.ManyToManyField(Skill)

class WorkHistory(models.Model):
    aspirant_profile = models.ForeignKey(AspirantProfile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

class SideProject(models.Model):
    aspirant_profile = models.ForeignKey(AspirantProfile, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=100)
    github_link = models.URLField()

class Education(models.Model):
    aspirant_profile = models.ForeignKey(AspirantProfile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

class Certification(models.Model):
    aspirant_profile = models.ForeignKey(AspirantProfile, on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)

class Aspirant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    profile = models.OneToOneField('AspirantProfile', on_delete=models.CASCADE, related_name='aspirant')

    def __str__(self):
        return self.user.username + f'{self.profile}'

class JobPosting(models.Model):
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill)
    created_at = models.DateTimeField(auto_now_add=True)

class JobApplication(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    aspirant = models.ForeignKey(Aspirant, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    is_shortlisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    # Add any additional fields specific to employer
