from datetime import timedelta
from django.db import models
import uuid
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedCharField
import binascii
from bip_utils import Bip44Coins, Bip44
from brightIDfaucet.settings import BRIGHT_ID_INTERFACE


class WalletAccount(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    private_key = EncryptedCharField(max_length=100)

    @property
    def address(self):
        node = Bip44.FromPrivateKey(binascii.unhexlify(self.private_key), Bip44Coins.ETHEREUM)
        return node.PublicKey().ToAddress()

    def __str__(self) -> str:
        return "%s - %s" % (self.name, self.address)

    @property
    def main_key(self):
        return self.private_key


class BrightUserManager(models.Manager):

    def get_or_create(self, address):
        try:
            return super().get_queryset().get(address=address)
        except BrightUser.DoesNotExist:
            _user = BrightUser(address=address, _sponsored=True)

            # don't create user if sponsorship fails
            # so user can retry connecting their wallet
            if BRIGHT_ID_INTERFACE.sponsor(str(_user.context_id)):
                _user.save()
                return _user


class BrightUser(models.Model):
    PENDING = "0"
    VERIFIED = "1"

    states = ((PENDING, "Pending"),
              (VERIFIED, "Verified"))

    address = models.CharField(max_length=45, unique=True)
    context_id = models.UUIDField(default=uuid.uuid4, unique=True)

    _verification_status = models.CharField(max_length=1, choices=states, default=PENDING)
    _sponsored = models.BooleanField(default=False)

    objects = BrightUserManager()

    def __str__(self):
        return "%d - %s" % (self.pk, self.address)

    @property
    def verification_url(self, bright_interface=BRIGHT_ID_INTERFACE):
        return bright_interface.get_verification_link(str(self.context_id))

    @property
    def verification_status(self):
        if self._verification_status == self.VERIFIED:
            return self.VERIFIED
        return self.get_verification_status()

    def get_verification_status(self) -> states:
        is_verified = BRIGHT_ID_INTERFACE.get_verification_status(str(self.context_id))
        if is_verified:
            self._verification_status = self.VERIFIED
            self.save()
        return self._verification_status

    def get_verification_url(self) -> str:
        return BRIGHT_ID_INTERFACE.get_verification_link(str(self.context_id))


class ClaimReceipt(models.Model):
    MAX_PENDING_DURATION = 15  # minutes
    PENDING = '0'
    VERIFIED = '1'
    REJECTED = '2'

    states = ((PENDING, "Pending"),
              (VERIFIED, "Verified"),
              (REJECTED, "Rejected")
              )

    chain = models.ForeignKey("Chain", related_name="claims", on_delete=models.PROTECT)
    bright_user = models.ForeignKey(BrightUser, related_name="claims", on_delete=models.PROTECT)

    _status = models.CharField(max_length=1, choices=states, default=PENDING)

    amount = models.BigIntegerField()
    datetime = models.DateTimeField()
    tx_hash = models.CharField(max_length=100, blank=True, null=True)

    def is_expired(self):
        return timezone.now() - self.datetime > timedelta(minutes=self.MAX_PENDING_DURATION)

    def status(self) -> states:
        return self._status


class Chain(models.Model):
    chain_name = models.CharField(max_length=255)
    chain_id = models.CharField(max_length=255, unique=True)

    native_currency_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    decimals = models.IntegerField(default=18)

    explorer_url = models.URLField(max_length=255, blank=True, null=True)
    rpc_url = models.URLField(max_length=255, blank=True, null=True)
    logo_url = models.URLField(max_length=255, blank=True, null=True)
    rpc_url_private = models.URLField(max_length=255, blank=True, null=True)

    max_claim_amount = models.BigIntegerField()

    poa = models.BooleanField(default=False)

    fund_manager_address = models.CharField(max_length=255, blank=True, null=True)
    wallet = models.ForeignKey(WalletAccount, related_name="chains", blank=True, null=True,
                               on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.pk} - {self.symbol}:{self.chain_id}"
