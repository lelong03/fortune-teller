from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .forms import FutureInputForm
from .models import Type
from datetime import date


# def index(request):
#     if request.method == 'POST':
#         form = FutureInputForm(request.POST)
#         if form.is_valid():
#             gender = form.cleaned_data['gender']
#             birthday = form.cleaned_data['birthday']
#             # Calculate user's current age
#             today = date.today()
#             age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
#             birthday_str = birthday.strftime('%Y-%m-%d')
#
#             # Based on gender, select the correct birthday list to search
#             if gender == 'male':
#                 types = Type.objects.filter(male_birthdays__icontains=birthday_str)
#             else:
#                 types = Type.objects.filter(female_birthdays__icontains=birthday_str)
#
#             # Expect exactly 12 matching types per business rule
#             if not settings.DEBUG_BYPASS_TYPE_COUNT and types.count() != 12:
#                 error_message = f"Data error: Expected exactly 12 types for the given birthday, but found {types.count()}. Please contact support."
#                 return render(request, 'prediction/index.html', {'form': form, 'error_message': error_message})
#
#             # For each type, get two most recent events (i.e. events with age <= user's age) ordered by descending age.
#             types_with_events = []
#             for t in types:
#                 recent_events = t.events.filter(age__lte=age).order_by('-age')[:2]
#                 types_with_events.append({'type': t, 'events': recent_events})
#
#             context = {
#                 'form': form,
#                 'types_with_events': types_with_events,
#                 'user_age': age,
#                 'birthday_str': birthday_str,
#                 'gender': gender,
#             }
#             return render(request, 'prediction/results.html', context)
#     else:
#         form = FutureInputForm()
#     return render(request, 'prediction/index.html', {'form': form})


def index(request):
    if request.method == 'POST':
        form = FutureInputForm(request.POST)
        if form.is_valid():
            gender = form.cleaned_data['gender']
            birthday = form.cleaned_data['birthday']
            today = date.today()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
            birthday_str = birthday.strftime('%Y-%m-%d')

            if gender == 'male':
                types = Type.objects.filter(male_birthdays__icontains=birthday_str)
            else:
                types = Type.objects.filter(female_birthdays__icontains=birthday_str)

            # If no types are found, show an error message
            if types.count() == 0:
                error_message = "Team has not updated information for this type of future. Please check back later."
                return render(request, 'prediction/index.html', {'form': form, 'error_message': error_message})

            # Otherwise, proceed even if there are less than 12 types (for testing purposes)
            types_with_events = []
            for t in types:
                recent_events = t.events.filter(age__lte=age).order_by('-age')[:2]
                types_with_events.append({'type': t, 'events': recent_events})

            context = {
                'form': form,
                'types_with_events': types_with_events,
                'user_age': age,
                'birthday_str': birthday_str,
                'gender': gender,
            }
            return render(request, 'prediction/results.html', context)
    else:
        form = FutureInputForm()
    return render(request, 'prediction/index.html', {'form': form})


def type_detail(request, type_id):
    # Display all events for the chosen type
    t = get_object_or_404(Type, id=type_id)
    events = t.events.all().order_by('age')
    context = {
        'type': t,
        'events': events,
    }
    return render(request, 'prediction/detail.html', context)
