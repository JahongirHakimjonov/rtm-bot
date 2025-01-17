import csv
import os
from typing import Any

from django.conf import settings
from django.core.management import base

from apps.rtm.models import Region


class Command(base.BaseCommand):
    help = "Import CSV data into Region model"

    def handle(self, *args: Any, **options: Any):
        try:
            with open(os.path.join(settings.BASE_DIR, "assets/regions.csv"), newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                regions = [
                    {
                        "name_uz": row["name_uz"],
                        "name_ru": row["name_ru"],
                    }
                    for row in reader
                ]
                existing_names = set(
                    Region.objects.filter(
                        name_uz__in=[r["name_uz"] for r in regions]
                    ).values_list("name_uz", flat=True)
                )
                new_regions = [
                    Region(name_uz=data["name_uz"], name_ru=data["name_ru"])
                    for data in regions
                    if data["name_uz"] not in existing_names
                ]
                Region.objects.bulk_create(new_regions)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created {len(new_regions)} Region objects."
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
