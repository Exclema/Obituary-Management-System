from django.test import TestCase, Client
from django.urls import reverse
from .models import Obituary
from datetime import date, timedelta

class ObituaryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.obituary = Obituary.objects.create(
            name="John Doe",
            date_of_birth=date(1950, 1, 1),
            date_of_death=date(2020, 1, 1),
            content="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            author="Jane Smith"
        )
    
    def test_obituary_creation(self):
        self.assertEqual(self.obituary.name, "John Doe")
        self.assertEqual(self.obituary.author, "Jane Smith")
        self.assertTrue(self.obituary.slug)
    
    def test_submit_obituary_view(self):
        response = self.client.get(reverse('submit_obituary'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Submit an Obituary')
        
        # Test form submission
        data = {
            'name': 'Test Name',
            'date_of_birth': '1960-01-01',
            'date_of_death': '2021-01-01',
            'content': 'Test content for the obituary.',
            'author': 'Test Author'
        }
        response = self.client.post(reverse('submit_obituary'), data)
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Verify the obituary was created
        self.assertTrue(Obituary.objects.filter(name='Test Name').exists())
    
    def test_view_obituaries(self):
        response = self.client.get(reverse('view_obituaries'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.obituary.name)
    
    def test_obituary_detail_view(self):
        url = reverse('obituary_detail', kwargs={'slug': self.obituary.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.obituary.name)
        self.assertContains(response, self.obituary.content)
    
    def test_invalid_form_submission(self):
        # Test with date of death before date of birth
        data = {
            'name': 'Invalid Dates',
            'date_of_birth': '2000-01-01',
            'date_of_death': '1990-01-01',
            'content': 'This should fail validation.',
            'author': 'Test Author'
        }
        response = self.client.post(reverse('submit_obituary'), data)
        self.assertEqual(response.status_code, 200)  # Should not redirect
        self.assertContains(response, 'Date of death cannot be before date of birth.')
        
        # Test with future date of death
        future_date = date.today() + timedelta(days=1)
        data['date_of_death'] = future_date.isoformat()
        response = self.client.post(reverse('submit_obituary'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Date of death cannot be in the future.')
