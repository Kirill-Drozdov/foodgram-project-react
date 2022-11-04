import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

models_and_data = (
    # (Ingredient, '../../data/ingredients.csv'),
    (Ingredient, 'ingredients.csv'),
)


class Command(BaseCommand):
    help = 'Loads csv files in database.'

    def handle(self, *args, **options):
        for model, path in models_and_data:
            with open(path, encoding='utf-8') as r_file:
                file_reader = csv.reader(r_file, delimiter=',')
                next(file_reader)
                for row in file_reader:
                    model(
                        name=row[0],
                        measurement_unit=row[1],
                    ).save()
                self.stdout.write(self.style.SUCCESS(
                    (f'Модель {model.__name__} '
                     'успешно заполнена тестовыми данными.'))
                )
