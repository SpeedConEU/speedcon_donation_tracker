from django.contrib import admin

from .models import Marathon, Donor, Donation


@admin.register(Marathon)
class MarathonAdmin(admin.ModelAdmin):
    search_fields = ("slug", "name")
    list_display = ("name", "start_time", "recipient_name", "accept_donations")
    list_editable = ("accept_donations",)


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    exclude = ("payer_id",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    exclude = ("txn_id",)
