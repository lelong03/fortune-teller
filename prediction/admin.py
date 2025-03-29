from django import forms
from django.contrib import admin
from .models import Type, Event
import csv
import io


class TypeAdminForm(forms.ModelForm):
    # Extra fields for CSV file upload (not part of the model)
    male_birthdays_csv = forms.FileField(required=False, help_text="Upload CSV file for male birthdays")
    female_birthdays_csv = forms.FileField(required=False, help_text="Upload CSV file for female birthdays")

    class Meta:
        model = Type
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Process male_birthdays CSV file if provided
        male_csv = self.cleaned_data.get('male_birthdays_csv')
        if male_csv:
            data = male_csv.read().decode('utf-8')
            birthdays = []
            reader = csv.reader(io.StringIO(data))
            for row in reader:
                birthdays.extend(row)
            # Join birthdays using "|" as the delimiter
            instance.male_birthdays = "|".join(birthday.strip() for birthday in birthdays if birthday.strip())

        # Process female_birthdays CSV file if provided
        female_csv = self.cleaned_data.get('female_birthdays_csv')
        if female_csv:
            data = female_csv.read().decode('utf-8')
            birthdays = []
            reader = csv.reader(io.StringIO(data))
            for row in reader:
                birthdays.extend(row)
            instance.female_birthdays = "|".join(birthday.strip() for birthday in birthdays if birthday.strip())

        if commit:
            instance.save()
        return instance


# Inline for Event model to allow adding multiple events on the Type admin page
class EventInline(admin.TabularInline):
    model = Event
    extra = 1  # You can change this number to show more blank forms


class TypeAdmin(admin.ModelAdmin):
    form = TypeAdminForm
    inlines = [EventInline]
    list_display = ('name',)
    search_fields = ('name', 'description')
    # If you had additional fields that could be used for filtering, you could add them here:
    # list_filter = ('some_field',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('type', 'age')
    search_fields = ('description', 'description_2', 'description_3')
    list_filter = ('age', 'type')


admin.site.register(Type, TypeAdmin)
admin.site.register(Event, EventAdmin)
