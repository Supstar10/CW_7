from celery import shared_task
from config.telegram_bot import bot

from habits.models import Habit


@shared_task
def send_telegram_reminder(habit_id):
    habit = Habit.objects.get(id=habit_id)
    message = f'Напоминание о привычке {habit.action} в {habit.place} в {habit.time}.'
    bot.send_message(chat_id=habit.user.profile.telegram_id, text=message)


@shared_task
def schedule_reminders():
    habits = Habit.objects.filter(is_active=True)
    for habit in habits:
        send_telegram_reminder.delay(habit.id)