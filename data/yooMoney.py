from yoomoney import Authorize

Authorize(
    client_id='70DA5718644333D79ABE68C43FAA896E7ABB3FE0D1E951EE7C67E5818DC321E6',
    redirect_uri='https://t.me/lazzat_163_Bot',
    scope= ["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
)