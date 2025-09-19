from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Contact, Company, Deal, Task, Note, Activity
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your views here.

def home(request):
    """Dashboard view showing key metrics and recent activities"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get key metrics
    total_contacts = Contact.objects.count()
    total_deals = Deal.objects.count()
    total_companies = Company.objects.count()
    
    # Recent activities
    recent_activities = Activity.objects.select_related('contact', 'deal', 'created_by')[:10]
    
    # Deals by stage
    deals_by_stage = Deal.objects.values('stage').annotate(count=Count('id'))
    
    # Revenue metrics
    won_deals = Deal.objects.filter(stage='closed_won')
    total_revenue = won_deals.aggregate(total=Sum('amount'))['total'] or 0
    
    # Overdue tasks
    overdue_tasks = Task.objects.filter(
        due_date__lt=timezone.now(),
        status__in=['pending', 'in_progress']
    ).count()
    
    context = {
        'total_contacts': total_contacts,
        'total_deals': total_deals,
        'total_companies': total_companies,
        'recent_activities': recent_activities,
        'deals_by_stage': deals_by_stage,
        'total_revenue': total_revenue,
        'overdue_tasks': overdue_tasks,
    }
    return render(request, 'dashboard.html', context)


def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def contact_list(request):
    """List all contacts with search and filtering"""
    contacts = Contact.objects.select_related('assigned_to', 'created_by').all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        contacts = contacts.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(company__icontains=search_query)
        )
    
    # Filter by contact type
    contact_type = request.GET.get('type')
    if contact_type:
        contacts = contacts.filter(contact_type=contact_type)
    
    # Filter by lead status
    lead_status = request.GET.get('status')
    if lead_status:
        contacts = contacts.filter(lead_status=lead_status)
    
    # Pagination
    paginator = Paginator(contacts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'contact_type': contact_type,
        'lead_status': lead_status,
        'contact_types': Contact.CONTACT_TYPE_CHOICES,
        'lead_statuses': Contact.LEAD_STATUS_CHOICES,
    }
    return render(request, 'contacts/list.html', context)


@login_required
def contact_detail(request, contact_id):
    """Contact detail view with related deals, tasks, and notes"""
    contact = get_object_or_404(Contact, id=contact_id)
    deals = contact.deals.all()
    tasks = contact.tasks.all()
    notes = contact.notes.all()
    activities = contact.activities.all()[:10]
    
    context = {
        'contact': contact,
        'deals': deals,
        'tasks': tasks,
        'notes': notes,
        'activities': activities,
    }
    return render(request, 'contacts/detail.html', context)


@login_required
def contact_create(request):
    """Create new contact"""
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        job_title = request.POST.get('job_title', '')
        contact_type = request.POST.get('contact_type', 'lead')
        lead_status = request.POST.get('lead_status', 'new')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        country = request.POST.get('country', '')
        zip_code = request.POST.get('zip_code', '')
        notes = request.POST.get('notes', '')
        
        # Create contact
        contact = Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            company=company,
            job_title=job_title,
            contact_type=contact_type,
            lead_status=lead_status,
            address=address,
            city=city,
            state=state,
            country=country,
            zip_code=zip_code,
            notes=notes,
            created_by=request.user
        )
        
        # Create activity
        Activity.objects.create(
            activity_type='contact',
            title=f'Contact created: {contact.full_name}',
            contact=contact,
            created_by=request.user
        )
        
        messages.success(request, f'Contact {contact.full_name} created successfully!')
        return redirect('contact_detail', contact_id=contact.id)
    
    context = {
        'contact_types': Contact.CONTACT_TYPE_CHOICES,
        'lead_statuses': Contact.LEAD_STATUS_CHOICES,
        'users': User.objects.all(),
    }
    return render(request, 'contacts/create.html', context)


@login_required
def contact_edit(request, contact_id):
    """Edit existing contact"""
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'POST':
        # Update contact fields
        contact.first_name = request.POST.get('first_name')
        contact.last_name = request.POST.get('last_name')
        contact.email = request.POST.get('email')
        contact.phone = request.POST.get('phone', '')
        contact.company = request.POST.get('company', '')
        contact.job_title = request.POST.get('job_title', '')
        contact.contact_type = request.POST.get('contact_type')
        contact.lead_status = request.POST.get('lead_status')
        contact.address = request.POST.get('address', '')
        contact.city = request.POST.get('city', '')
        contact.state = request.POST.get('state', '')
        contact.country = request.POST.get('country', '')
        contact.zip_code = request.POST.get('zip_code', '')
        contact.notes = request.POST.get('notes', '')
        
        assigned_to_id = request.POST.get('assigned_to')
        if assigned_to_id:
            contact.assigned_to = User.objects.get(id=assigned_to_id)
        else:
            contact.assigned_to = None
        
        contact.save()
        
        # Create activity
        Activity.objects.create(
            activity_type='contact',
            title=f'Contact updated: {contact.full_name}',
            contact=contact,
            created_by=request.user
        )
        
        messages.success(request, f'Contact {contact.full_name} updated successfully!')
        return redirect('contact_detail', contact_id=contact.id)
    
    context = {
        'contact': contact,
        'contact_types': Contact.CONTACT_TYPE_CHOICES,
        'lead_statuses': Contact.LEAD_STATUS_CHOICES,
        'users': User.objects.all(),
    }
    return render(request, 'contacts/edit.html', context)


@login_required
def deal_list(request):
    """List all deals with filtering and search"""
    deals = Deal.objects.select_related('contact', 'company', 'assigned_to').all()
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        deals = deals.filter(
            Q(title__icontains=search_query) |
            Q(contact__first_name__icontains=search_query) |
            Q(contact__last_name__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )
    
    # Filter by stage
    stage = request.GET.get('stage')
    if stage:
        deals = deals.filter(stage=stage)
    
    # Pagination
    paginator = Paginator(deals, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'stage': stage,
        'deal_stages': Deal.DEAL_STAGE_CHOICES,
    }
    return render(request, 'deals/list.html', context)


@login_required
def deal_detail(request, deal_id):
    """Deal detail view"""
    deal = get_object_or_404(Deal, id=deal_id)
    tasks = deal.tasks.all()
    notes = deal.notes.all()
    activities = deal.activities.all()[:10]
    
    context = {
        'deal': deal,
        'tasks': tasks,
        'notes': notes,
        'activities': activities,
    }
    return render(request, 'deals/detail.html', context)


@login_required
def deal_create(request):
    """Create new deal"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        contact_id = request.POST.get('contact')
        company_id = request.POST.get('company')
        amount = request.POST.get('amount')
        stage = request.POST.get('stage', 'prospecting')
        probability = request.POST.get('probability', 0)
        expected_close_date = request.POST.get('expected_close_date')
        
        contact = Contact.objects.get(id=contact_id)
        company = Company.objects.get(id=company_id) if company_id else None
        
        deal = Deal.objects.create(
            title=title,
            description=description,
            contact=contact,
            company=company,
            amount=amount,
            stage=stage,
            probability=probability,
            expected_close_date=expected_close_date,
            created_by=request.user
        )
        
        # Create activity
        Activity.objects.create(
            activity_type='deal',
            title=f'Deal created: {deal.title}',
            deal=deal,
            contact=contact,
            created_by=request.user
        )
        
        messages.success(request, f'Deal "{deal.title}" created successfully!')
        return redirect('deal_detail', deal_id=deal.id)
    
    context = {
        'contacts': Contact.objects.all(),
        'companies': Company.objects.all(),
        'deal_stages': Deal.DEAL_STAGE_CHOICES,
        'users': User.objects.all(),
    }
    return render(request, 'deals/create.html', context)


@login_required
def task_list(request):
    """List tasks with filtering"""
    tasks = Task.objects.select_related('contact', 'deal', 'assigned_to').all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    
    # Filter by assigned user
    if not request.user.is_superuser:
        tasks = tasks.filter(assigned_to=request.user)
    
    # Pagination
    paginator = Paginator(tasks, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status': status,
        'task_statuses': Task.STATUS_CHOICES,
    }
    return render(request, 'tasks/list.html', context)


@login_required
def task_create(request):
    """Create new task"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        task_type = request.POST.get('task_type', 'other')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date')
        contact_id = request.POST.get('contact')
        deal_id = request.POST.get('deal')
        assigned_to_id = request.POST.get('assigned_to')
        
        contact = Contact.objects.get(id=contact_id) if contact_id else None
        deal = Deal.objects.get(id=deal_id) if deal_id else None
        assigned_to = User.objects.get(id=assigned_to_id)
        
        task = Task.objects.create(
            title=title,
            description=description,
            task_type=task_type,
            priority=priority,
            due_date=due_date,
            contact=contact,
            deal=deal,
            assigned_to=assigned_to,
            created_by=request.user
        )
        
        # Create activity
        Activity.objects.create(
            activity_type='task',
            title=f'Task created: {task.title}',
            contact=contact,
            deal=deal,
            created_by=request.user
        )
        
        messages.success(request, f'Task "{task.title}" created successfully!')
        return redirect('task_list')
    
    context = {
        'contacts': Contact.objects.all(),
        'deals': Deal.objects.all(),
        'users': User.objects.all(),
        'task_types': Task.TASK_TYPE_CHOICES,
        'priorities': Task.PRIORITY_CHOICES,
    }
    return render(request, 'tasks/create.html', context)


@login_required
def company_list(request):
    """List companies"""
    companies = Company.objects.all()
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        companies = companies.filter(
            Q(name__icontains=search_query) |
            Q(industry__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(companies, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'companies/list.html', context)


@login_required
def company_create(request):
    """Create new company"""
    if request.method == 'POST':
        name = request.POST.get('name')
        website = request.POST.get('website', '')
        industry = request.POST.get('industry', '')
        company_type = request.POST.get('company_type', 'prospect')
        description = request.POST.get('description', '')
        
        company = Company.objects.create(
            name=name,
            website=website,
            industry=industry,
            company_type=company_type,
            description=description,
            created_by=request.user
        )
        
        messages.success(request, f'Company "{company.name}" created successfully!')
        return redirect('company_list')
    
    context = {
        'company_types': Company.COMPANY_TYPE_CHOICES,
    }
    return render(request, 'companies/create.html', context)


@login_required
def reports(request):
    """Reports and analytics view"""
    # Deal metrics
    total_deals = Deal.objects.count()
    won_deals = Deal.objects.filter(stage='closed_won').count()
    lost_deals = Deal.objects.filter(stage='closed_lost').count()
    
    # Revenue metrics
    total_revenue = Deal.objects.filter(stage='closed_won').aggregate(
        total=Sum('amount'))['total'] or 0
    
    # Lead conversion
    total_leads = Contact.objects.filter(contact_type='lead').count()
    converted_leads = Contact.objects.filter(
        contact_type='lead', lead_status='converted').count()
    conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    
    # Tasks by status
    tasks_by_status = Task.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'total_deals': total_deals,
        'won_deals': won_deals,
        'lost_deals': lost_deals,
        'total_revenue': total_revenue,
        'conversion_rate': conversion_rate,
        'tasks_by_status': tasks_by_status,
    }
    return render(request, 'reports.html', context)
