from django.urls import path
from . import views
from .models import Tasks


urlpatterns = [
    path('', views.TasksFilterView.as_view(model=Tasks), name='tasks'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/', views.TaskView.as_view(), name='view_task'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(),
         name='update_task'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(),
         name='delete_task'),

]
