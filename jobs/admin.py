from django.contrib import admin

# Register your models here.

from jobs.models import CustomUser, Skill, WorkHistory, SideProject, Education, Certification, Aspirant, AspirantProfile, JobPosting, JobApplication, Employer

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Customize the list display as needed
    list_display = ['username', 'email', 'is_staff']

    # Add additional fields to the user change form in admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','is_aspirant','is_employer')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add the ability to change password directly in the admin interface
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    actions = ['delete_selected']
    actions = ['delete_custom_users']

    def delete_custom_users(self, request, queryset):
        # Delete selected CustomUsers instances
        queryset.delete()

    delete_custom_users.short_description = "Delete selected Custom Users"


# Register the CustomUser model with the custom UserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
class SkillAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # New skill instance, check if at least one AspirantProfile is associated
            if not AspirantProfile.objects.exists():
                # No AspirantProfile exists, prevent saving
                self.message_user(request, "Cannot save Skill without associated AspirantProfile", level='ERROR')
                return
        super().save_model(request, obj, form, change)

admin.site.register(Skill, SkillAdmin)
class WorkHistoryInline(admin.TabularInline):
    model = WorkHistory
    extra = 1

class SideProjectInline(admin.TabularInline):
    model = SideProject
    extra = 1

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1

class AspirantProfileAdmin(admin.ModelAdmin):
    inlines = [
        WorkHistoryInline,
        SideProjectInline,
        EducationInline,
        CertificationInline,
    ]

    actions = ['delete_selected']
    actions = ['delete_aspirant_profiles']

    def delete_aspirant_profiles(self, request, queryset):
        # Delete selected AspirantProfile instances
        queryset.delete()

    delete_aspirant_profiles.short_description = "Delete selected Aspirant Profiles"

admin.site.register(AspirantProfile, AspirantProfileAdmin)
admin.site.register(Aspirant)

admin.site.register(JobPosting)
admin.site.register(JobApplication)
admin.site.register(Employer)

