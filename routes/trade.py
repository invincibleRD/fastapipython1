from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.trade import Trade
from config.db import client
from schemas.trade import tradeEntity, tradesEntity
from typing import List
import math


trade = APIRouter()
con = client.TradingCompany.trades2


@trade.get("/trades",)
async def get_trades():
    print("all")
    trades = con.find()
    return [Trade(**trade) for trade in trades]


@trade.get('/trades/search={query}')
async def search_trades(query: str):
    query = {
        "$or": [
            {"counterparty": {"$regex": f".*{query}.*", "$options": "i"}},
            {"instrumentId": {"$regex": f".*{query}.*", "$options": "i"}},
            {"instrumentName": {"$regex": f".*{query}.*", "$options": "i"}},
            {"trader": {"$regex": f".*{query}.*", "$options": "i"}},
        ]
    }
    print("search by quary")
    trades = con.find(query)
    return [Trade(**trade) for trade in trades]


@trade.get("/trades/{id}")
async def get_trade_by_id(id: str):
    print("find by ID")
    trade = con.find_one({"tradeId": id})
    if trade is None:
        raise HTTPException(
            status_code=404, detail="Trade not found/Invalid trade ID")
    return Trade(**trade)


@trade.get("/tradesfiltered")
async def get_filtered_trades(assetClass: str = None, start: datetime = None, end: datetime = None,
                              minPrice: float = None, maxPrice: float = None, tradeType: str = None,
                              ) -> List[Trade]:
    filters = {}
    if assetClass:
        filters["assetClass"] = assetClass
    if start:
        filters["tradeDateTime"] = {"$gte": start}
    if end:
        if "tradeDateTime" in filters:
            filters["tradeDateTime"]["$lte"] = end
        else:
            filters["tradeDateTime"] = {"$lte": end}
    if minPrice:
        filters["tradeDetails.price"] = {"$gte": minPrice}
    if maxPrice:
        if "tradeDetails.price" in filters:
            filters["tradeDetails.price"]["$lte"] = maxPrice
        else:
            filters["tradeDetails.price"] = {"$lte": maxPrice}
    if tradeType:
        filters["tradeDetails.buySellIndicator"] = tradeType
    print(filters)
    print("filtered data ")
    trades = con.find(filters)
    return [Trade(**trade) for trade in trades]


@trade.get("/paginatedtrades")
async def get_paginated_trades(page: int = 1, perPage: int = 5):
    res = {}
    all_trades = con.find()
    trades = [Trade(**trade) for trade in all_trades]
    res["pageNumber"] = page
    res["totalPages"] = math.ceil(trades.__len__()/perPage)
    res["totalTrades"] = trades.__len__()
    data = con.find().skip((page-1)*perPage).limit(perPage)
    trades = [Trade(**trade) for trade in data]
    if (trades == {} or page > res["totalPages"]):
        res["trades"] = "Please provide correct page number"
    else:
        res["trades"] = trades
    return res
