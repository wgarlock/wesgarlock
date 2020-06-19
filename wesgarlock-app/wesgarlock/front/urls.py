from django.urls import path

from . import views

context_patterns = [
    path('login/', views.LoginView.as_view(), name="front_login"),
    path('logout/', views.LogoutView.as_view(), name="front_logout"),
    path('password-reset', views.PasswordResetView.as_view(), name="front_password_reset"),
    path('api-password-reset-confirm', views.PasswordResetConfirmViewAPI.as_view(), name="front_password_reset_confirm_api"),
    path('message/', views.MessagePostView.as_view(), name="front_message_post")
]

urlpatterns = context_patterns + [
    path('password_change', views.PasswordChangeView.as_view(), name="front_password_change"),
    path('password_change/done', views.PasswordChangeDoneView.as_view(), name="front_password_change_done"),
    path('password-reset/done', views.PasswordResetDoneView.as_view(), name="front_password_reset_done"),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='front_password_reset_complete'),
]
