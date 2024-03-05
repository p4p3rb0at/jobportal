# Create your views here.
from django.shortcuts import render, redirect
from django.urls import path, reverse_lazy
from django.shortcuts import render, get_object_or_404
from jobs.forms import AspirantSignupForm, EmployerSignupForm, AspirantProfileForm
from jobs.models import Aspirant,CustomUser
from django.contrib.auth.views import LoginView

def index(request):
    return render(request, 'index.html')

class AspirantLoginView(LoginView):
    template_name = 'aspirant_login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # If the user is already authenticated, redirect to a specific view
            return redirect(reverse_lazy('aspirant_dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Specify the name of the URL pattern you want to redirect to after successful login
        return reverse_lazy('create_aspirant_profile')
    
class EmployerLoginView(LoginView):
    template_name = 'employer_login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # If the user is already authenticated, redirect to a specific view
            return redirect(reverse_lazy('employer_dashboard'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        # Specify the name of the URL pattern you want to redirect to after successful login
        return reverse_lazy('employer_dashboard')

def aspirant_signup(request):
    if request.method == 'POST':
        form = AspirantSignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page or any other page
            return redirect('aspirant_login')
    else:
        form = AspirantSignupForm()
    return render(request, 'aspirant_signup.html', {'form': form})

def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            user = CustomUser.objects.get(username=form.cleaned_data['username'])
            employer, created = Employer.objects.get_or_create(user=user)
            employer.company_name = form.cleaned_data['company_name']
            employer.save()
            # Redirect to login page or any other page
            return redirect('employer_login')
    else:
        form = EmployerSignupForm()
    return render(request, 'employer_signup.html', {'form': form})

from jobs.forms import AspirantProfileForm, WorkHistoryFormSet, SideProjectFormSet, EducationFormSet, CertificationFormSet

def create_aspirant_profile(request):
    try:
        aspirant = Aspirant.objects.get(user=request.user)
        # If an Aspirant instance exists, redirect to another view
        return redirect(reverse_lazy('aspirant_dashboard'))
    except Aspirant.DoesNotExist:
        pass  # If no Aspirant instance exists, proceed with the login process
    if request.method == 'POST':
        aspirant_profile_form = AspirantProfileForm(request.POST)
        print(aspirant_profile_form)
        work_history_formset = WorkHistoryFormSet(request.POST, prefix='work_history')
        side_project_formset = SideProjectFormSet(request.POST, prefix='side_project')
        education_formset = EducationFormSet(request.POST, prefix='education')
        certification_formset = CertificationFormSet(request.POST, prefix='certification')

        if (aspirant_profile_form.is_valid() and work_history_formset.is_valid() and
                side_project_formset.is_valid() and education_formset.is_valid() and certification_formset.is_valid()):
            aspirant_profile = aspirant_profile_form.save(commit=False)
            aspirant_profile.save()

            skills = request.POST.getlist('skills')
            aspirant_profile.skills.set(skills)
            aspirant_profile.save()

            work_history_formset.instance = aspirant_profile
            work_history_formset.save()

            side_project_formset.instance = aspirant_profile
            side_project_formset.save()

            education_formset.instance = aspirant_profile
            education_formset.save()

            certification_formset.instance = aspirant_profile
            certification_formset.save()

            # Create an instance of Aspirant and associate it with the AspirantProfile
            aspirant, created = Aspirant.objects.get_or_create(user=request.user, profile=aspirant_profile)
            return redirect('aspirant_resume')
    else:
        aspirant_profile_form = AspirantProfileForm()
        work_history_formset = WorkHistoryFormSet(prefix='work_history')
        side_project_formset = SideProjectFormSet(prefix='side_project')
        education_formset = EducationFormSet(prefix='education')
        certification_formset = CertificationFormSet(prefix='certification')

    return render(request, 'create_aspirant_profile.html', {
        'aspirant_profile_form': aspirant_profile_form,
        'work_history_formset': work_history_formset,
        'side_project_formset': side_project_formset,
        'education_formset': education_formset,
        'certification_formset': certification_formset,
    })

# views.py
from jobs.models import AspirantProfile, WorkHistory, SideProject, Education, Certification, Skill

def aspirant_resume(request):
    try:
        aspirant = Aspirant.objects.get(user=request.user)
        aspirant_profile = AspirantProfile.objects.get(aspirant = aspirant)
        skills = Skill.objects.filter(aspirantprofile=aspirant_profile)
        work_history_list = WorkHistory.objects.filter(aspirant_profile=aspirant_profile)
        side_project_list = SideProject.objects.filter(aspirant_profile=aspirant_profile)
        education_list = Education.objects.filter(aspirant_profile=aspirant_profile)
        certification_list = Certification.objects.filter(aspirant_profile=aspirant_profile)
    except AspirantProfile.DoesNotExist:
        aspirant_profile = None
        work_history_list = []
        side_project_list = []
        education_list = []
        certification_list = []

    return render(request, 'aspirant_resume.html', {
        'aspirant_profile': aspirant_profile,
        'skills': skills,
        'work_history_list': work_history_list,
        'side_project_list': side_project_list,
        'education_list': education_list,
        'certification_list': certification_list,
    })

from django.contrib.auth.decorators import login_required
from jobs.forms import JobPostingForm
from jobs.models import Employer

def post_job(request):
    if not request.user.is_employer:
        return redirect('access_denied')  # Redirect to an access denied page or login page for employers
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            employer = Employer.objects.get(user__username = request.user)
            job_posting.employer = employer
            #print(job_posting.skills_required)
            job_posting.save()
            skills_required = form.cleaned_data['skills_required']
            job_posting.skills_required.set(skills_required)
            return redirect('success')  # Redirect to a success page
    else:
        form = JobPostingForm()
    return render(request, 'post_job.html', {'form': form})

from jobs.models import JobPosting

def aspirant_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'aspirant'):
        aspirant = Aspirant.objects.get(user = request.user)
        aspirant_skills = aspirant.profile.skills.all()
        matched_jobs = JobPosting.objects.filter(skills_required__in=aspirant_skills).distinct()
        applied = JobPosting.objects.filter(applications__aspirant=request.user.aspirant)
        jobs = JobPosting.objects.all()
        return render(request, 'aspirant_dashboard.html', {'matched_jobs': matched_jobs,'jobs':jobs, 'applied':applied })
    else:
        return render(request, 'access_denied.html')  # Redirect to an access denied page

from jobs.models import JobApplication
from jobs.forms import JobApplicationForm

def job_application(request, job_posting_id):
    job_posting = JobPosting.objects.get(id=job_posting_id)
    aspirant = request.user.aspirant
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid() and not JobApplication.objects.filter(job_posting=job_posting, aspirant=aspirant).exists():
            job_application = form.save(commit=False)
            
            job_application.job_posting = job_posting
            job_application.aspirant = aspirant  # Assuming Aspirant is related to User
            job_application.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = JobApplicationForm()
    return render(request, 'job_application.html', {'form': form, 'job_posting': job_posting})

def employer_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'employer'):
        employer = request.user.employer
        job_postings = JobPosting.objects.filter(employer=employer)
        return render(request, 'employer_dashboard.html', {'job_postings': job_postings})
    else:
        return render(request, 'access_denied.html')  # Redirect to an access denied page

def view_applicants(request, job_id):
    if request.user.is_authenticated and hasattr(request.user, 'employer'):
        job_posting = get_object_or_404(JobPosting, id=job_id, employer=request.user.employer)
        applicants = job_posting.applications.all()
        return render(request, 'view_applicants.html', {'job_posting': job_posting, 'applicants': applicants})
    else:
        return render(request, 'access_denied.html')  # Redirect to an access denied page

def view_applicants(request, job_id):
    if request.user.is_authenticated and hasattr(request.user, 'employer'):
        job_posting = get_object_or_404(JobPosting, id=job_id, employer=request.user.employer)
        applicants = job_posting.applications.all()
        return render(request, 'view_applicants.html', {'job_posting': job_posting, 'applicants': applicants})
    else:
        return render(request, 'access_denied.html')  # Redirect to an access denied page
    
def shortlist_applicant(request, job_id, applicant_id):
    if request.user.is_authenticated and hasattr(request.user, 'employer'):
        job_posting = get_object_or_404(JobPosting, id=job_id, employer=request.user.employer)
        applicant = get_object_or_404(JobApplication, id=applicant_id, job_posting=job_posting)
        applicant.is_shortlisted = True
        applicant.save()
        return redirect('view_applicants', job_id=job_id)
    else:
        return render(request, 'access_denied.html')  # Redirect to an access denied page

def posted_jobs(request):
    if request.user.is_authenticated and hasattr(request.user, 'employer'):
        employer = request.user.employer
        posted_jobs = JobPosting.objects.filter(employer=employer)
        return render(request, 'posted_jobs.html', {'posted_jobs': posted_jobs})
    else:
        return render(request, 'access_denied.html')
      
def access_denied(request):
    return render(request,'access_denied.html')

def success(request):
    return render(request,'success.html')

