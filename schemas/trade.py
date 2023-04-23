import datetime
import json


def tradesEntity(entity) -> list:
    return [tradeEntity(item) for item in entity]


def tradeDetails(item) -> dict:
    return {
        "buySellIndicator": item["buySellIndicator"],
        "price": item["price"],
        "quantity": item["quantity"]
    }


def tradeEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "assetClass": item["assetClass"],
        "counterParty": item["counterparty"],
        "instrumentId": item["instrumentId"],
        "instrumentName": item["instrumentName"],
        "tradeDateTime": item["tradeDateTime"],
        "tradeDetails": tradeDetails(item["tradeDetails"]),
        "tradeId": item["tradeId"],
        "trader": item["trader"]
    }
