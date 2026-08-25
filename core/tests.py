from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import Note, Homework, Task


class AuthenticationAndAccessTests(TestCase):
    """Tests for student registration, login, logout, and access control."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='teststudent',
            email='teststudent@example.com',
            password='testpassword123'
        )

    def test_home_page_accessible(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student Study Portal")

    def test_registration_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newstudent',
            'email': 'newstudent@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newstudent').exists())
        # Automatically logged in and redirected to dashboard
        self.assertTrue(response.context['user'].is_authenticated)

    def test_registration_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'mismatchuser',
            'email': 'mismatch@example.com',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'teststudent',
            'password': 'testpassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.login(username='teststudent', password='testpassword123')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_unauthenticated_user_redirected_to_login(self):
        protected_urls = [
            'dashboard', 'notes', 'notes_add',
            'homework', 'homework_add',
            'todo', 'todo_add',
            'youtube', 'wikipedia', 'dictionary', 'books', 'unit_converter'
        ]
        for url_name in protected_urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/login/'))


class DashboardAndDataPrivacyTests(TestCase):
    """Tests for dashboard calculation and strict user data privacy."""

    def setUp(self):
        self.user1 = User.objects.create_user(username='student1', password='pass12345')
        self.user2 = User.objects.create_user(username='student2', password='pass12345')
        
        # User 1 items
        self.note1 = Note.objects.create(user=self.user1, title="User1 Note", subject="Math", content="Calculus")
        self.hw1 = Homework.objects.create(user=self.user1, title="User1 HW", subject="Physics", due_date=timezone.now().date() + timedelta(days=2))
        self.task1 = Task.objects.create(user=self.user1, title="User1 Task")

        # User 2 items
        self.note2 = Note.objects.create(user=self.user2, title="User2 Note", subject="CS", content="Algorithms")
        self.hw2 = Homework.objects.create(user=self.user2, title="User2 HW", subject="CS", due_date=timezone.now().date() + timedelta(days=1))
        self.task2 = Task.objects.create(user=self.user2, title="User2 Task")

    def test_dashboard_statistics(self):
        self.client.login(username='student1', password='pass12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_notes'], 1)
        self.assertEqual(response.context['pending_homework'], 1)
        self.assertEqual(response.context['completed_homework'], 0)
        self.assertEqual(response.context['pending_tasks'], 1)
        self.assertEqual(response.context['completed_tasks'], 0)

    def test_notes_user_privacy(self):
        self.client.login(username='student1', password='pass12345')
        response = self.client.get(reverse('notes'))
        self.assertContains(response, "User1 Note")
        self.assertNotContains(response, "User2 Note")

        # Attempt to edit or delete User2's note should 404
        edit_res = self.client.get(reverse('notes_edit', kwargs={'id': self.note2.id}))
        self.assertEqual(edit_res.status_code, 404)
        delete_res = self.client.post(reverse('notes_delete', kwargs={'id': self.note2.id}))
        self.assertEqual(delete_res.status_code, 404)

    def test_homework_user_privacy(self):
        self.client.login(username='student1', password='pass12345')
        response = self.client.get(reverse('homework'))
        self.assertContains(response, "User1 HW")
        self.assertNotContains(response, "User2 HW")

        # Attempt to toggle, edit, or delete User2's homework should 404
        toggle_res = self.client.get(reverse('homework_toggle', kwargs={'id': self.hw2.id}))
        self.assertEqual(toggle_res.status_code, 404)

    def test_todo_user_privacy(self):
        self.client.login(username='student1', password='pass12345')
        response = self.client.get(reverse('todo'))
        self.assertContains(response, "User1 Task")
        self.assertNotContains(response, "User2 Task")

        toggle_res = self.client.get(reverse('todo_toggle', kwargs={'id': self.task2.id}))
        self.assertEqual(toggle_res.status_code, 404)


class CRUDOperationsTests(TestCase):
    """Tests for Notes, Homework, and To-Do CRUD functionality."""

    def setUp(self):
        self.user = User.objects.create_user(username='cruduser', password='password123')
        self.client.login(username='cruduser', password='password123')

    def test_note_crud(self):
        # Create
        res = self.client.post(reverse('notes_add'), {
            'title': 'Operating Systems Notes',
            'subject': 'CS301',
            'content': 'Process scheduling, Semaphore, Deadlock detection'
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        note = Note.objects.get(title='Operating Systems Notes')
        self.assertEqual(note.user, self.user)

        # Edit
        res = self.client.post(reverse('notes_edit', kwargs={'id': note.id}), {
            'title': 'OS Notes Updated',
            'subject': 'CS301',
            'content': 'Updated content'
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        note.refresh_from_db()
        self.assertEqual(note.title, 'OS Notes Updated')

        # Delete
        res = self.client.post(reverse('notes_delete', kwargs={'id': note.id}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Note.objects.filter(id=note.id).exists())

    def test_homework_crud_and_toggle(self):
        # Create
        due = timezone.now().date() + timedelta(days=3)
        res = self.client.post(reverse('homework_add'), {
            'title': 'Lab Assignment 1',
            'subject': 'Database Systems',
            'due_date': due,
            'description': 'SQL Queries'
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        hw = Homework.objects.get(title='Lab Assignment 1')
        self.assertFalse(hw.completed)

        # Toggle Complete
        self.client.get(reverse('homework_toggle', kwargs={'id': hw.id}), follow=True)
        hw.refresh_from_db()
        self.assertTrue(hw.completed)

        # Toggle Pending
        self.client.get(reverse('homework_toggle', kwargs={'id': hw.id}), follow=True)
        hw.refresh_from_db()
        self.assertFalse(hw.completed)

        # Delete
        self.client.post(reverse('homework_delete', kwargs={'id': hw.id}), follow=True)
        self.assertFalse(Homework.objects.filter(id=hw.id).exists())

    def test_todo_crud_and_toggle(self):
        # Create
        res = self.client.post(reverse('todo_add'), {
            'title': 'Read Chapter 5',
            'description': 'Prepare summary notes'
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        task = Task.objects.get(title='Read Chapter 5')
        self.assertFalse(task.completed)

        # Toggle Complete
        self.client.get(reverse('todo_toggle', kwargs={'id': task.id}), follow=True)
        task.refresh_from_db()
        self.assertTrue(task.completed)

        # Delete
        self.client.post(reverse('todo_delete', kwargs={'id': task.id}), follow=True)
        self.assertFalse(Task.objects.filter(id=task.id).exists())


class StudyToolsAndAPIViewsTests(TestCase):
    """Tests for study tools views and error resilience."""

    def setUp(self):
        self.user = User.objects.create_user(username='tooluser', password='password123')
        self.client.login(username='tooluser', password='password123')

    def test_unit_converter_calculations(self):
        # Test Length conversion: 1 kilometer to meters = 1000 meters
        res = self.client.get(reverse('unit_converter'), {
            'category': 'length',
            'input_value': '1',
            'from_unit': 'kilometer',
            'to_unit': 'meter'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['result'], 1000.0)

        # Test Temperature conversion: 0 Celsius to Fahrenheit = 32
        res = self.client.get(reverse('unit_converter'), {
            'category': 'temperature',
            'input_value': '0',
            'from_unit': 'celsius',
            'to_unit': 'fahrenheit'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['result'], 32.0)

    def test_youtube_page_renders_gracefully_when_key_empty(self):
        res = self.client.get(reverse('youtube'), {'q': 'Python'})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "YouTube")

    def test_wikipedia_page_renders(self):
        res = self.client.get(reverse('wikipedia'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Wikipedia")

    def test_dictionary_page_renders(self):
        res = self.client.get(reverse('dictionary'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Dictionary")

    def test_books_page_renders(self):
        res = self.client.get(reverse('books'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Academic Book Search")
