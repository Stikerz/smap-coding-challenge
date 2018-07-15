
from django.core.management import call_command
from django.test import TestCase
import os
from consumption.models import Consumers, Consumption
from dashboard import settings


DATA_DIR= os.path.join(os.path.split(settings.BASE_DIR)[0],
                    'test_data')


class ConsumptionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_file_path = os.path.join(DATA_DIR, 'consumer',
                                      'test_user_data.csv')
        consumption_file_path = os.path.join(DATA_DIR, 'consumption',
                                             '5000.csv')
        call_command('import', consumption_data=consumption_file_path,
                     user_data=user_file_path)

    def test_get_average(self):
        consumption = Consumption.objects.get(id=1)
        average = consumption.get_average()
        self.assertEqual({'Jul': 319, 'Aug': 1237}, average)

    def test_get_total(self):
        consumption = Consumption.objects.get(id=1)
        total = consumption.get_total()
        self.assertEqual({'Jul': 31021.0, 'Aug':14845.0}, total)