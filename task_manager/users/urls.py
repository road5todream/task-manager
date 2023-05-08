from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('create/', views.RegisterUser.as_view(), name='create_user'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(),
         name='update_user'),
    path('<int:pk>/delete/', views.DeleteUserView.as_view(),
         name='delete_user'),
]
