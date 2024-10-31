import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Q, Count, F, Avg, Sum


# Create queries within functions


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    result = []

    matching_astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string)
            |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not matching_astronauts:
        return ""

    for a in matching_astronauts:
        status = 'Active' if a.is_active is True else 'Inactive'
        result.append(f"Astronaut: {a.name}, phone number: {a.phone_number}, status: {status}")

    return '\n'.join(result)


def get_top_astronaut():
    top_astronaut = Astronaut.objects.get_astronauts_by_missions_count().order_by('-missions_count', 'phone_number').first()

    if not top_astronaut or top_astronaut.missions_count == 0:
        return "No data."

    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.missions_count} missions."


def get_top_commander():
    top_commander = Astronaut.objects.annotate(
            missions_count=Count('commander_mission')
        ).order_by(
            '-missions_count', 'phone_number'
        ).first()

    if not top_commander or top_commander.missions_count == 0:
        return "No data."

    return f"Top Commander: {top_commander.name} with {top_commander.missions_count} commanded missions."


def get_last_completed_mission():
    last_mission = Mission.objects.select_related(
        'spacecraft'
    ).prefetch_related(
        'astronauts'
    ).annotate(
      total_spacewalks=Sum('astronauts__spacewalks')
    ).filter(status=StatusChoices.COMPLETED).order_by('-launch_date').first()

    if not last_mission:
        return "No data."

    commander_name = last_mission.commander.name if last_mission.commander else 'TBA'

    astronauts = ', '.join(last_mission.astronauts.all().order_by('name').values_list('name', flat=True))
    total_spacewalks = last_mission.total_spacewalks

    return f"The last completed mission is: {last_mission.name}. Commander: {commander_name}. Astronauts: {astronauts}. Spacecraft: {last_mission.spacecraft_mission.name}. Total spacewalks: {total_spacewalks}."


def get_most_used_spacecraft():
    top_spacecraft = Spacecraft.objects.annotate(
        missions_count=Count('spacecraft_mission')
    ).order_by(
        '-missions_count', 'name'
    ).first()

    if not top_spacecraft or top_spacecraft.missions_count == 0:
        return 'No data.'

    unique_astronauts_count = Astronaut.objects.filter(missions__spacecraft=top_spacecraft).distinct().count()

    return (f"The most used spacecraft is: {top_spacecraft.name}, "
            f"manufactured by {top_spacecraft.manufacturer}, "
            f"used in {top_spacecraft.missions_count} missions, "
            f"astronauts on missions: {unique_astronauts_count}.")


def decrease_spacecrafts_weight():
    spacecrafts_to_update = Spacecraft.objects.filter(
        spacecraft_mission__status='Planned',
        weight__gte=200.0
    ).distinct()

    spacecrafts_to_update.update(weight=F('weight') - 200.0)

    if spacecrafts_to_update == 0:
        return 'No changes in weight'

    avg_weight = spacecrafts_to_update.annotate(average_weight=Avg('weight'))

    return (f"The weight of {spacecrafts_to_update.count()} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight['avg_weight']:.1f}kg")






