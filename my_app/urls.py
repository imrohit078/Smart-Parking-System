from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('detect/', views.detect_redirect_page, name='detect_plate'),
    path('receipt/<int:session_id>/', views.receipt, name='receipt'),
    path('earnings/', views.earnings_report, name='earnings_report'),
    path('earnings/export/', views.export_earnings_csv, name='export_earnings_csv'),
    path('receipt/pdf/<int:session_id>/', views.generate_pdf_receipt, name='pdf_receipt'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update-session/<int:session_id>/', views.session_update_view, name='update_session'),
    path('manual-entry/', views.manual_entry_view, name='manual_entry'),

]
