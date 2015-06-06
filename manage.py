#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import dotenv
import shutil
from getenv import env

if __name__ == "__main__":
    dotenv.read_dotenv()
    
    if not os.path.isfile(env('SQLITE_DB')):
        print "Copying chemiresto.prod.sqlite to chemiresto.sqlite...\n"
        shutil.copy2(env('SQLITE_DB_BACKUP'), env('SQLITE_DB'))
        print "Ajouter les modèles récemment créés...\n"
        os.system('manage.py syncdb')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

