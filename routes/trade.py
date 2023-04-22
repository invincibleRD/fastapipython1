from fastapi import APIRouter,HTTPException

from models.trade import Trade
from config.db import client
from schemas.trade import tradeEntity, tradesEntity
from mongopush import putdata
from typing import List

trade = APIRouter()
con=client.TradingCompany.trades




# Endpoint to fetch a list of trades
@trade.get("/trades")
async def get_trades():
    print("all")
    return tradesEntity(con.find())

@trade.get('/trades/search={query}')
async def search(query:str):
    query = {
        "$or": [
            {"counterparty": {"$regex": f".*{query}.*", "$options": "i"}},
            {"instrument_id": {"$regex": f".*{query}.*", "$options": "i"}},
            {"instrument_name": {"$regex": f".*{query}.*", "$options": "i"}},
            {"trader": {"$regex": f".*{query}.*", "$options": "i"}},
        ]
    }
    print("search by quary")
    return tradesEntity(client.TradingCompany.trades.find(query))
# Endpoint to fetch a single trade by id
@trade.get("/trades/{id}")
async def get_trade_by_id(id: str):
    print("find by ID")
    return tradesEntity(con.find({"trade_id":id}))
    # if not restrade:
    #     raise HTTPException(status_code=404, detail="Trade not found")
    # return restrade

# Endpoint to search across trades
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
