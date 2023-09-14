from curses.ascii import HT
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from .models import User, ToDo, Alarm, Link
from .forms import NewTaskForm, AlarmForm, NewLinkForm
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
    if request.user.is_authenticated: 
        return render(request, "dashboard/index.html", {
            "todo":ToDo.objects.filter(completed=False, user=request.user.id).order_by("-date")[:6],
            "alarms": Alarm.objects.filter(user=request.user).order_by('expired', 'date_time')[:4],
        })
    else:
        return render(request,"dashboard/no_user.html")

def login_view(request):
    if request.method == "POST":
        #Sign In
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #Authenticate
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "dashboard/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "dashboard/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "dashboard/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "dashboard/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "dashboard/register.html")

@login_required
def todo(request):
    if request.method == 'PUT':
        task_id = request.task_id
        status = request.completed
        if status:
            task = ToDo.objects.get(pk=task_id)
            if request.user == task.user:
                task.completed = True
                task.save()
        return HttpResponse("Done")
    elif request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            action = form.cleaned_data["action"]
            todo = ToDo(user = request.user, name = name, action = action)
            todo.save()
            return HttpResponseRedirect(reverse('todo'))
    return render(request, "dashboard/todo.html", {
        "todo": ToDo.objects.order_by("-date").filter(completed=False, user=request.user.id),
        "form": NewTaskForm(),
    })

@login_required
def todo_completed(request):
    return render(request, "dashboard/todo-completed.html", {
        "todo": ToDo.objects.order_by("-date").filter(completed=True, user=request.user.id),
        "form": NewTaskForm(),
    })

@login_required
@csrf_exempt
def task(request, task_id):
    task = ToDo.objects.get(pk = task_id)
    if request.user == task.user:
        if request.method == 'DELETE':
            task.delete()
        elif request.method == "PUT":
            task.completed = not task.completed
            task.save()
        elif request.method == "POST":
            data = json.loads(request.body)
            task.name = data.get("name", "")
            task.action = data.get("action", "")
            task.save()
    return HttpResponse("Works")

@login_required
@csrf_exempt
def time(request):
    if request.method == 'PUT':
        user = request.user
        user.stopstart += 1
        user.save()
        return HttpResponse(request.user.stopstart)
    return render(request, "dashboard/time.html", {
        'form' : AlarmForm(),
        "alarms": Alarm.objects.filter(user=request.user).order_by('expired', 'date_time'),
    })

@login_required
def alarms(request):
    if request.method == 'POST':
        form = AlarmForm(request.POST)
        if form.is_valid():
            user = request.user
            date_time = form.cleaned_data["date"]
            name = form.cleaned_data["name"]
            alarm = Alarm(user = user, date_time = date_time, name=name)
            alarm.save()
            return HttpResponseRedirect(reverse("time"))
    else:
        alarms = Alarm.objects.filter(user = request.user.id).order_by('date_time')
        return JsonResponse([alarm.serialize() for alarm in alarms], safe=False)

@csrf_exempt
@login_required
def alarm(request, alarm_id):
    alarm = Alarm.objects.get(pk = alarm_id)
    if request.user == alarm.user:
        if request.method == 'DELETE':
            alarm.delete()
        elif request.method == 'PUT':
            alarm.expired = True
            alarm.save()
    return HttpResponse("Done")

@login_required
@csrf_exempt
def darkmode(request):
    if request.method == 'PUT':
        user = request.user
        state = user.darkmode
        user.darkmode = not state
        user.save()
    return HttpResponse(request.user.darkmode)

@login_required
def progress(request):
    allTasks = ToDo.objects.filter(user = request.user.id).count()
    completedTasks = ToDo.objects.filter(user = request.user.id, completed = True).count()

    activeAlarms = Alarm.objects.filter(user = request.user.id, expired = False).count()
    allAlarms = Alarm.objects.filter(user = request.user.id).count()

    pinnedLinks = Link.objects.filter(user = request.user.id, pinned = True).count()
    allLinks = Link.objects.filter(user = request.user.id).count()

    if completedTasks != 0:
        tasks_percentage = str(f"{completedTasks/allTasks*100:.0f}")
    else:
        tasks_percentage = "0"

    return render(request, "dashboard/progress.html", {
        #tasks
        'tasks_percentage' : tasks_percentage,
        'completedTasks' : completedTasks,
        'allTasks' : allTasks,
        #time
        'activeAlarms' : activeAlarms,
        'allAlarms' : allAlarms,
        'stop_count' : request.user.stopstart,
        #links
        'pinnedLinks' : pinnedLinks,
        'allLinks' : allLinks,
    })

@login_required
def links(request):
    if request.method == 'POST':
        form = NewLinkForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            link = form.cleaned_data["link"]
            image = form.cleaned_data["image"]
            linkObject = Link(user = request.user, name = name, link=link, image=image)
            linkObject.save()
            return HttpResponseRedirect(reverse("links"))
    return render(request, "dashboard/links.html", {
        "links": Link.objects.order_by("-date").filter(user=request.user.id),
        "form": NewLinkForm(),
    })

@csrf_exempt
@login_required
def link(request, link_id):
    link = Link.objects.get(pk = link_id)
    if request.user == link.user:
        if request.method == 'DELETE':
            link.delete()
        elif request.method == "POST":
            link.pinned = not link.pinned
            link.save()
            return HttpResponseRedirect(reverse("links"))
    return HttpResponse(request.method)

@csrf_exempt
@login_required
def pinned(request):
    links = Link.objects.filter(user = request.user, pinned = True).order_by('date')[:5]
    return JsonResponse([link.serialize() for link in links], safe=False)
