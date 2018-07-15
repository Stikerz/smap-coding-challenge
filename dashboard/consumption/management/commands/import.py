from django.core.management.base import BaseCommand

import os
import csv
import glob
import logging
from dashboard import settings
from consumption.models import Consumers, Consumption

class Command(BaseCommand):
    help = 'import data'
    stdlogger = logging.getLogger(__name__)
    name = __name__
    def _save_consumer_data(self,filename):

        self.stdlogger.debug("Opening file {}".format(filename))
        with open(os.path.expanduser(filename), 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)

            for row in csvreader:
                if not Consumers.objects.filter(id=row[0]).exists():
                    self.stdlogger.info("Adding Consumer {} to DB".format(row[
                                                                                0]))
                    Consumers.objects.create(id=row[0], area=row[1],
                                                 tariff=row[2])
                    self.stdlogger.debug("Consumer {} successfully added into "
                                        "DB".format(row[0]))
                else:
                    self.stdlogger.debug("Consumer {} already exists in "
                                         "DB".format(row[0]))

    def _save_consumption_data(self, filename, user):

        self.stdlogger.debug("Opening file {}".format(filename))
        with open(os.path.expanduser(filename), 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)

            for row in csvreader:
                if not Consumption.objects.filter(consumer_id=user, date_time=row[\
                        0]).exists():
                    user_instance = Consumers.objects.get(id=user)
                    self.stdlogger.debug("Adding consumption info for consumer {"
                                     "} into DB".format(user))
                    Consumption.objects.create(consumer_id=user_instance,
                                               date_time=row[\
                        0], consumption= row[1])
                    self.stdlogger.debug("Successfuly added consumption info for "
                                     "consumer {} into the DB".format(user))
                else:
                    self.stdlogger.debug("Consumption info for consumer {} "
                                         "date:{} already exists".format(user,
                                                                         row[0]))

    def add_arguments(self, parser):
        parser.add_argument('--user-data', '-u', dest='user_data',
                            action='store', default='' ,
                            required=False, help='')

        parser.add_argument('--consumption-data', '-c', dest='consumption_data',
                            required=False, help='', action='store', default='')


    def handle(self, *args, **options):
        if options['user_data']:
            if os.path.exists(options['user_data']):
                if os.path.isdir(options['user_data']):
                    self.stdlogger.debug("Find all files in directory {}".format(options['user_data']))
                    consumer_files = glob.glob("{}/*.csv".format(options[
                                                                     'user_data']))

                    for file in consumer_files:
                        self.stdlogger.info(
                            "Importing file {} ".format(file))
                        self._save_consumer_data(file)

                else:
                    self.stdlogger.info("Importing file {} ".format(options[
                                                                'user_data']))
                    self._save_consumer_data(options['user_data'])
            else:
                self.stdlogger.error("Filepath '{}' does not exist".format(
                    options['user_data']))


        if options['consumption_data']:
            if os.path.exists(options['consumption_data']):
                if os.path.isdir(options['consumption_data']):
                    consumption_files = glob.glob("{}/*.csv".format(options[
                        'consumption_data']))

                    for file in consumption_files:
                        filename = os.path.split(file)[1]
                        user = filename.split('.')[0]
                        self.stdlogger.info(
                            "Importing file {} ".format(file))
                        self._save_consumption_data(file, user)

                else:
                    filename = os.path.split(options['consumption_data'])[1]
                    user = filename.split('.')[0]
                    self._save_consumption_data(options['consumption_data'], user)
            else:
                self.stdlogger.error("Filepath '{}' does not exist".format(
                    options['consumption_data']))



        if not options['consumption_data'] and not options['user_data']:

            consumer_file = os.path.join(os.path.split(settings.BASE_DIR)[0],
                                         'data','consumer',
                                     'user_data.csv')
            consumption_dir = os.path.join(os.path.split(settings.BASE_DIR)[0],
                                         'data','consumption')

            self.stdlogger.info("Importing file {} ".format(consumer_file))
            self._save_consumer_data(consumer_file)

            consumption_files = glob.glob("{}/*.csv".format(consumption_dir))

            for file in consumption_files:
                filename = os.path.split(file)[1]
                user = filename.split('.')[0]
                self.stdlogger.info("Importing file {} ".format(file))
                self._save_consumption_data(file, user)



