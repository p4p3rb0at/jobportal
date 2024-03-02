from django.urls import path
from jobs import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/aspirant/', views.aspirant_signup, name='aspirant_signup'),
    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('login/aspirant/', views.AspirantLoginView.as_view(template_name='aspirant_login.html'), name='aspirant_login'),
    path('login/employer/', views.EmployerLoginView.as_view(template_name='employer_login.html'), name='employer_login'),
    path('create/aspirant/profile/', views.create_aspirant_profile, name='create_aspirant_profile'),
    path('aspirant/resume/', views.aspirant_resume, name='aspirant_resume'),
    path('post/job/', views.post_job, name='post_job'),
    path('dashboard/aspirant', views.aspirant_dashboard, name='aspirant_dashboard'),
    path('apply/<int:job_posting_id>/', views.job_application, name='job_application'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('employer/job/<int:job_id>/applicant/<int:applicant_id>/shortlist/', views.shortlist_applicant, name='shortlist_applicant'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('access/denied/', views.access_denied, name='access_denied'),
    path('success/', views.success, name='success'),
    # Add other URL patterns as needed
]