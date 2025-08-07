from django.shortcuts import render, redirect , get_object_or_404
from .models import Task
from .forms import TaskForm
from django.core.paginator import Paginator 
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import RegisterForm
# Create the views here

def task_list(request):

    if not request.user.is_authenticated:
        return redirect('login')
    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'incomplete':
        tasks = tasks.filter(completed=False)

    paginator = Paginator(tasks, 5)  # Show 5 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save (commit= False)
            task.user = request.user
            task.save()
            return redirect('/todo')
    
    return render(request, 'todo/task_list.html', {
        'tasks': tasks, 
        'form': form, 
        'page_obj': page_obj,
        'status': status,
        })

def delete_task(request, id):
    task = get_object_or_404(Task, id= id, user = request.user)
    task.delete()
    return redirect('/todo')

def edit_task(request, id):
    task = get_object_or_404(Task, id=id, user = request.user)
    tasks = Task.objects.filter(user= request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/todo')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_list.html', {'form': form, 'tasks':tasks, 'editing': True})

class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('task_list')
        return super().get(request, *args, **kwargs)
    
def register_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after successful registration
            return redirect('task_list')
    else:
        form = RegisterForm()
    
    return render(request, 'todo/register.html', {'form': form})
