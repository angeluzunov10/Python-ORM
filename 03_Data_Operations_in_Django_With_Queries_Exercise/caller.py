import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions

from main_app.models import Pet, Car, Artifact, Location, Task, HotelRoom, Character


def create_pet(name, species):
    new_pet = Pet.objects.create(name=name, species=species)
    new_pet.save()

    return f'{new_pet.name} is a very cute {new_pet.species}!'


def create_artifact(name, origin, age, description, is_magical):
    new_artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f'The artifact {new_artifact.name} is {new_artifact.age} years old!'


def rename_artifact(artifact: Artifact, new_name):
    # Artifact.objects.filter(is_magical=True, age__gt=250, pk=artifact.pk).update(name=new_name)

    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    result =[]
    all_locations = Location.objects.all().order_by('-id')

    for location in all_locations:
        result.append(f'{location.name} has a population of {location.population}!')

    return '\n'.join(result)


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    all_cars = Car.objects.all()

    for car in all_cars:
        percentage_off = sum(int(digit) for digit in str(car.year)) / 100
        car.price_with_discount = float(car.price) - float(car.price) * percentage_off
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)
    result = []

    for task in unfinished_tasks:
        result.append(f'Task - {task.title} needs to be done until {task.due_date}!')

    return '\n'.join(result)


def complete_odd_tasks():
    tasks = Task.objects.all()

    for task in tasks:
        if task.id % 2 ==1:
            task.is_finished = True

    Task.objects.bulk_update(tasks, ['is_finished'])


def encode_and_replace(text, task_title):
    decoded_text = ''.join(chr(ord(symbol) - 3) for symbol in text)

    Task.objects.filter(title=task_title).update(description=decoded_text)


def get_deluxe_rooms():
    all_rooms = HotelRoom.objects.all()
    result = []

    for room in all_rooms:
        if room.id % 2 == 0 and room.room_type == 'Deluxe':
            result.append(f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!')

    return '\n'.join(result)


def increase_room_capacity():
    all_rooms = HotelRoom.objects.all().order_by('id')
    previous_room_capacity = None

    for room in all_rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity

    HotelRoom.objects.bulk_update(all_rooms, ['capacity'])


def reserve_first_room():
    first_room = HotelRoom.objects.first()

    first_room.is_reserved = True

    first_room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()

    if not last_room.is_reserved:
        last_room.delete()


def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level= F('level') + 3,
        intelligence= F('intelligence') - 7
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points= F('hit_points') / 2,
        dexterity= F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory='The inventory is empty'
    )


def fuse_characters(first_character: Character, second_character: Character):
    mega_character = Character.objects.create(
        name=f'{first_character.name} {second_character.name}',
        class_name='Fusion',
        level=int((first_character.level + second_character.level) // 2),
        strength=int((first_character.strength + second_character.strength) * 1.2),
        dexterity=int((first_character.dexterity + second_character.dexterity) * 1.4),
        intelligence=int((first_character.intelligence + second_character.intelligence) * 1.5),
        hit_points=first_character.hit_points + second_character.hit_points,
        inventory=' '
    )

    if first_character.class_name in ['Mage', 'Scout']:
        mega_character.inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    elif first_character.class_name in ['Warrior', 'Assassin']:
        mega_character.inventory = 'Dragon Scale Armor, Excalibur'

    mega_character.save()

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.all().update(
        dexterity=30
    )


def grand_intelligence():
    Character.objects.all().update(
        intelligence=40
    )


def grand_strength():
    Character.objects.all().update(
        strength=50
    )


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()















