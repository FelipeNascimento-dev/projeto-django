import random
from django.core.management.base import BaseCommand
from faker import Faker
from sales.models import Sale

class Command(BaseCommand):
    help = 'Popula o BD com dados de vendas fictícios'

    def handle(self,*args, **kwargs):
        faker = Faker()
        products = [
            "Produto A", "Produto B", "Produto C",
            "Produto D", "Produto E", "Produto F",
            "Produto G", "Produto H", "Produto I", "Produto J"
        ]

        sales = []
        for _ in range(300):
            sale = Sale(
                date=faker.date_this_year(),
                product=random.choice(products),
                quantity=random.randint(1, 100),
                price=round(random.uniform(10.0, 500.0), 2)
            )

            sales.append(sale)
        Sale.objects.bulk_create(sales)

        self.stdout.write(self.style.SUCCESS(
            'Banco de dados foi populado com 300 vendas!'
            ))