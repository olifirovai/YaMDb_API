from django.core.management.base import BaseCommand, CommandError
from ...models import Category
import csv


class Command(BaseCommand):
  


    def handle(self, *args, **options):
        with open('C:\\study\\api_yamdb\\data\\category.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            linenumer=1
            
            for row in reader:
                if linenumer==1:
                    linenumer=2
                    continue
                else:                
                    _, created = Category.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                        )
                self.stdout.write(str(row), ending='')
