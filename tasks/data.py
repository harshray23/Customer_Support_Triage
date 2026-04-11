from tasks.easy import get_task as easy_task
from tasks.medium import get_task as medium_task
from tasks.hard import get_task as hard_task

import random


def get_random_task():
    return random.choice([
        easy_task(),
        medium_task(),
        hard_task()
    ])