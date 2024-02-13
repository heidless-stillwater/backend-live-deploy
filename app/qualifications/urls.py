from django.urls import path
from .views import QualificationsListView

urlpatterns = [
    path('', QualificationsListView.as_view()),
]