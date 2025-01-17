import base64
import json

from rest_framework import serializers

from authentication.serializers import SimpleProfilerSerializer
from core.constraints import ConstraintVerification, get_constraint
from core.serializers import UserConstraintBaseSerializer
from faucet.serializers import SmallChainSerializer

from .constants import CONTRACT_ADDRESSES
from .models import Constraint, LineaRaffleEntries, Raffle, RaffleEntry, UserConstraint


class ConstraintSerializer(UserConstraintBaseSerializer, serializers.ModelSerializer):
    class Meta(UserConstraintBaseSerializer.Meta):
        ref_name = "RaffleConstraint"
        model = Constraint

    def get_params(self, constraint: UserConstraint):
        c_class: ConstraintVerification = get_constraint(constraint.name)
        return [p.name for p in c_class.param_keys()]


class SimpleRaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = [
            "pk",
            "name",
            "contract",
            "raffleId",
        ]
        read_only_fields = [
            "pk",
            "name",
            "contract",
            "raffleId",
        ]


class RaffleEntrySerializer(serializers.ModelSerializer):
    raffle = SimpleRaffleSerializer()
    user_profile = SimpleProfilerSerializer()
    chain = serializers.SerializerMethodField()
    wallet = serializers.SerializerMethodField()

    class Meta:
        model = RaffleEntry
        fields = [
            "pk",
            "chain",
            "raffle",
            "user_profile",
            "wallet",
            "created_at",
            "multiplier",
            "tx_hash",
            "claiming_prize_tx",
        ]
        read_only_fields = [
            "pk",
            "chain",
            "raffle",
            "user_profile",
            "wallet",
            "created_at",
            "multiplier",
        ]

    def get_chain(self, entry: RaffleEntry):
        return entry.raffle.chain.chain_id

    def get_wallet(self, entry: RaffleEntry):
        return entry.user_profile.wallets.get(wallet_type=entry.raffle.chain.chain_type).address


class WinnerEntrySerializer(serializers.ModelSerializer):
    user_profile = SimpleProfilerSerializer()
    wallet = serializers.SerializerMethodField()

    class Meta:
        model = RaffleEntry
        fields = ["pk", "user_profile", "wallet", "created_at", "multiplier", "tx_hash", "claiming_prize_tx"]
        read_only_fields = [
            "pk",
            "user_profile",
            "wallet",
            "created_at",
            "multiplier",
        ]

    def get_wallet(self, entry: RaffleEntry):
        return entry.user_profile.wallets.get(wallet_type=entry.raffle.chain.chain_type).address


class CreateRaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = "__all__"

        read_only_fields = [
            "pk",
            "raffleId",
            "creator_profile",
            "created_at",
            "status",
            "rejection_reason",
            "is_active",
        ]

    def validate(self, data):
        constraints = data["constraints"]
        constraint_params = json.loads(base64.b64decode(data["constraint_params"]))
        data["constraint_params"] = base64.b64decode(data["constraint_params"]).decode("utf-8")
        reversed_constraints = []
        if "reversed_constraints" in data:
            reversed_constraints = str(data["reversed_constraints"]).split(",")
        if len(constraints) != 0:
            for c in constraints:
                constraint_class: ConstraintVerification = get_constraint(c.name)
                try:
                    if len(constraint_class.param_keys()) != 0:
                        constraint_class.is_valid_param_keys(constraint_params[c.name])
                except KeyError as e:
                    raise serializers.ValidationError({"constraint_params": [{f"{c.name}": str(e)}]})
        valid_constraints = [str(c.pk) for c in constraints]
        if len(reversed_constraints) > 0:
            for c in reversed_constraints:
                if c not in valid_constraints:
                    raise serializers.ValidationError({"reversed_constraints": [{f"{c}": "Invalid constraint pk"}]})
        if "winners_count" in data and data["winners_count"] > data["max_number_of_entries"]:
            raise serializers.ValidationError({"winners_count": "Invalid value"})
        valid_chains = list(CONTRACT_ADDRESSES.keys())
        chain_id = data["chain"].chain_id
        if chain_id not in valid_chains:
            raise serializers.ValidationError({"chain": "Invalid value"})
        valid_contracts = list(CONTRACT_ADDRESSES[chain_id].values())
        if data["contract"] not in valid_contracts:
            raise serializers.ValidationError({"contract": "Invalid value"})
        data["creator_profile"] = self.context["user_profile"]
        return data


class RaffleSerializer(serializers.ModelSerializer):
    chain = SmallChainSerializer()
    winner_entry = WinnerEntrySerializer()
    user_entry = serializers.SerializerMethodField()
    constraints = ConstraintSerializer(many=True, read_only=True)
    creator_profile = SimpleProfilerSerializer()

    class Meta:
        model = Raffle
        fields = [
            "pk",
            "name",
            "description",
            "necessary_information",
            "creator_name",
            "creator_profile",
            "creator_address",
            "creator_url",
            "discord_url",
            "twitter_url",
            "email_url",
            "telegram_url",
            "image_url",
            "prize_amount",
            "prize_asset",
            "prize_name",
            "prize_symbol",
            "decimals",
            "is_prize_nft",
            "nft_ids",
            "token_uri",
            "chain",
            "contract",
            "raffleId",
            "constraints",
            "constraint_params",
            "reversed_constraints",
            "created_at",
            "start_at",
            "deadline",
            "max_number_of_entries",
            "status",
            "rejection_reason",
            "tx_hash",
            "is_active",
            "winner_entry",
            "is_expired",
            "is_claimable",
            "user_entry",
            "number_of_entries",
            "number_of_onchain_entries",
            "max_multiplier",
            "winners_count",
        ]

    def get_user_entry(self, raffle: Raffle):
        try:
            return RaffleEntrySerializer(raffle.entries.get(user_profile=self.context["user"])).data
        except RaffleEntry.DoesNotExist:
            return None


class LineaRaffleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaRaffleEntries
        fields = "__all__"
