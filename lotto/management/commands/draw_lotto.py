from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from lotto.models import Draw
from lotto.services import quick_pick

class Command(BaseCommand):
    help = "지정 회차를 추첨하고 당첨 번호를 저장합니다. (status=SCHEDULED -> DONE)"

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="회차 번호 (예: 1)")
        parser.add_argument("--date", type=str, help="YYYY-MM-DD (없으면 오늘)")

    def handle(self, *args, **opts):
        number = opts["number"]
        date_str = opts.get("date")
        if date_str:
            try:
                draw_date = timezone.datetime.fromisoformat(date_str).date()
            except Exception:
                raise CommandError("날짜 형식이 올바르지 않습니다. 예: 2025-12-01")
        else:
            draw_date = timezone.now().date()

        draw, _ = Draw.objects.get_or_create(number=number, defaults={"draw_date": draw_date})
        if draw.winning_numbers:
            self.stdout.write(self.style.WARNING(f"{number}회는 이미 추첨됨: {draw.winning_numbers}"))
            return

        nums = quick_pick()
        draw.winning_numbers = nums
        draw.status = "DONE"
        draw.draw_date = draw_date
        draw.save()

        self.stdout.write(self.style.SUCCESS(f"{number}회 추첨 완료: {nums} (status=DONE)"))