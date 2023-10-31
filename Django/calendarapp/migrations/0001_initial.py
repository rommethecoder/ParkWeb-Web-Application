# Generated by Django 4.2 on 2023-10-24 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookableArea",
            fields=[
                ("AreaID", models.AutoField(primary_key=True, serialize=False)),
                ("AreaName", models.CharField(max_length=30)),
                ("Location", models.CharField(max_length=255)),
                ("Capacity", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "EventID",
                    models.AutoField(default=1, primary_key=True, serialize=False),
                ),
                ("EventName", models.CharField(default="Default Event", max_length=30)),
                ("EventDate", models.DateTimeField(default="2023-10-23 00:00:00")),
                ("EventType", models.CharField(default="Default Type", max_length=20)),
                (
                    "EventCategory",
                    models.CharField(default="Default Category", max_length=30),
                ),
                ("Description", models.TextField(default="Default Description")),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("BookingID", models.AutoField(primary_key=True, serialize=False)),
                ("StartDateTime", models.DateTimeField()),
                ("EndDateTime", models.DateTimeField()),
                (
                    "AreaID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="calendarapp.bookablearea",
                    ),
                ),
                (
                    "EventID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="calendarapp.event",
                    ),
                ),
                (
                    "UserID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Availability",
            fields=[
                ("AvailabilityID", models.AutoField(primary_key=True, serialize=False)),
                ("StartDateTIme", models.DateTimeField()),
                ("EndDateTime", models.DateTimeField()),
                ("IsAvailable", models.BooleanField(default=True)),
                (
                    "AreaID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="calendarapp.bookablearea",
                    ),
                ),
            ],
        ),
    ]