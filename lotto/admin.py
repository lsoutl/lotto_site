from django.contrib import admin
from .models import Draw, Ticket

@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ("number", "draw_date", "status")
    list_filter = ("status",)
    search_fields = ("number",)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("user", "draw", "is_auto", "purchased_at")
    list_filter = ("draw", "is_auto")
    search_fields = ("user__username",)