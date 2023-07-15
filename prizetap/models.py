from django.db import models
from faucet.models import Chain
from django.utils import timezone
from authentication.models import NetworkTypes, UserProfile
from faucet.models import WalletAccount
from .utils import (
    raffle_hash_message,
    sign_hashed_message
)
from core.models import UserConstraint

# Create your models here.

class Constraint(UserConstraint):
    pass
    

class Raffle(models.Model):

    class Meta:
        models.UniqueConstraint(
            fields=['chain', 'contract', 'raffleId'], name="unique_raffle")

    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    contract = models.CharField(max_length=256)
    raffleId = models.BigIntegerField()
    signer = models.ForeignKey(WalletAccount, on_delete=models.DO_NOTHING)
    creator = models.CharField(max_length=256, null=True, blank=True)
    creator_url = models.URLField(max_length=255, null=True, blank=True)
    discord_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    image_url = models.URLField(max_length=255, null=True, blank=True)

    prize_amount = models.BigIntegerField()
    prize_asset = models.CharField(max_length=255)
    prize_name = models.CharField(max_length=100)
    prize_symbol = models.CharField(max_length=100)
    decimals = models.IntegerField(default=18)
    

    is_prize_nft = models.BooleanField(default=False)
    nft_id = models.BigIntegerField(null=True, blank=True)
    token_uri = models.TextField(null=True, blank=True)

    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE, related_name="raffles", null=True, blank=True
    )

    constraints = models.ManyToManyField(Constraint, blank=True, related_name="raffles")

    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    deadline = models.DateTimeField(null=True, blank=True)
    max_number_of_entries = models.IntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    @property
    def is_expired(self):
        if self.deadline is None:
            return False
        return self.deadline < timezone.now()

    @property
    def is_maxed_out(self):
        if self.max_number_of_entries is None:
            return False
        return self.max_number_of_entries <= self.number_of_entries

    @property
    def is_claimable(self):
        return not self.is_expired and not self.is_maxed_out and self.is_active

    @property
    def number_of_entries(self):
        return self.entries.filter(tx_hash__isnull=False).aggregate(
            TOTAL = models.Sum('multiplier'))['TOTAL'] or 0
    
    @property
    def winner(self):
        try:
            return self.entries.get(is_winner=True).user_profile
        except RaffleEntry.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.name}"
    
    def generate_signature(self, user: str, nonce: int = None, multiplier: int = None):
        assert self.raffleId and self.signer

        hashed_message = raffle_hash_message(
            user=user,
            raffleId=self.raffleId,
            nonce=nonce,
            multiplier=multiplier
        )

        return sign_hashed_message(
            hashed_message, self.signer.private_key
        )


class RaffleEntry(models.Model):
    class Meta:
        unique_together = (("raffle", "user_profile"),)
        verbose_name_plural = "raffle entries"

    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name="entries")
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="raffle_entries"
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    signature = models.CharField(max_length=1024, blank=True, null=True)
    multiplier = models.IntegerField(default=1)
    is_winner = models.BooleanField(blank=True, default=False)
    tx_hash = models.CharField(max_length=255, blank=True, null=True)
    claiming_prize_tx = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.raffle} - {self.user_profile}"

    @property
    def user(self):
        return self.user_profile.wallets.get(wallet_type=NetworkTypes.EVM).address
    
    @property
    def nonce(self):
        return self.pk

    def save(self, *args, **kwargs):
        if self.is_winner:
            try:
                entry = RaffleEntry.objects.get(is_winner=True, raffle=self.raffle)
                assert entry.pk == self.pk, "The raffle already has a winner"
            except RaffleEntry.DoesNotExist:
                pass
                    
        super().save(*args, **kwargs)
