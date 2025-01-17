import csv
from typing import Any

from django.core.management import base

from apps.rtm.models import Science


import csv
from typing import Any

from django.core.management import base

from apps.rtm.models import Science


class Command(base.BaseCommand):
    help = "Import CSV data into Science model"

    def handle(self, *args: Any, **options: Any):
        try:
            with open("assets/subjects.csv", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                sciences = [
                    {
                        "name_uz": row["name_uz"],
                        "name_ru": row["name_ru"],
                    }
                    for row in reader
                ]
                existing_names = set(
                    Science.objects.filter(
                        name_uz__in=[r["name_uz"] for r in sciences]
                    ).values_list("name_uz", flat=True)
                )
                new_sciences = [
                    Science(name_uz=data["name_uz"], name_ru=data["name_ru"])
                    for data in sciences
                    if data["name_uz"] not in existing_names
                ]
                Science.objects.bulk_create(new_sciences)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created {len(new_sciences)} Science objects."
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
