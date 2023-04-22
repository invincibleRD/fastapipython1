import datetime
import json

def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "password": item["password"]
    }


def tradesEntity(entity) -> list:
    return [tradeEntity(item) for item in entity]

def tradeDetails(item)->dict:
    return{
        "buySellIndicator":item["buySellIndicator"],
        "price":item["price"],
        "quantity":item["quantity"]
    }

def tradeEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "assetClass": item["asset_class"],
        "counterParty": item["counterparty"],
        "instrumentId": item["instrument_id"],
        "instrumentName": item["instrument_name"],
        "tradeDateTime": item["trade_date_time"],
        "tradeDetails": tradeDetails(item["trade_details"]),
        "tradeId": item["trade_id"],
        "trader": item["trader"]
    }


