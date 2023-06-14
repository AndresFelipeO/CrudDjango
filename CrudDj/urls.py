
from django.contrib import admin
from django.urls import path
from tasks import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signup,name='signup'),
    path('tasks/',views.tasks,name='tasks'),
    path('tasks/completed/',views.tasks_completed,name='tasks_completed'),
    path('docente_menu/', views.docente_menu, name='docente_menu'),
    path('tasks/create/',views.create_task,name='create_tasks'),
    path('tasks/<int:task_id>/',views.task_detail,name='tasks_detail'),
    path('tasks/<int:task_id>/complete',views.complete_task,name='tasks_Complete'),
    path('tasks/<int:task_id>/delete',views.delete_task,name='tasks_delete'),
    path('logout/',views.signout,name='logout'),
    path('signin/',views.signin,name='signin'),
    path('evaluacion/', views.evaluacion_view, name='evaluacion'),
]
