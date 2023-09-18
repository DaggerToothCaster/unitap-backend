from django.contrib import admin
from prizetap.models import *
from core.admin import UserConstraintBaseAdmin


class RaffleAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "creator"]

class RaffleٍEntryAdmin(admin.ModelAdmin):
    list_display = [
        "pk", 
        "raffle", 
        "get_wallet",
        "age",
    ]

    @admin.display(ordering='user_profile__wallets', description='Wallet')
    def get_wallet(self, obj):
        return obj.user_profile.wallets.get(wallet_type=NetworkTypes.EVM).address


admin.site.register(Raffle, RaffleAdmin)
admin.site.register(RaffleEntry, RaffleٍEntryAdmin)
admin.site.register(Constraint, UserConstraintBaseAdmin)
