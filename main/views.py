from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import User, Project, ProjectMember, Task
from .forms import CustomUserCreationForm, ProjectForm, TaskForm

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            if User.objects.count() == 0:
                user.role = 'admin'
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_tasks = Task.objects.filter(Q(assignee=request.user) | Q(project__members__user=request.user)).distinct()
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='completed').count()
    in_progress_tasks = user_tasks.filter(status='in-progress').count()
    todo_tasks = user_tasks.filter(status='todo').count()
    in_review_tasks = user_tasks.filter(status='in-review').count()
    overdue_tasks = user_tasks.filter(due_date__lt=timezone.now().date()).exclude(status='completed').count()

    active_projects = Project.objects.filter(members__user=request.user).annotate(
        total_project_tasks=Count('tasks'),
        completed_project_tasks=Count('tasks', filter=Q(tasks__status='completed'))
    ).distinct()[:4]
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'todo_tasks': todo_tasks,
        'in_review_tasks': in_review_tasks,
        'overdue_tasks': overdue_tasks,
        'active_projects': active_projects,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def project_list(request):
    projects = Project.objects.filter(members__user=request.user).distinct()
    return render(request, 'projects/list.html', {'projects': projects})

@login_required
def project_board(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'projects/board.html', {'project': project})

@login_required
def task_list(request):
    tasks = Task.objects.filter(Q(assignee=request.user) | Q(project__members__user=request.user)).distinct()
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
def team_list(request):
    members = User.objects.all()
    return render(request, 'team/list.html', {'members': members})
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            ProjectMember.objects.create(project=project, user=request.user, role='admin')
            messages.success(request, 'Project created successfully!')
            return redirect('project_list')
    return redirect('project_list')

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('project_board', id=project.id)
    return redirect('project_board', id=project.id)

@login_required
def task_update_status(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=id)
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def task_delete(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=id)
        task.delete()
        messages.success(request, 'Task deleted successfully!')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def team_update_role(request, id):
    if request.method == 'POST' and request.user.role == 'admin':
        user = get_object_or_404(User, id=id)
        new_role = request.POST.get('role')
        if new_role in dict(User._meta.get_field('role').choices):
            user.role = new_role
            user.save()
            messages.success(request, f'Role updated for {user.get_full_name()}')
    return redirect('team_list')

@login_required
def team_delete(request, id):
    if request.method == 'POST' and request.user.role == 'admin':
        user = get_object_or_404(User, id=id)
        if user != request.user:
            user.delete()
            messages.success(request, 'User removed successfully')
    return redirect('team_list')

