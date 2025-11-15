from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Draw, Ticket
from .forms import ManualPurchaseForm
from .services import quick_pick

def index(request):
    draws = Draw.objects.all()
    return render(request, "lotto/index.html", {"draws": draws})

def my_tickets(request):
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/my/tickets/")  # 임시: admin 로그인 재활용
    tickets = Ticket.objects.filter(user=request.user).select_related("draw")
    return render(request, "lotto/my_tickets.html", {"tickets": tickets})

def draw_result(request, draw):
    d = get_object_or_404(Draw, number=draw)
    winners = Ticket.objects.filter(draw=d, rank__gt=0).select_related("user").order_by("rank", "-purchased_at")
    return render(request, "lotto/draw_result.html", {"draw": d, "winners": winners})

@login_required
def buy_auto(request, draw):
    d = get_object_or_404(Draw, number=draw, status="SCHEDULED")
    Ticket.objects.create(user=request.user, draw=d, is_auto=True, picks=quick_pick())
    return redirect("my_tickets")

@login_required
def buy_manual(request, draw):
    d = get_object_or_404(Draw, number=draw, status="SCHEDULED")
    form = ManualPurchaseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Ticket.objects.create(user=request.user, draw=d, is_auto=False, picks=form.cleaned_data["numbers"])
        return redirect("my_tickets")
    return render(request, "lotto/buy_manual.html", {"form": form, "draw": d})