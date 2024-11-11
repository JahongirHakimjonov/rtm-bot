import csv
import os

from django.conf import settings
from django.core.management import base

from apps.rtm.models import Region


class Command(base.BaseCommand):
    help = "Import CSV data into Region model"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            nargs="?",
            default=os.path.join(settings.BASE_DIR, "assets/regions.csv"),
        )

    def handle(self, *args, **options):
        csv_path = options.get("csv_path")

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_path}"))
            return

        try:
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    id = row.get("id", None)
                    name_uz = row.get("name_uz", None)
                    name_ru = row.get("name_ru", None)

                    if not name_uz and not name_ru:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Skipping row with missing region names: {row}"
                            )
                        )
                        continue

                    region = None
                    try:
                        if name_uz:
                            region = Region.objects.get(name_uz=name_uz)
                        elif name_ru:
                            region = Region.objects.get(name_ru=name_ru)
                    except Region.DoesNotExist:
                        pass
                    except Region.MultipleObjectsReturned:
                        self.stdout.write(
                            self.style.ERROR(f"Multiple regions found for {row}")
                        )
                        continue

                    if region:
                        if id:
                            region.id = id
                        if name_uz:
                            region.name_uz = name_uz
                        if name_ru:
                            region.name_ru = name_ru
                        region.save()
                        self.stdout.write(self.style.SUCCESS(f"Region updated: {row}"))
                    else:
                        Region.objects.update_or_create(
                            id=id,
                            defaults={
                                "name_uz": name_uz,
                                "name_ru": name_ru,
                            },
                        )
                        self.stdout.write(self.style.SUCCESS(f"Region created: {row}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
