from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('pdf/<int:pdf_id>/', views.pdf_detail, name='pdf_detail'),
    path('pdf/<int:pdf_id>/share/', views.generate_share_link, name='generate_share_link'),
    path('shared/<uuid:uuid>/', views.shared_pdf_view, name='shared_pdf'),
]
