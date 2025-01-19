from rest_framework import serializers
from tracker.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        habit = Habit.objects.create(user=user, **validated_data)
        return habit

    def validate(self, attrs):
        habit = Habit(**attrs)
        habit.user = self.context['request'].user
        habit.clean()
        return attrs
