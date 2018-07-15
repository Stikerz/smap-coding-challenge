
from django.core.management import call_command
from django.test import TestCase
import os
from consumption.models import Consumers, Consumption
from dashboard import settings


DATA_DIR= os.path.join(os.path.split(settings.BASE_DIR)[0],
                    'test_data')


class ConsumptionViewsTest(TestCase):

    def test_summary_view(self):
        response = self.client.get("/summary/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "consumption/summary.html")

    def test_detail_view_with_valid_arg(self):
        user_file_path = os.path.join(DATA_DIR, 'consumer',
                                      'test_user_data.csv')
        consumption_file_path = os.path.join(DATA_DIR, 'consumption',
                                             '5000.csv')
        call_command('import', consumption_data=consumption_file_path,
                     user_data=user_file_path)

        consumption = Consumption.objects.get(id=1)
        response = self.client.get("/detail/{}/".format(
            str(consumption.consumer_id.id)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "consumption/detail.html")

    def test_detail_view_with_invalid_arg(self):
        response = self.client.get("/detail/4/")
        self.assertEqual(response.status_code, 404)


