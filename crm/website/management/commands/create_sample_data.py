from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from website.models import Contact, Company, Deal, Task, Activity
from datetime import datetime, timedelta
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Create sample data for the CRM system'

    def handle(self, *args, **options):
        # Create sample users
        if not User.objects.filter(username='sales_user').exists():
            sales_user = User.objects.create_user(
                username='sales_user',
                email='sales@example.com',
                password='password123',
                first_name='Sales',
                last_name='User'
            )
            
        if not User.objects.filter(username='manager').exists():
            manager = User.objects.create_user(
                username='manager',
                email='manager@example.com',
                password='password123',
                first_name='Sales',
                last_name='Manager'
            )
        
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin2',
                email='admin2@example.com',
                password='admin123'
            )
        
        # Create sample companies
        companies_data = [
            {
                'name': 'TechCorp Industries',
                'industry': 'Technology',
                'company_type': 'prospect',
                'website': 'https://techcorp.example.com',
                'description': 'Leading technology solutions provider'
            },
            {
                'name': 'Global Manufacturing Co',
                'industry': 'Manufacturing',
                'company_type': 'customer',
                'website': 'https://globalmfg.example.com',
                'description': 'Large manufacturing company'
            },
            {
                'name': 'StartupXYZ',
                'industry': 'Software',
                'company_type': 'prospect',
                'website': 'https://startupxyz.example.com',
                'description': 'Innovative startup in AI space'
            }
        ]
        
        for company_data in companies_data:
            if not Company.objects.filter(name=company_data['name']).exists():
                Company.objects.create(
                    created_by=admin_user,
                    **company_data
                )
        
        # Create sample contacts
        contacts_data = [
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john.smith@techcorp.example.com',
                'phone': '+1-555-123-4567',
                'company': 'TechCorp Industries',
                'job_title': 'CTO',
                'contact_type': 'lead',
                'lead_status': 'qualified'
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah.j@globalmfg.example.com',
                'phone': '+1-555-234-5678',
                'company': 'Global Manufacturing Co',
                'job_title': 'Procurement Manager',
                'contact_type': 'customer',
                'lead_status': 'converted'
            },
            {
                'first_name': 'Mike',
                'last_name': 'Davis',
                'email': 'mike@startupxyz.example.com',
                'phone': '+1-555-345-6789',
                'company': 'StartupXYZ',
                'job_title': 'CEO',
                'contact_type': 'lead',
                'lead_status': 'contacted'
            },
            {
                'first_name': 'Emily',
                'last_name': 'Brown',
                'email': 'emily.brown@example.com',
                'phone': '+1-555-456-7890',
                'company': 'FreelanceConsulting',
                'job_title': 'Consultant',
                'contact_type': 'prospect',
                'lead_status': 'new'
            }
        ]
        
        for contact_data in contacts_data:
            if not Contact.objects.filter(email=contact_data['email']).exists():
                Contact.objects.create(
                    created_by=admin_user,
                    **contact_data
                )
        
        # Create sample deals
        contacts = Contact.objects.all()
        companies = Company.objects.all()
        
        deals_data = [
            {
                'title': 'Enterprise Software License',
                'description': 'Annual software license for enterprise solution',
                'amount': 50000.00,
                'stage': 'negotiation',
                'probability': 75,
                'expected_close_date': timezone.now().date() + timedelta(days=30)
            },
            {
                'title': 'Manufacturing Equipment',
                'description': 'Custom manufacturing equipment order',
                'amount': 125000.00,
                'stage': 'proposal',
                'probability': 60,
                'expected_close_date': timezone.now().date() + timedelta(days=45)
            },
            {
                'title': 'Consulting Services',
                'description': 'IT consulting services for digital transformation',
                'amount': 25000.00,
                'stage': 'qualification',
                'probability': 40,
                'expected_close_date': timezone.now().date() + timedelta(days=60)
            }
        ]
        
        if contacts and companies:
            for i, deal_data in enumerate(deals_data):
                if not Deal.objects.filter(title=deal_data['title']).exists():
                    Deal.objects.create(
                        contact=contacts[i % len(contacts)],
                        company=companies[i % len(companies)] if i < len(companies) else None,
                        created_by=admin_user,
                        **deal_data
                    )
        
        # Create sample tasks
        deals = Deal.objects.all()
        task_data = [
            {
                'title': 'Follow up call with John Smith',
                'description': 'Discuss pricing and implementation timeline',
                'task_type': 'call',
                'priority': 'high',
                'due_date': timezone.now() + timedelta(days=1),
                'assigned_to': admin_user
            },
            {
                'title': 'Prepare proposal document',
                'description': 'Create detailed proposal for manufacturing equipment',
                'task_type': 'other',
                'priority': 'medium',
                'due_date': timezone.now() + timedelta(days=5),
                'assigned_to': admin_user
            },
            {
                'title': 'Schedule demo meeting',
                'description': 'Schedule product demo with startup team',
                'task_type': 'meeting',
                'priority': 'medium',
                'due_date': timezone.now() + timedelta(days=3),
                'assigned_to': admin_user
            }
        ]
        
        if contacts and deals:
            for i, task in enumerate(task_data):
                if not Task.objects.filter(title=task['title']).exists():
                    Task.objects.create(
                        contact=contacts[i % len(contacts)],
                        deal=deals[i % len(deals)] if i < len(deals) else None,
                        created_by=admin_user,
                        **task
                    )
        
        # Create some activities
        for contact in contacts[:3]:
            Activity.objects.create(
                activity_type='contact',
                title=f'Contact created: {contact.full_name}',
                contact=contact,
                created_by=admin_user
            )
        
        for deal in deals[:2]:
            Activity.objects.create(
                activity_type='deal',
                title=f'Deal created: {deal.title}',
                deal=deal,
                contact=deal.contact,
                created_by=admin_user
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data for CRM system!')
        )