from django.contrib import admin
from core.admin import UserConstraintBaseAdmin
from .models import *

# Register your models here.


class TokenDistributionAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "token",
        "token_address",
        "amount",
        "chain",
        "created_at",
        "deadline",
    ]


class TokenDistributionClaimAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "token_distribution",
        "status",
        "user_profile",
        "age",
    ]
    list_filter = ["token_distribution", "status"]


admin.site.register(Constraint, UserConstraintBaseAdmin)
admin.site.register(TokenDistribution, TokenDistributionAdmin)
admin.site.register(TokenDistributionClaim, TokenDistributionClaimAdmin)
