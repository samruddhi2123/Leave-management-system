from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SignupForm, LeaveForm
from .models import Leave

# Home
def home(request):
    return render(request, "home.html")

# Signup
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("student_dashboard")
    return render(request, "login.html")

# Logout
def logout_view(request):
    logout(request)
    return redirect("home")

# Student Dashboard
@login_required
def student_dashboard(request):
    leaves = request.user.leaves.all()
    return render(request, "student_dashboard.html", {"leaves": leaves})

# Apply Leave
@login_required
def apply_leave(request):
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.student = request.user
            leave.save()
            return redirect("student_dashboard")
    else:
        form = LeaveForm()
    return render(request, "apply_leave.html", {"form": form})

# Admin Dashboard
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    leaves = Leave.objects.all().order_by("-applied_at")
    return render(request, "admin_dashboard.html", {"leaves": leaves})

# Update Status
@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_status(request, leave_id, status):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = status
    leave.save()
    return redirect("admin_dashboard")

# Create your views here.
