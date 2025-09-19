from django.contrib import admin
from .models import Contact, Company, Deal, Task, Note, Activity

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'company', 'contact_type', 'lead_status', 'assigned_to', 'created_at']
    list_filter = ['contact_type', 'lead_status', 'assigned_to', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'company']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Details', {
            'fields': ('company', 'job_title', 'contact_type', 'lead_status')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'zip_code'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'company_type', 'employee_count', 'annual_revenue', 'created_by', 'created_at']
    list_filter = ['company_type', 'industry', 'created_at']
    search_fields = ['name', 'industry']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact', 'company', 'amount', 'stage', 'probability', 'expected_close_date', 'assigned_to', 'created_at']
    list_filter = ['stage', 'assigned_to', 'created_at', 'expected_close_date']
    search_fields = ['title', 'contact__first_name', 'contact__last_name', 'company__name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Deal Information', {
            'fields': ('title', 'description', 'contact', 'company')
        }),
        ('Financial Details', {
            'fields': ('amount', 'stage', 'probability')
        }),
        ('Timeline', {
            'fields': ('expected_close_date', 'actual_close_date')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task_type', 'priority', 'status', 'due_date', 'assigned_to', 'contact', 'deal', 'created_at']
    list_filter = ['task_type', 'priority', 'status', 'assigned_to', 'due_date', 'created_at']
    search_fields = ['title', 'description', 'contact__first_name', 'contact__last_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'task_type', 'priority', 'status')
        }),
        ('Timeline', {
            'fields': ('due_date', 'completed_date')
        }),
        ('Relations', {
            'fields': ('contact', 'deal')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact', 'deal', 'company', 'created_by', 'created_at']
    list_filter = ['created_by', 'created_at']
    search_fields = ['title', 'content', 'contact__first_name', 'contact__last_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'contact', 'deal', 'created_by', 'created_at']
    list_filter = ['activity_type', 'created_by', 'created_at']
    search_fields = ['title', 'description', 'contact__first_name', 'contact__last_name']
    list_per_page = 25
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        # Activities are usually created automatically, not manually
        return False
