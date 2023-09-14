
from django.urls import path

from . import views

urlpatterns = [
    
    #system
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("darkmode", views.darkmode, name="darkmode"),
    
    #todo applet
    path("todo", views.todo, name="todo"),
    path("todo/completed", views.todo_completed, name="todo-completed"),
    path("todo/<int:task_id>", views.task, name="task"),

    #time applet
    path("time", views.time, name="time"),
    path("time/alarm", views.alarms, name="alarms"),
    path("time/alarm/<int:alarm_id>", views.alarm, name="alarm"),

    #links applet
    path("links", views.links, name="links"),
    path("links/<int:link_id>", views.link, name="link"),
    path("links/pinned", views.pinned, name="pinned"),

    #progress applet
    path("progress", views.progress, name="progress"),
]
