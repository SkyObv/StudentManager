from django.urls import path
from .views import StudentListView

urlpatterns = [
    path('getStuidents/', StudentListView.as_view()),
]