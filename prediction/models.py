from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # These fields store a long string of birthdays separated by "|" or ";".
    male_birthdays = models.TextField(help_text="List of male birthdays separated by '|' or ';'", blank=True)
    female_birthdays = models.TextField(help_text="List of female birthdays separated by '|' or ';'", blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    type = models.ForeignKey(Type, related_name='events', on_delete=models.CASCADE)
    age = models.IntegerField(help_text="Age at which the event will occur")
    description = models.TextField(blank=True)
    description_2 = models.TextField(blank=True)
    description_3 = models.TextField(blank=True)

    def __str__(self):
        return f"Event for {self.type.name} at age {self.age}"
