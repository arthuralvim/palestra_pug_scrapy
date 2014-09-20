# -*- coding: utf-8 -*-

from plan import Plan

cron = Plan()

# cron.script('script.py', path='/web/yourproject/scripts', every='1.month')

if __name__ == "__main__":
    cron.run('check')
    # cron.run('clear')
    # cron.run('update')
    # cron.run('write')
