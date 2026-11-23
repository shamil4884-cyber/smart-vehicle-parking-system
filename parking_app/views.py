from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Mall, Complaint, Slot, Vehicle
@ensure_csrf_cookie
def home_view(request):
    # If logged in, redirect to respective dashboard
    if request.user.is_authenticated:
        try:
            role = request.user.profile.role
            if role == 'admin':
                return redirect('admin_dashboard')
            elif role == 'mall':
                return redirect('mall_dashboard')
            else:
                return redirect('user_dashboard')
        except UserProfile.DoesNotExist:
            pass
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        role = request.POST.get('role', 'user') # default role is 'user'

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Choose another.")
            return render(request, 'register.html')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        # Create user profile
        UserProfile.objects.create(user=user, full_name=full_name, mobile_number=mobile_number, role=role)
        
        # If it's a mall owner, create an initial mall entry automatically
        if role == 'mall':
            Mall.objects.create(
                owner=user.profile,
                mall_name=f"{full_name}'s Mall",
                location="Kozhikode",
                city="Calicut",
                contact_number=mobile_number
            )
            
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                role = user.profile.role
                if role == 'admin':
                    return redirect('admin_dashboard')
                elif role == 'mall':
                    return redirect('mall_dashboard')
                else:
                    return redirect('user_dashboard')
            except UserProfile.DoesNotExist:
                # Default role fallback
                UserProfile.objects.create(user=user, full_name=user.username, mobile_number="", role="user")
                return redirect('user_dashboard')
        else:
            context = {
                'm': "Username or password incorrect. Please try again."
            }
            return render(request, 'login.html', context)
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def user_dashboard(request):
    # Ensure role is user
    if request.user.profile.role != 'user':
        return redirect('home')
        
    malls = Mall.objects.all()
    # Get slot status for Lulu Mall (assume it's the first slot entry with slno=1)
    slot_status, created = Slot.objects.get_or_create(slno='1', defaults={'a': '0', 'b': '0', 'c': '0', 'd': '0'})
    
    # Get user's complaints
    complaints = Complaint.objects.filter(user=request.user.profile).order_by('-created_at')
    
    # Get vehicle logs for this user if plate matches user. We assume a sample plate KL22 for demo
    vehicle_logs = Vehicle.objects.all().order_by('-id')[:5]

    context = {
        'malls': malls,
        'slots': slot_status,
        'complaints': complaints,
        'vehicle_logs': vehicle_logs,
    }
    return render(request, 'user.html', context)

@login_required
def admin_dashboard(request):
    # Ensure role is admin
    if request.user.profile.role != 'admin':
        return redirect('home')
        
    # Get stats
    total_users = UserProfile.objects.filter(role='user').count()
    total_malls = Mall.objects.count()
    
    # Get complaints to display or forward
    complaints = Complaint.objects.all().order_by('-created_at')
    
    context = {
        'total_users': total_users,
        'total_malls': total_malls,
        'complaints': complaints,
    }
    return render(request, 'admin.html', context)

@login_required
def mall_dashboard(request):
    # Ensure role is mall
    if request.user.profile.role != 'mall':
        return redirect('home')
        
    # Find mall associated with this owner
    mall = Mall.objects.filter(owner=request.user.profile).first()
    
    # Get live slot status
    slot_status, created = Slot.objects.get_or_create(slno='1', defaults={'a': '0', 'b': '0', 'c': '0', 'd': '0'})
    
    # Get vehicle entrance logs
    vehicle_logs = Vehicle.objects.all().order_by('-id')[:10]
    
    # Get complaints forwarded to this mall or general complaints
    complaints = Complaint.objects.filter(is_forwarded=True).order_by('-created_at')
    
    context = {
        'mall': mall,
        'slots': slot_status,
        'vehicle_logs': vehicle_logs,
        'complaints': complaints,
    }
    return render(request, 'mall.html', context)

@login_required
def user_mange(request):
    # Manage Users view for Admin
    if request.user.profile.role != 'admin':
        return redirect('home')
    users = UserProfile.objects.filter(role='user')
    context = {
        'dd': users
    }
    return render(request, 'user_mange.html', context)

@login_required
def mange_malls(request):
    # Manage Malls view for Admin (displays list of malls)
    if request.user.profile.role != 'admin':
        return redirect('home')
        
    if request.method == 'POST':
        mall_name = request.POST.get('mall_name')
        location = request.POST.get('location')
        city = request.POST.get('city')
        contact_number = request.POST.get('contact_number')
        
        Mall.objects.create(
            mall_name=mall_name,
            location=location,
            city=city,
            contact_number=contact_number
        )
        return redirect('mange_malls')

    malls = Mall.objects.all()
    context = {
        'malls': malls
    }
    return render(request, 'mange_malls.html', context)

@login_required
def post_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Feedback')
        text = request.POST.get('message')
        mall_id = request.POST.get('mall_id')
        
        mall = None
        if mall_id:
            try:
                mall = Mall.objects.get(id=mall_id)
            except Mall.DoesNotExist:
                pass
                
        Complaint.objects.create(
            user=request.user.profile,
            mall=mall,
            title=title,
            text=text
        )
        messages.success(request, "Complaint/Feedback submitted successfully!")
        
    return redirect('user_dashboard')

@login_required
def forward_complaint(request, complaint_id):
    if request.user.profile.role != 'admin':
        return redirect('home')
        
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.is_forwarded = True
    complaint.save()
    messages.success(request, f"Complaint forwarded to Mall.")
    return redirect('admin_dashboard')

@login_required
def post_reply(request, complaint_id):
    if request.user.profile.role != 'mall':
        return redirect('home')
        
    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.reply = reply_text
        complaint.save()
        messages.success(request, "Reply posted successfully!")
        
    return redirect('mall_dashboard')


import json
import os
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

@require_POST
def chatbot_response(request):
    try:
        if request.content_type == "application/json":
            data = json.loads(request.body)
            message = str(data.get("message", "")).strip()
        else:
            message = request.POST.get("message", "").strip()

        if not message:
            return JsonResponse({"response": "Please enter a message."})

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return JsonResponse(
                {"response": "AI service is not configured."},
                status=503
            )

        from google import genai
        client = genai.Client(api_key=api_key)

        result = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=(
                "You are the Smart Parking System website assistant. "
                "Help users with parking, registration, login, "
                "slot availability and website navigation. "
                "Do not invent live parking availability.\n\n"
                f"User: {message}"
            )
        )

        return JsonResponse({
            "response": result.text or "No response generated."
        })

    except Exception:
        logger.exception("Gemini chatbot failed")
        return JsonResponse(
            {"response": "AI service is temporarily unavailable."},
            status=503
        )