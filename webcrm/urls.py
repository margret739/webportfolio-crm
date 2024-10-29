from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('customer/<int:pk>', views.record_customer, name='customer'),
    path('delete_customer/<int:pk>', views.delete_customer, name='delete_customer'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('update_customer/<int:pk>', views.update_customer, name='update_customer'),
    path('agent/', views.agent_list, name='agent'),
    path('agent/<int:pk>/', views.agent_customer, name='agent_customer'),
    path('add_agent/', views.add_agent, name='add_agent'),
    path('agent_detail/<int:pk>/', views.agent_detail, name='agent_detail'),
    path('agent_delete/<int:pk>', views.agent_delete, name='agent_delete'),
    path('agent_update/<int:pk>/', views.agent_update, name='agent_update'),
]
