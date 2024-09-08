from rest_framework import serializers
from .models import CoinDetails


class CoindetailSerializer(serializers.ModelSerializer):
    coinvalue_entryrange_mapping = serializers.SerializerMethodField()

    class Meta:
        model = CoinDetails
        fields = [
            "category",
            "id",
            "label",
            "description",
            "Image",
            "coinvalue_entryrange_mapping",
            "coming_soon",
        ]

    def get_coinvalue_entryrange_mapping(self, instance):
        coinvalue_entryrange_mapping = {}

        if instance.coinvalue:
            coinvalue_entryrange_mapping[str(instance.coinvalue)] = instance.entryrange

        if instance.coinvalue1:
            coinvalue_entryrange_mapping[
                str(instance.coinvalue1)
            ] = instance.entryrange1

        if instance.coinvalue2:
            coinvalue_entryrange_mapping[
                str(instance.coinvalue2)
            ] = instance.entryrange2

        return coinvalue_entryrange_mapping
