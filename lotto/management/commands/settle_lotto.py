from collections import Counter
from django.core.management.base import BaseCommand, CommandError
from lotto.models import Draw, Ticket
from lotto.services import score

class Command(BaseCommand):
    help = "지정 회차의 모든 티켓을 채점하고 등수를 저장합니다."

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="회차 번호 (예: 1)")

    def handle(self, *args, **opts):
        number = opts["number"]
        try:
            draw = Draw.objects.get(number=number)
        except Draw.DoesNotExist:
            raise CommandError(f"{number}회 Draw가 없습니다. 먼저 생성/추첨하세요.")

        if not draw.winning_numbers:
            raise CommandError(f"{number}회는 아직 당첨 번호가 없습니다. draw_lotto 먼저 실행하세요.")

        qs = Ticket.objects.filter(draw=draw)
        if not qs.exists():
            self.stdout.write("해당 회차에 티켓이 없습니다.")
            return

        counter = Counter()
        for t in qs:
            result = score(t.picks, draw.winning_numbers)
            t.match_count = result["match_count"]
            t.rank = result["rank"]
            t.save(update_fields=["match_count", "rank"])
            counter[t.rank] += 1

        # 요약 출력
        lines = [f"{number}회 정산 결과",
                 f"  1등: {counter[1]}",
                 f"  2등: {counter[2]}",
                 f"  3등: {counter[3]}",
                 f"  4등: {counter[4]}",
                 f"  꽝 : {counter[0]}"]
        self.stdout.write("\n".join(lines))