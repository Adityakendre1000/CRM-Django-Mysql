# CRM System - Django & MySQL

A comprehensive Customer Relationship Management (CRM) system built with Django and MySQL, featuring contact management, deal tracking, task management, and reporting capabilities.

## Features

### 📋 Core CRM Functionality
- **Contact Management**: Store and manage customer contact information, lead status, and contact types
- **Deal Pipeline**: Track sales opportunities through different stages with probability and revenue tracking
- **Task Management**: Create and assign tasks with priorities, due dates, and status tracking
- **Company Management**: Manage company information and relationships
- **Activity Tracking**: Automatic logging of user activities and interactions
- **Notes System**: Add notes to contacts, deals, and companies

### 🎯 Key Features
- **Dashboard**: Overview of key metrics, recent activities, and quick actions
- **Search & Filtering**: Advanced search and filtering across all modules
- **User Authentication**: Secure login/logout with user registration
- **Admin Interface**: Comprehensive Django admin interface for data management
- **Responsive Design**: Mobile-friendly Bootstrap-based UI
- **MySQL Integration**: Robust database backend with proper relationships

### 📊 Reports & Analytics
- Revenue tracking and deal pipeline analytics
- Lead conversion rate analysis
- Task status distribution
- Win/loss deal analysis
- Activity timeline and history

## Technology Stack

- **Backend**: Django 5.2.1
- **Database**: MySQL
- **Frontend**: Bootstrap 5, Font Awesome icons
- **Authentication**: Django built-in authentication
- **ORM**: Django ORM with MySQL connector

## Installation & Setup

### Prerequisites
- Python 3.10+
- MySQL Server
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CRM-Django-Mysql
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv virt
   # On Windows:
   .\virt\Scripts\Activate.ps1
   # On macOS/Linux:
   source virt/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django mysqlclient pillow
   ```

4. **Configure MySQL database**
   - Create a MySQL database named `elderco`
   - Update database credentials in `crm/settings.py` if needed:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'elderco',
           'USER': 'root',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Run migrations**
   ```bash
   cd crm
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Login with your superuser credentials
   - Access admin panel at `http://127.0.0.1:8000/admin/`

## Usage Guide

### Getting Started
1. **Login**: Use your credentials to access the CRM system
2. **Dashboard**: View key metrics and recent activities
3. **Add Contacts**: Start by adding your contacts and leads
4. **Create Companies**: Add company information for your business relationships
5. **Track Deals**: Create deals and track them through your sales pipeline
6. **Manage Tasks**: Create and assign tasks to team members
7. **Generate Reports**: View analytics and reports for insights

### Navigation
- **Dashboard**: Overview and quick actions
- **Contacts**: Manage all contacts and leads
- **Deals**: Track sales opportunities
- **Tasks**: Manage to-do items and follow-ups
- **Companies**: Company database
- **Reports**: Analytics and insights
- **Admin**: System administration

### Key Workflows

#### Adding a New Lead
1. Go to Contacts → Add Contact
2. Fill in contact information
3. Set contact type to "Lead"
4. Set lead status appropriately
5. Save and assign to a team member

#### Creating a Deal
1. Go to Deals → Add Deal
2. Select the contact and company
3. Enter deal amount and expected close date
4. Set appropriate stage and probability
5. Save and track progress

#### Managing Tasks
1. Go to Tasks → Add Task
2. Set priority and due date
3. Assign to team member
4. Link to relevant contact/deal
5. Track completion status

## Database Models

### Contact
- Personal information (name, email, phone)
- Professional details (company, job title)
- Contact type and lead status
- Address information
- Notes and assignment

### Company
- Company details (name, industry, website)
- Company type and size information
- Financial information (revenue, employees)
- Contact relationships

### Deal
- Deal information (title, description, amount)
- Stage and probability tracking
- Timeline (expected/actual close dates)
- Contact and company relationships

### Task
- Task details (title, description, type)
- Priority and status management
- Due dates and completion tracking
- Relationships to contacts and deals

### Activity
- Automatic activity logging
- User action tracking
- Timeline of interactions
- System audit trail

### Note
- Flexible note system
- Attachable to contacts, deals, companies
- User attribution and timestamps

## Admin Interface

The Django admin interface provides:
- Complete CRUD operations for all models
- Advanced filtering and search capabilities
- Bulk operations and data export
- User and permission management
- System configuration options

Access admin at: `http://127.0.0.1:8000/admin/`

## Security Features

- User authentication and authorization
- CSRF protection
- SQL injection prevention through Django ORM
- XSS protection with template escaping
- Secure password hashing

## Development

### Project Structure
```
crm/
├── crm/                 # Django project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── website/             # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # App URL routing
│   ├── admin.py         # Admin configuration
│   └── templates/       # HTML templates
└── manage.py            # Django management
```

### Customization
- Modify models in `website/models.py`
- Add new views in `website/views.py`
- Update templates in `website/templates/`
- Configure admin in `website/admin.py`

## Support

For issues or questions:
1. Check the Django documentation
2. Review MySQL connection settings
3. Verify virtual environment activation
4. Check database permissions and connectivity

## License

This project is for educational and development purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This is a development version. For production use, additional security measures, performance optimizations, and deployment configurations should be implemented.