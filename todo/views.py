from django.shortcuts import render, redirect , get_object_or_404
from .models import Task
from .forms import TaskForm
from django.core.paginator import Paginator 
# Create the views here

def task_list(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/todo')
    
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})

def delete_task(request, id):
    task = get_object_or_404(Task, id= id)
    task.delete()
    return redirect('/todo')

def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    tasks = Task.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/todo')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_list.html', {'form': form, 'tasks':tasks, 'editing': True})