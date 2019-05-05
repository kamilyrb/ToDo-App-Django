# -*- coding: utf-8 -*-
import os

import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Starting...')
        try:

            self.stdout.write('Deleting migration files...')

            for migration in ['main/migrations/']:
                migration_dir = os.path.realpath(migration)
                files = os.listdir(migration_dir)

                for f in files:
                    if '0' in f:
                        os.remove(migration_dir + "/" + f)

            cursor = connection.cursor()

            self.stdout.write('Dropping schema...')
            cursor.execute("drop schema public cascade;create schema public;")

            self.stdout.write('Applying migrations...')
            call_command('makemigrations')
            call_command('migrate')

            self.stdout.write(self.style.SUCCESS('Successfully executed resetdb command :)'))
        except Exception as ex:
            self.stdout.write(self.style.ERROR('Error line:' + str(sys.exc_info()[-1].tb_lineno)))
            self.stdout.write(self.style.ERROR('Error:' + str(ex.args)))
