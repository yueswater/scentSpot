from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfume, User, UsageLog

def login_view(request):
    """登入頁面"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            
            # If there is next parameter, direct to this page
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def register_view(request):
    """註冊頁面"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Verify password
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        
        # Check password strength
        if len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'register.html')
        
        # Check if the username already exists
        if AuthUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')
        
        # Check if Email already exists
        if AuthUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')
        
        # Create user (password will be hashed automatically)
        try:
            auth_user = AuthUser.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            auth_user.save()
            
            # Also create a User (staff) record
            User.objects.create(
                name=username,
                auth_user=auth_user
            )
            
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'register.html')


def logout_view(request):
    """登出"""
    username = request.user.username if request.user.is_authenticated else None
    logout(request)
    
    if username:
        messages.success(request, f'Goodbye, {username}! You have been logged out.')
    
    return redirect('/')

def home(request):
    """首頁 - 不需要登入"""
    return render(request, 'home.html')

@login_required(login_url='login')
def record_usage(request):
    """記錄香水使用 - 需要登入"""
    
    # 嘗試找到當前登入使用者對應的 User (staff) 記錄
    try:
        current_staff_user = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        # 如果找不到，自動建立一個
        current_staff_user = User.objects.create(
            name=request.user.username,
            auth_user=request.user
        )
        messages.info(request, f'Staff profile created for {request.user.username}')
    
    if request.method == "POST":
        gender = request.POST.get("gender")
        perfume_id = request.POST.get("perfume")

        # Validate inputs
        if not perfume_id:
            messages.error(request, 'Please select a perfume.')
            return redirect("record_usage")

        try:
            perfume = Perfume.objects.get(id=perfume_id)
            
            # 使用當前登入使用者的 User 記錄
            UsageLog.objects.create(
                gender=gender,
                perfume=perfume,
                user=current_staff_user,  # 自動使用當前登入使用者
            )
            
            messages.success(
                request, 
                f'Successfully recorded {perfume.brand} - {perfume.name}!'
            )
        except Perfume.DoesNotExist:
            messages.error(request, 'Selected perfume does not exist.')
        except Exception as e:
            messages.error(request, f'Error recording usage: {str(e)}')

        return redirect("record_usage")

    # GET request - show form
    perfumes = Perfume.objects.all().order_by("brand", "name")

    return render(request, "record_usage.html", {
        "perfumes": perfumes,
        "current_user": current_staff_user,  # 傳遞當前使用者
    })


@login_required(login_url='login')
def today_logs(request):
    """今日使用記錄 - 需要登入"""
    # Today's date
    today = timezone.localtime().date()

    logs = UsageLog.objects.filter(
        used_at__date=today
    ).select_related('perfume', 'user')

    # Gender statistics
    count_gender = logs.values('gender').annotate(count=Count('id'))

    # Perfume usage ranking
    count_perfume = logs.values('perfume__brand', 'perfume__name').annotate(
        count=Count('id')
    ).order_by('-count')

    return render(request, 'today.html', {
        'logs': logs,
        'count_gender': count_gender,
        'count_perfume': count_perfume,
        'today': today,
    })


@login_required(login_url='login')
def all_logs(request):
    """所有使用記錄 - 需要登入"""
    logs = UsageLog.objects.select_related('perfume', 'user').order_by('-used_at')

    # Filters
    date = request.GET.get("date")
    perfume_id = request.GET.get("perfume")
    gender = request.GET.get("gender")

    if date:
        logs = logs.filter(used_at__date=date)

    if perfume_id and perfume_id != "all":
        logs = logs.filter(perfume_id=perfume_id)

    if gender and gender != "all":
        logs = logs.filter(gender=gender)

    perfumes = Perfume.objects.all().order_by("brand", "name")

    return render(request, "logs.html", {
        "logs": logs,
        "perfumes": perfumes,
        "selected_date": date,
        "selected_perfume": perfume_id,
        "selected_gender": gender,
    })

@login_required(login_url='login')
def perfume_management(request):
    """香水管理頁面 - 顯示所有香水"""
    perfumes = Perfume.objects.all().order_by('-created_at')
    
    return render(request, 'perfume_management.html', {
        'perfumes': perfumes,
    })


@login_required(login_url='login')
def add_perfume(request):
    """新增香水"""
    if request.method == 'POST':
        brand = request.POST.get('brand')
        name = request.POST.get('name')
        capacity_ml = request.POST.get('capacity_ml')
        description = request.POST.get('description', '')
        image_url = request.POST.get('image_url', '')
        
        try:
            perfume = Perfume.objects.create(
                brand=brand,
                name=name,
                capacity_ml=capacity_ml,
                description=description if description else None,
                image_url=image_url if image_url else None
            )
            messages.success(request, f'Successfully added {brand} - {name}!')
        except Exception as e:
            messages.error(request, f'Error adding perfume: {str(e)}')
        
        return redirect('perfume_management')
    
    return redirect('perfume_management')


@login_required(login_url='login')
def edit_perfume(request, perfume_id):
    """編輯香水"""
    perfume = get_object_or_404(Perfume, id=perfume_id)
    
    if request.method == 'POST':
        perfume.brand = request.POST.get('brand')
        perfume.name = request.POST.get('name')
        perfume.capacity_ml = request.POST.get('capacity_ml')
        description = request.POST.get('description', '')
        image_url = request.POST.get('image_url', '')
        
        perfume.description = description if description else None
        perfume.image_url = image_url if image_url else None
        
        try:
            perfume.save()
            messages.success(request, f'Successfully updated {perfume.brand} - {perfume.name}!')
        except Exception as e:
            messages.error(request, f'Error updating perfume: {str(e)}')
    
    return redirect('perfume_management')


@login_required(login_url='login')
def delete_perfume(request, perfume_id):
    """刪除香水"""
    perfume = get_object_or_404(Perfume, id=perfume_id)
    
    if request.method == 'POST':
        perfume_name = f"{perfume.brand} - {perfume.name}"
        try:
            perfume.delete()
            messages.success(request, f'Successfully deleted {perfume_name}!')
        except Exception as e:
            messages.error(request, f'Error deleting perfume: {str(e)}')
    
    return redirect('perfume_management')