from BU.futures.api import auth


def bulkOrders(self, symbol, side, price, volume, systemOrderType):

    params = [{
        "side": side,
        "price": price,
        "volume": volume,
        "systemOrderType": systemOrderType
    }]
    path = f'/openapi/exchange/{symbol}/bulkOrders'

    res = self.request(method='POST', params=params, path=path, auth=True)
    return res