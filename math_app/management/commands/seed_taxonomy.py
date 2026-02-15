import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from math_app.models import Grade, Subject, Tag


class Command(BaseCommand):
    help = "Seed Grade/Subject/Tag data from a fixture JSON using get_or_create."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default="fixtures/math_seed.json",
            help="Path to the fixture JSON (relative to BASE_DIR by default).",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force execution in production environment (requires confirmation).",
        )

    def handle(self, *args, **options):
        # ========================================
        # セキュリティチェック：本番環境での実行禁止
        # ========================================
        if not settings.DEBUG:
            # 本番環境（DEBUG=False）での実行を禁止
            if not options.get("force"):
                raise CommandError(
                    "⛔ 本番環境では seed_taxonomy は実行できません。\n"
                    "万が一本番環境で実行する必要がある場合は、"
                    "--force フラグを使用してください。\n"
                    "ただし、本番環境でのシード実行はデータ喪失のリスクがあります。"
                )
            # force オプション使用時の最終確認
            confirm = input(
                "⚠️  WARNING: 本番環境（本物のデータベース）でシードを実行しようとしています。\n"
                "これにより既存のデータが上書きされる可能性があります。\n\n"
                "本当に実行しますか？ (yes/no): "
            )
            if confirm.lower() != "yes":
                self.stdout.write(
                    self.style.WARNING("実行がキャンセルされました。")
                )
                return
            self.stdout.write(
                self.style.WARNING(
                    "⚠️  本番環境でのシード実行が開始されました。"
                )
            )
        raw_path = options["path"]
        path = raw_path
        if not os.path.isabs(raw_path):
            path = os.path.join(settings.BASE_DIR, raw_path)

        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f"Fixture not found: {path}"))
            return

        with open(path, "r", encoding="utf-8-sig") as handle:
            payload = json.load(handle)

        grade_map = {}
        subject_map = {}
        created_counts = {"grade": 0, "subject": 0, "tag": 0}

        for entry in self._filter_model(payload, "math_app.grade"):
            fields = entry.get("fields", {})
            code = fields.get("code")
            if not code:
                continue
            grade, created = Grade.objects.get_or_create(
                code=code,
                defaults={
                    "name": fields.get("name", ""),
                    "order": fields.get("order", 0),
                },
            )
            if created:
                created_counts["grade"] += 1
            grade_map[entry.get("pk")] = grade

        for entry in self._filter_model(payload, "math_app.subject"):
            fields = entry.get("fields", {})
            grade = grade_map.get(fields.get("grade"))
            if grade is None:
                continue
            name = fields.get("name")
            if not name:
                continue
            subject, created = Subject.objects.get_or_create(
                name=name,
                grade=grade,
                defaults={
                    "order": fields.get("order", 0),
                },
            )
            if created:
                created_counts["subject"] += 1
            subject_map[entry.get("pk")] = subject

        for entry in self._filter_model(payload, "math_app.tag"):
            fields = entry.get("fields", {})
            name = fields.get("name")
            if not name:
                continue
            grade = grade_map.get(fields.get("grade"))
            subject = subject_map.get(fields.get("subject"))
            tag, created = Tag.objects.get_or_create(
                name=name,
                grade=grade,
                subject=subject,
                defaults={
                    "order": fields.get("order", 0),
                },
            )
            if created:
                created_counts["tag"] += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Seed complete: "
                f"Grade +{created_counts['grade']}, "
                f"Subject +{created_counts['subject']}, "
                f"Tag +{created_counts['tag']}"
            )
        )

    @staticmethod
    def _filter_model(payload, model_label):
        label = model_label.lower()
        for entry in payload:
            if entry.get("model", "").lower() == label:
                yield entry
