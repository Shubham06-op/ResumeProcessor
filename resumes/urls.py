from django.urls import path
from .views import ResumeExtractView

urlpatterns = [
    path('extract_resume/', ResumeExtractView.as_view(), name='extract_resume'),  # Updated to match your endpoint
]
