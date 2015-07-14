#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import dotenv

if __name__ == "__main__":
    dotenv.read_dotenv()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
