from apscheduler.schedulers.background import BackgroundScheduler
from core.models import Letter
from django.utils import timezone


def deliver_letters():
    letters = Letter.letters.sents()
    for letter in letters:
        if letter.delivery_date < timezone.now():
            letter.deliver()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        deliver_letters,
        'interval',
        minutes=1,
        id='deliver_letters',
        replace_existing=True)

    scheduler.start()
