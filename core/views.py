from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import Note, Homework, Task
from .forms import UserRegistrationForm, NoteForm, HomeworkForm, TaskForm
from .services.youtube_service import search_youtube
from .services.wikipedia_service import search_wikipedia
from .services.dictionary_service import lookup_word
from .services.books_service import search_books


# ===================================================
# LANDING PAGE & AUTHENTICATION VIEWS
# ===================================================

def home(request):
    """Landing/Home page view for Student Study Portal."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


def register_user(request):
    """User registration view with automatic login upon success."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Student Study Portal, {user.username}! Your account was created successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below to create your account.")
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_user(request):
    """User login view with validation and redirection."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}! Login successful.")
                next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    """User logout view."""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('login')


# ===================================================
# DASHBOARD VIEW
# ===================================================

@login_required
def dashboard(request):
    """
    Central student dashboard displaying real-time summary statistics,
    recent notes, urgent homework, and pending tasks.
    """
    user = request.user
    
    # Calculate real-time statistics
    total_notes = Note.objects.filter(user=user).count()
    pending_homework = Homework.objects.filter(user=user, completed=False).count()
    completed_homework = Homework.objects.filter(user=user, completed=True).count()
    pending_tasks = Task.objects.filter(user=user, completed=False).count()
    completed_tasks = Task.objects.filter(user=user, completed=True).count()

    # Recent items
    recent_notes = Note.objects.filter(user=user)[:4]
    urgent_homework = Homework.objects.filter(user=user, completed=False).order_by('due_date')[:4]
    pending_todo_list = Task.objects.filter(user=user, completed=False)[:5]

    context = {
        'total_notes': total_notes,
        'pending_homework': pending_homework,
        'completed_homework': completed_homework,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'recent_notes': recent_notes,
        'urgent_homework': urgent_homework,
        'pending_todo_list': pending_todo_list,
        'today': timezone.now().date(),
    }
    return render(request, 'core/dashboard.html', context)


# ===================================================
# NOTES MANAGEMENT VIEWS
# ===================================================

@login_required
def notes_list(request):
    """View and search user notes."""
    query = request.GET.get('q', '').strip()
    subject_filter = request.GET.get('subject', '').strip()

    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(content__icontains=query)
        )

    if subject_filter:
        notes = notes.filter(subject__iexact=subject_filter)

    # Get list of unique subjects for filter dropdown
    subjects = Note.objects.filter(user=request.user).values_list('subject', flat=True).distinct()

    context = {
        'notes': notes,
        'query': query,
        'subject_filter': subject_filter,
        'subjects': subjects,
    }
    return render(request, 'core/notes_list.html', context)


@login_required
def notes_add(request):
    """Create a new study note."""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, f"Note '{note.title}' created successfully!")
            return redirect('notes')
        else:
            messages.error(request, "Please check the form and fix any errors.")
    else:
        form = NoteForm()

    return render(request, 'core/note_form.html', {'form': form, 'action': 'Add Note'})


@login_required
def notes_edit(request, id):
    """Edit an existing note belonging to the logged-in student."""
    note = get_object_or_404(Note, id=id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f"Note '{note.title}' updated successfully!")
            return redirect('notes')
        else:
            messages.error(request, "Please check the form and fix any errors.")
    else:
        form = NoteForm(instance=note)

    return render(request, 'core/note_form.html', {'form': form, 'note': note, 'action': 'Edit Note'})


@login_required
def notes_delete(request, id):
    """Delete a note belonging to the logged-in student."""
    note = get_object_or_404(Note, id=id, user=request.user)

    if request.method == 'POST':
        title = note.title
        note.delete()
        messages.success(request, f"Note '{title}' deleted successfully!")
        return redirect('notes')

    return render(request, 'core/note_confirm_delete.html', {'note': note})


# ===================================================
# HOMEWORK MANAGEMENT VIEWS
# ===================================================

@login_required
def homework_list(request):
    """View homework separated into pending and completed assignments."""
    query = request.GET.get('q', '').strip()
    
    homeworks = Homework.objects.filter(user=request.user)

    if query:
        homeworks = homeworks.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(description__icontains=query)
        )

    pending_homeworks = homeworks.filter(completed=False)
    completed_homeworks = homeworks.filter(completed=True)

    context = {
        'pending_homeworks': pending_homeworks,
        'completed_homeworks': completed_homeworks,
        'query': query,
        'today': timezone.now().date(),
    }
    return render(request, 'core/homework_list.html', context)


@login_required
def homework_add(request):
    """Create a new homework assignment."""
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            hw = form.save(commit=False)
            hw.user = request.user
            hw.save()
            messages.success(request, f"Homework '{hw.title}' added successfully!")
            return redirect('homework')
        else:
            messages.error(request, "Please check the form and fix any errors.")
    else:
        form = HomeworkForm(initial={'due_date': timezone.now().date()})

    return render(request, 'core/homework_form.html', {'form': form, 'action': 'Add Homework'})


@login_required
def homework_edit(request, id):
    """Edit an existing homework assignment."""
    hw = get_object_or_404(Homework, id=id, user=request.user)

    if request.method == 'POST':
        form = HomeworkForm(request.POST, instance=hw)
        if form.is_valid():
            form.save()
            messages.success(request, f"Homework '{hw.title}' updated successfully!")
            return redirect('homework')
        else:
            messages.error(request, "Please check the form and fix any errors.")
    else:
        form = HomeworkForm(instance=hw)

    return render(request, 'core/homework_form.html', {'form': form, 'homework': hw, 'action': 'Edit Homework'})


@login_required
def homework_toggle(request, id):
    """Toggle homework completion status."""
    hw = get_object_or_404(Homework, id=id, user=request.user)
    hw.completed = not hw.completed
    hw.save()
    status_str = "completed" if hw.completed else "marked as pending"
    messages.success(request, f"Homework '{hw.title}' {status_str}!")
    return redirect('homework')


@login_required
def homework_delete(request, id):
    """Delete a homework assignment."""
    hw = get_object_or_404(Homework, id=id, user=request.user)

    if request.method == 'POST':
        title = hw.title
        hw.delete()
        messages.success(request, f"Homework '{title}' deleted successfully!")
        return redirect('homework')

    return render(request, 'core/homework_confirm_delete.html', {'homework': hw})


# ===================================================
# TO-DO LIST MANAGEMENT VIEWS
# ===================================================

@login_required
def todo_list(request):
    """View daily study tasks and to-do items."""
    pending_tasks = Task.objects.filter(user=request.user, completed=False)
    completed_tasks = Task.objects.filter(user=request.user, completed=True)

    context = {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'today': timezone.now().date(),
    }
    return render(request, 'core/todo_list.html', context)


@login_required
def todo_add(request):
    """Add a new study task."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' added successfully!")
            return redirect('todo')
        else:
            messages.error(request, "Please check the form and fix any errors.")
    else:
        form = TaskForm()

    return render(request, 'core/todo_form.html', {'form': form, 'action': 'Add Task'})


@login_required
def todo_edit(request, id):
    """Edit an existing study task."""
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully!")
            return redirect('todo')
        else:
            messages.error(request, "Please check the form and fix any errors.")
    else:
        form = TaskForm(instance=task)

    return render(request, 'core/todo_form.html', {'form': form, 'task': task, 'action': 'Edit Task'})


@login_required
def todo_toggle(request, id):
    """Toggle task completion status."""
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    status_str = "completed" if task.completed else "marked as pending"
    messages.success(request, f"Task '{task.title}' {status_str}!")
    return redirect('todo')


@login_required
def todo_delete(request, id):
    """Delete a task."""
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f"Task '{title}' deleted successfully!")
        return redirect('todo')

    return render(request, 'core/todo_confirm_delete.html', {'task': task})


# ===================================================
# STUDY TOOLS & EXTERNAL API VIEWS
# ===================================================

@login_required
def youtube_search_view(request):
    """YouTube Educational Video Search view."""
    query = request.GET.get('q', '').strip()
    result_data = None

    if query:
        result_data = search_youtube(query)

    context = {
        'query': query,
        'result_data': result_data,
    }
    return render(request, 'core/youtube.html', context)


@login_required
def wikipedia_search_view(request):
    """Wikipedia concept and topic search view."""
    query = request.GET.get('q', '').strip()
    result_data = None

    if query:
        result_data = search_wikipedia(query)

    context = {
        'query': query,
        'result_data': result_data,
    }
    return render(request, 'core/wikipedia.html', context)


@login_required
def dictionary_view(request):
    """English dictionary lookup view."""
    word = request.GET.get('q', '').strip()
    result_data = None

    if word:
        result_data = lookup_word(word)

    context = {
        'word': word,
        'result_data': result_data,
    }
    return render(request, 'core/dictionary.html', context)


@login_required
def books_search_view(request):
    """Google Books academic book search view."""
    query = request.GET.get('q', '').strip()
    result_data = None

    if query:
        result_data = search_books(query)

    context = {
        'query': query,
        'result_data': result_data,
    }
    return render(request, 'core/books.html', context)


@login_required
def unit_converter_view(request):
    """
    Unit converter view supporting Length, Weight, Temperature, Area, and Volume.
    Provides backend Python calculation handling and template context.
    """
    category = request.GET.get('category', 'length')
    input_value = request.GET.get('input_value', '')
    from_unit = request.GET.get('from_unit', '')
    to_unit = request.GET.get('to_unit', '')
    result = None
    error = None

    # Conversion tables relative to base units
    # Base units: length (meter), weight (gram), area (square meter), volume (liter)
    CONVERSIONS = {
        'length': {
            'meter': 1.0,
            'kilometer': 1000.0,
            'centimeter': 0.01,
            'millimeter': 0.001,
            'mile': 1609.344,
            'foot': 0.3048,
            'inch': 0.0254,
        },
        'weight': {
            'gram': 1.0,
            'kilogram': 1000.0,
            'milligram': 0.001,
            'pound': 453.59237,
            'ounce': 28.34952,
        },
        'area': {
            'square meter': 1.0,
            'square kilometer': 1000000.0,
            'square foot': 0.092903,
            'square inch': 0.00064516,
            'acre': 4046.86,
        },
        'volume': {
            'liter': 1.0,
            'milliliter': 0.001,
            'cubic meter': 1000.0,
            'gallon (US)': 3.78541,
        }
    }

    if input_value and from_unit and to_unit:
        try:
            val = float(input_value)
            if category == 'temperature':
                # Temperature conversion
                if from_unit == to_unit:
                    res = val
                elif from_unit == 'celsius' and to_unit == 'fahrenheit':
                    res = (val * 9/5) + 32
                elif from_unit == 'celsius' and to_unit == 'kelvin':
                    res = val + 273.15
                elif from_unit == 'fahrenheit' and to_unit == 'celsius':
                    res = (val - 32) * 5/9
                elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
                    res = (val - 32) * 5/9 + 273.15
                elif from_unit == 'kelvin' and to_unit == 'celsius':
                    res = val - 273.15
                elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
                    res = (val - 273.15) * 9/5 + 32
                else:
                    res = val
                result = round(res, 6)
            elif category in CONVERSIONS:
                table = CONVERSIONS[category]
                if from_unit in table and to_unit in table:
                    # Convert from_unit to base unit, then base unit to to_unit
                    base_val = val * table[from_unit]
                    converted_val = base_val / table[to_unit]
                    result = round(converted_val, 6)
                else:
                    error = "Selected unit not found in conversion category."
        except ValueError:
            error = "Please enter a valid numeric value to convert."

    context = {
        'category': category,
        'input_value': input_value,
        'from_unit': from_unit,
        'to_unit': to_unit,
        'result': result,
        'error': error,
    }
    return render(request, 'core/unit_converter.html', context)
