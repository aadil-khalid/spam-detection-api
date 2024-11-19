from django.core.management.base import BaseCommand
from faker import Faker
from ...models import User, Contact

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(50):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password123',
                phone_number=fake.phone_number(),
                email=fake.email()
            )
        for _ in range(10):
            Contact.objects.create(
                user=user,
                name=fake.name(),
                phone_number=fake.phone_number(),
                is_spam=fake.boolean(chance_of_getting_true=20)
            )
        self.stdout.write(self.style.SUCCESS('Database populated with sample data'))