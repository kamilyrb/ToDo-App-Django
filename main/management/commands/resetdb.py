# -*- coding: utf-8 -*-
import os

import sys

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand


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

            call_command('flush', interactive=False)
            self.stdout.write('Removed db...')
            user = User()
            user.username = 'admin'
            user.is_superuser = True
            user.first_name = 'Super'
            user.last_name = 'User'
            user.is_active = True
            user.set_password('123')
            user.save()
            self.stdout.write('Created super user ...')

            self.stdout.write('Applying migrations...')
            call_command('makemigrations')
            call_command('migrate')

            self.stdout.write(self.style.SUCCESS('Successfully executed resetdb command :)'))
        except Exception as ex:
            self.stdout.write(self.style.ERROR('Error line:' + str(sys.exc_info()[-1].tb_lineno)))
            self.stdout.write(self.style.ERROR('Error:' + str(ex.args)))
