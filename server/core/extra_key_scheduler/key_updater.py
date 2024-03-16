from apscheduler.schedulers.background import BackgroundScheduler
from core.models import User, Timer

def addKeys():
  timer = Timer.objects.all().first()
  users = User.objects.all()
  print(timer.is_started)
  if timer.is_started:
    for user in users:
      user.keys += 1
      user.save(update_fields=['keys'])
    print("keys updated")
  print("hehe")
  

# From and to can also be added. That wll be done when the dates are finalized.

def start():
  mins = Timer.objects.all().first().add_keys_interval_min
  scheduler = BackgroundScheduler()
  scheduler.add_job(addKeys, "interval", minutes=mins,id="addKey_001",replace_existing=True)
  scheduler.start()
