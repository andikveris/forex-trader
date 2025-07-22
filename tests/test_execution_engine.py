import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.core.base_classes import BaseExecutionEngine
from src.core.interfaces import TradingSignal

class DummyExecutionEngine(BaseExecutionEngine):
    """Simple engine with deterministic pricing and commissions"""
    def __init__(self, exit_price: float, *args, **kwargs):
        super().__init__('DummyEngine', *args, **kwargs)
        self._exit_price = exit_price

    def _get_execution_price(self, signal: TradingSignal) -> float:
        return signal.price

    def _get_exit_price(self, trade):
        return self._exit_price

    def _calculate_commission(self, position_size: float, price: float) -> float:
        # Constant commission to make calculations predictable
        return 1.0


def test_close_position_updates_balance_without_extra_exit_commission():
    engine = DummyExecutionEngine(exit_price=20, config={'initial_balance': 1000})
    signal = TradingSignal(
        pair='EURUSD',
        signal='BUY',
        strategy='test',
        confidence=1.0,
        price=10,
        timestamp=datetime.now()
    )
    trade = engine.execute_trade(signal, position_size=1)
    balance_after_entry = engine.get_account_balance()

    closed_trade = engine.close_position(trade.trade_id)
    expected_balance = balance_after_entry + closed_trade.profit_loss
    assert engine.get_account_balance() == expected_balance
