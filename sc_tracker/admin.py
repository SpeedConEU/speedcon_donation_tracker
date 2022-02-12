from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from .models import Marathon, Donor, Donation, Run, Runner


class RunInLine(SortableInlineAdminMixin, admin.StackedInline):
    model = Run
    extra = 0
    classes = ("collapse", "collapse-entry")
    show_change_link = True
    fieldsets = (
        (None, {"fields": ("game_name",)}),
        (
            "More",
            {
                "fields": (
                    "category",
                    "platform",
                    "estimate",
                    "additional_setup",
                    "runners",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Marathon)
class MarathonAdmin(admin.ModelAdmin):
    search_fields = ("slug", "name")
    list_display = ("name", "start_time", "recipient_name", "accept_donations")
    list_editable = ("accept_donations",)
    inlines = [RunInLine]


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    exclude = ("payer_id",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    exclude = ("txn_id",)


@admin.register(Runner)
class RunnerAdmin(admin.ModelAdmin):
    pass


# @admin.register(Run)
# class RunAdmin(admin.ModelAdmin):
#    pass
