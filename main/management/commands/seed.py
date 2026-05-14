from django.core.management.base import BaseCommand
from main.models import User, Project, ProjectMember, Task
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        Task.objects.all().delete()
        ProjectMember.objects.all().delete()
        Project.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write('Creating users...')
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@taskflow.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        sarah = User.objects.create_user(
            username='sarah',
            email='sarah@taskflow.com',
            password='password123',
            first_name='Sarah',
            last_name='Chen',
            role='member'
        )

        james = User.objects.create_user(
            username='james',
            email='james@taskflow.com',
            password='password123',
            first_name='James',
            last_name='Wilson',
            role='member'
        )

        self.stdout.write('Creating projects...')
        p1 = Project.objects.create(
            name='Website Redesign',
            description='Complete redesign of the company website with modern UI/UX',
            owner=admin,
            color='#6366f1'
        )
        ProjectMember.objects.create(project=p1, user=admin, role='admin')
        ProjectMember.objects.create(project=p1, user=sarah, role='member')
        ProjectMember.objects.create(project=p1, user=james, role='member')

        p2 = Project.objects.create(
            name='Mobile App Development',
            description='Build a cross-platform mobile application',
            owner=admin,
            color='#8b5cf6'
        )
        ProjectMember.objects.create(project=p2, user=admin, role='admin')
        ProjectMember.objects.create(project=p2, user=sarah, role='member')

        self.stdout.write('Creating tasks...')
        now = timezone.now().date()
        
        Task.objects.create(
            title='Design wireframes',
            description='Create low-fidelity wireframes for the homepage',
            status='completed',
            priority='medium',
            project=p1,
            assignee=sarah,
            created_by=admin,
            due_date=now - timedelta(days=2)
        )

        Task.objects.create(
            title='Setup React Native project',
            description='Initialize the React Native project with required dependencies',
            status='completed',
            priority='high',
            project=p2,
            assignee=sarah,
            created_by=admin,
            due_date=now - timedelta(days=1)
        )

        Task.objects.create(
            title='Implement login UI',
            description='Build the login and registration screens',
            status='in-progress',
            priority='high',
            project=p2,
            assignee=sarah,
            created_by=admin,
            due_date=now + timedelta(days=2)
        )

        Task.objects.create(
            title='Database optimization',
            description='Add indexes and optimize slow queries',
            status='todo',
            priority='urgent',
            project=p1,
            assignee=james,
            created_by=admin,
            due_date=now + timedelta(days=1)
        )
        
        Task.objects.create(
            title='Write API documentation',
            description='Document all new endpoints for the mobile app',
            status='todo',
            priority='medium',
            project=p2,
            assignee=admin,
            created_by=admin,
            due_date=now + timedelta(days=5)
        )

        Task.objects.create(
            title='Fix navigation bug',
            description='Mobile menu does not close on link click',
            status='in-review',
            priority='high',
            project=p1,
            assignee=james,
            created_by=sarah,
            due_date=now - timedelta(days=1)
        )

        Task.objects.create(
            title='User research interviews',
            description='Conduct 5 interviews with target demographic',
            status='in-progress',
            priority='medium',
            project=p1,
            assignee=admin,
            created_by=admin,
            due_date=now + timedelta(days=7)
        )

        Task.objects.create(
            title='Setup CI/CD pipeline',
            description='Configure GitHub Actions for automated testing',
            status='todo',
            priority='urgent',
            project=p1,
            assignee=admin,
            created_by=admin,
            due_date=now + timedelta(days=3)
        )

        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))
