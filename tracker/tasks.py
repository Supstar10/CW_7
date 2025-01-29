from celery import shared_task
from config.telegram_bot import bot
from tracker.models import Habit
from django.utils import timezone
import datetime

@shared_task
def send_telegram_reminder(habit_id):
    habit = Habit.objects.get(id=habit_id)
    current_time = timezone.localtime(timezone.now()).time()
    reminder_time = habit.time

    # Проверяем, что напоминание отправляется за 10 минут до времени выполнения привычки
    if abs((datetime.datetime.combine(datetime.date.today(), current_time) -
            datetime.datetime.combine(datetime.date.today(), reminder_time)).total_seconds()) <= 600:
        message = f'Напоминание о привычке {habit.action} в {habit.place} в {habit.time}.'
        bot.send_message(chat_id=habit.user.telegram_id, text=message)

@shared_task
def schedule_reminders():
    habits = Habit.objects.filter(is_active=True)
    for habit in habits:
        # Вычисляем время янапоминани (за 10 минут до времени выполнения привычки)
        reminder_time = (datetime.datetime.combine(datetime.date.today(), habit.time) -
                         datetime.timedelta(minutes=10)).time()

        # Получаем текущее время
        current_time = timezone.localtime(timezone.now()).time()

        # Проверяем, что текущее время соответствует времени напоминания
        if abs((datetime.datetime.combine(datetime.date.today(), current_time) -
                datetime.datetime.combine(datetime.date.today(), reminder_time)).total_seconds()) <= 60:
            send_telegram_reminder.delay(habit.id)
