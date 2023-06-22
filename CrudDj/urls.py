
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
    path('decano_menu/', views.decano_menu, name='decano_menu'),
    path('coordinador_menu/', views.coordinador_menu, name='coordinador_menu'),
    path('tasks/create/',views.create_task,name='create_tasks'),
    path('tasks/<int:task_id>/',views.task_detail,name='tasks_detail'),
    path('tasks/<int:task_id>/complete',views.complete_task,name='tasks_Complete'),
    path('tasks/<int:task_id>/delete',views.delete_task,name='tasks_delete'),
    path('logout/',views.signout,name='logout'),
    path('signin/',views.signin,name='signin'),
    path('evaluacion/', views.evaluacion_view, name='evaluacion'),
    path('labor/', views.labor_view, name='labor'),
    path('accion_labor/', views.labor_registrar, name='accion_labor'),
    path('gestionar_evaluacion/', views.gestionar_Eva_view, name='gestionar_evaluacion'),
    path('g_evaluaciones/', views.gestionar_eva, name='g_evaluaciones'),
    path('registrar-periodo/', views.periodo_view, name='periodo'),
    path('accion_periodo/', views.gestionar_periodo, name='accion_periodo'),
    path('eva_doc/', views.gestionar_eva_doc, name='eva_doc'),
    path('rol_view/', views.rol_view, name='rol_view'),
    path('accion_rol/', views.gestionar_user_rol, name='accion_rol'),
    
]
 