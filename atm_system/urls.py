from django.urls import path

from .import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.test_transaction, name='test'),

    # path('change-pin/', views.change_pin_view, name='change_pin')

]
