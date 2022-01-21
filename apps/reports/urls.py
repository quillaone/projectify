from .views import ReportsListView, ReportDetailView
from .filters import ReportsFiltersView
from django.urls import path

urlpatterns = [
    path('report/', ReportsListView.as_view()),
    path('report/<int:pk>', ReportDetailView.as_view()),
    path('report/filters/', ReportsFiltersView.as_view())
]
