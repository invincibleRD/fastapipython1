# FastAPI Assignment

This is a FastAPI assignment by steeleye.

## Getting Started

1. Clone this repository to your local machine.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Start the API with `uvicorn main:app --reload`.

The API should now be accessible at `http://localhost:8000`.

## Endpoints

### List Trades

Retrieve a list of trades.

**Endpoint:** `/trades`

**Method:** `GET`

**Query Parameters:**
- `page`: Page number for pagination.
- `perPage`: Number of trades to show per page.

**Response:**
- `trades`: List of trades.

### Get Trade by ID

Retrieve information about a single trade.

**Endpoint:** `/trades/{{id}}`

**Method:** `GET`

**Path Parameters:**
- `id`: ID of the trade.

**Example:**
- `/trades/3`

**Response:**
- `trade`: Information about the trade.

### Search Trades

Search for trades based on certain criteria.

**Endpoint:** 
`/trades/search`

**Method:** `GET`

**Query Parameters:**
- `search`: Text to search for in any of the fields `counterparty`, `instrumentId`, `instrumentName`, or `trader`.

**Example:**
- `/trades/search=apple`

**Response:**
- `trades`: List of trades that match the search criteria.

### Filter Trades

Filter trades based on certain criteria.

**Endpoint:** `/tradesfiltered`

**Method:** `GET`

**Query Parameters:**
- `assetClass`: Asset class of the trade.
- `start`: Minimum date for the `tradeDateTime` field.
- `end`: Maximum date for the `tradeDateTime` field.
- `minPrice`: Minimum value for the `tradeDetails.price` field.
- `maxPrice`: Maximum value for the `tradeDetails.price` field.
- `tradeType`: Value of the `tradeDetails.buySellIndicator` field.

**Response:**
- `/tradesfiltered?&minPrice=100&maxPrice=500&tradeType=buy
`

**Response:**
- `trades`: List of trades that match the filter criteria.

## Pagination

To paginate the results of the `/paginatedtrades` endpoint, you can use the `page` and `perPage` query parameters.

For example, to retrieve the second page of trades with 10 trades per page, you would use the following endpoint:

**Example**
- `/paginatedtrades?page=1&page_size=5`


