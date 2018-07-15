from django.core.management import call_command
from django.test import TestCase
import os
from consumption.models import Consumers, Consumption
from dashboard import settings

DATA_DIR= os.path.join(os.path.split(settings.BASE_DIR)[0],
                    'test_data')


class ImportTest(TestCase):


    def test_command_user_flag_with_file_path(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        file_path = os.path.join(DATA_DIR, 'consumer', 'test_user_data.csv')
        call_command('import', user_data=file_path)

        self.assertEqual(len(Consumers.objects.all()), 61)

    def test_command_user_flag_with_invalid_filepath(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        file_path = '/fake/foo/path'
        call_command('import', user_data=file_path)

        self.assertEqual(len(Consumers.objects.all()), 0)


    def test_command_user_flag_with_dir_path(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        dir_path = os.path.join(DATA_DIR, 'consumer')
        call_command('import', user_data=dir_path)

        self.assertEqual(len(Consumers.objects.all()), 61)

    def test_command_user_flag_with_invalid_dir_path(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        dir_path = '/fake/foo/dir'
        call_command('import', user_data=dir_path)

        self.assertEqual(len(Consumers.objects.all()), 0)


    def test_command_consumption_flag_with_file_path(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        self.assertEqual(len(Consumption.objects.all()), 0)
        Consumers.objects.create(id=5000, area='a1', tariff='t2')
        self.assertEqual(len(Consumers.objects.all()), 1)
        file_path = os.path.join(DATA_DIR, 'consumption', '5000.csv')
        call_command('import', consumption_data=file_path)

        self.assertEqual(len(Consumption.objects.all()), 109)

    def test_command_consumption_flag_with_invalid_file_path(self):
        self.assertEqual(len(Consumption.objects.all()), 0)
        file_path = '/fake/foo/path'
        call_command('import', consumption_data=file_path)
        self.assertEqual(len(Consumption.objects.all()), 0)


    def test_command_consumption_flag_with_dir_path(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        self.assertEqual(len(Consumption.objects.all()), 0)
        Consumers.objects.create(id=5000, area='a1', tariff='t2')
        self.assertEqual(len(Consumers.objects.all()), 1)
        file_path = os.path.join(DATA_DIR, 'consumption')
        call_command('import', consumption_data=file_path)

        self.assertEqual(len(Consumption.objects.all()), 109)


    def test_command_user_and_consumption_flag_with_dir_path(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        self.assertEqual(len(Consumption.objects.all()), 0)
        user_dir_path = os.path.join(DATA_DIR, 'consumer')
        consumption_dir_path = os.path.join(DATA_DIR, 'consumption')
        call_command('import', consumption_data=consumption_dir_path,
                     user_data=user_dir_path )
        self.assertEqual(len(Consumers.objects.all()), 61)
        self.assertEqual(len(Consumption.objects.all()), 109)


    def test_command_user_and_consumer_flag_with_invalid_dir_path(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        self.assertEqual(len(Consumption.objects.all()), 0)
        user_dir_path = '/foo/boo'
        consumption_dir_path = 'foo/foo'
        call_command('import', consumption_data=consumption_dir_path,
                     user_data=user_dir_path )
        self.assertEqual(len(Consumers.objects.all()), 0)
        self.assertEqual(len(Consumption.objects.all()), 0)

    def test_command_user_and_consumer_flag_with_file_path(self):
        self.assertEqual(len(Consumers.objects.all()), 0)
        self.assertEqual(len(Consumption.objects.all()), 0)
        user_file_path = os.path.join(DATA_DIR, 'consumer', 'test_user_data.csv')
        consumption_file_path = os.path.join(DATA_DIR, 'consumption',
                                            '5000.csv')
        call_command('import', consumption_data=consumption_file_path,
                     user_data=user_file_path )
        self.assertEqual(len(Consumers.objects.all()), 61)
        self.assertEqual(len(Consumption.objects.all()), 109)





