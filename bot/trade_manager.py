
from api.oanda_api import OandaApi
from models.trade_decision import TradeDecision

def trade_is_open(pair, api: OandaApi):
    open_trades = api.get_open_trades()

    for trade in open_trades:
        if trade.instrument == pair:
            return trade

    return None

def place_trade(trade_decision: TradeDecision, api: OandaApi, log_message, log_error, trade_risk):
    ot = trade_is_open(trade_decision.pair, api)

    if ot is not None:
        log_message(f"Failed to place trade {trade_decision}, already open: {ot}", trade_decision.pair)
        return None

    trade_units = get_trade_units(api, trade_decision.pair, trade_decision.signal, trade_decision.loss, trade_risk, log_message)

    trade_id = api.place_trade(
        trade_decision.pair, 
        trade_units, 
        trade_decision.signal,
        trade_decision.sl, 
        trade_decision.tp
    )

    if trade_id is None:
        log_error(f"ERROR place {trade_decision}")
        log_message(f"ERROR place {trade_decision}", trade_decision.pair)
    else:
        log_message(f"Placed {trade_decision}", trade_decision.pair)