from fastapi import APIRouter, HTTPException
from datetime import datetime
from models.trade import Trade
from config.db import client
from mongopush import putdata
from schemas.trade import tradeEntity, tradesEntity
from typing import List
import math

trade = APIRouter()
con = client.TradingCompany.trades2


@trade.get("/trades", response_model=List[Trade])
async def get_trades() -> List[Trade]:
    print("all")
    trades = con.find()
    return [Trade(**trade) for trade in trades]


@trade.get('/trades/search={query}', response_model=List[Trade])
async def search_trades(query: str) -> List[Trade]:
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


@trade.get("/trades/{id}", response_model=Trade)
async def get_trade_by_id(id: str) -> Trade:
    print("find by ID")
    trade = con.find_one({"tradeId": id})
    if trade is None:
        raise HTTPException(
            status_code=404, detail="Trade not found/Invalid trade ID")
    return Trade(**trade)


@trade.get("/tradesfiltered", response_model=List[Trade])
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
async def get_paginated_trades(page: int = 1, page_size: int = 5) -> dict:
    res = {}
    all_trades = con.find()
    trades = [Trade(**trade) for trade in all_trades]
    res["pageNumber"] = page
    res["totalPages"]=math.ceil(trades.__len__()/page_size)
    res["totalTrades"] = trades.__len__()
    data=con.find().skip((page-1)*page_size).limit(page_size)
    trades=[Trade(**trade) for trade in data]
    if(trades=={} or page>res["totalPages"]):
        res["trades"]="Please provide correct page number"
    else:
        res["trades"]=trades
    return res


# @trade.get("/tradesfiltered")
# async def get_filtered_trades(assetClass: str = None, start: datetime = None, end: datetime = None,
#                       minPrice: float = None, maxPrice: float = None, tradeType: str = None,pageSize:int=0,limit:int=10):
#     filters = {}
#     if assetClass:
#         filters["asset_class"] = assetClass
#     if start:
#         filters["tradeDateTime"] = {"$gte": start}
#     if end:
#         if "tradeDateTime" in filters:
#             filters["tradeDateTime"]["$lte"] = end
#         else:
#             filters["tradeDateTime"] = {"$lte": end}
#     if minPrice:
#         filters["tradeDetails.price"] = {"$gte": minPrice}
#     if maxPrice:
#         if "tradeDetails.price" in filters:
#             filters["tradeDetails.price"]["$lte"] = maxPrice
#         else:
#             filters["tradeDetails.price"] = {"$lte": maxPrice}
#     if tradeType:
#         filters["trade_details.buySellIndicator"] = tradeType
#     print(filters)
#     print("filtered data ")
#     if(pageSize!=0):
#         res=[]
#         for i in range(0,limit):
#             res.append(tradesEntity(con.find(filters).skip(i).limit(pageSize)))
#             if(i+pageSize>=limit):
#                 pageSize=limit-1
#             i+=pageSize
#         print("pagination  applied")
#         return res
#     return tradesEntity(con.find(filters).limit(limit))


# @trade.get("/pagination")
# async def get_paginated_trades(limit: int = 10, size: int = 0):
#     # tradesEntity(con.find().skip(skip).limit(limit))
#     res={}
#     for i in range(0,limit,size):
#         res.append(tradesEntity(con.find().skip(i).limit(size)))
#     print("pagination  applied")
#     return res
    # return tradesEntity(con.find(filters))


# @trade.get("/trades/search")
# async def search_trades(query: str):
#     query={
#         "$or": [
#             {"counterparty": {"$regex": f".*{query}.*", "$options": "i"}},
#             {"instrument_id": {"$regex": f".*{query}.*", "$options": "i"}},
#             {"instrument_name": {"$regex": f".*{query}.*", "$options": "i"}},
#             {"trader": {"$regex": f".*{query}.*", "$options": "i"}},
#         ]
#     }
#     return tradesEntity(con.find(query))


# @trade.get('/tradeslist')
# async def list_trades():
#     # print(client.TradingCompany.trades.find())
#     # print(tradesEntity(client.TradingCompany.trades.find()))
#     print("list all")
#     return tradesEntity(con.find())


# @trade.get('/trades/id={id}')
# async def find_by_ID(id: str):
#     print("find by ID")
#     return tradesEntity(con.find({"trade_id":id}))


# # @trade.get('/tradeslist')
# # async def find_by_tradeID(id: str = None, counterparty:str=None,instrumentId:str=None,instrumentName:str=None,trader:str=None):
# #     result =[]
# #     if(id):
# #         return tradesEntity(con.find_one({"trade_id":id}))
# #         # cursor = collection.find().limit(10)
# #         # for doc in cursor:
# #         #     result.append(doc)
# #     return {"trades": result}

#     # return tradesEntity(client.TradingCompany.trades.find({"trade_id": trader_id}))


# # @trade.post('/')
# # async def create_user(user:User):
# #     client.test.user.insert_one(dict(user))
# #     return  {"Inserted_data": dict(user)}

#     # putdata()
