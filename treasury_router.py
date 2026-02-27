import logging
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] Treasury Router: %(message)s')
logger = logging.getLogger("TreasuryRouter")

class TreasuryRouter:
    """
    Mathematically divides incoming revenue into two streams:
    1. The AI's Operations Wallet (for API costs and infrastructure scaling).
    2. The Creator Dividend (personal payout).
    """

    def __init__(self, target_operations_float: float = 50.00, ledger_path: str = "ledger.json"):
        # The AI will always try to keep exactly this amount in its ops wallet.
        self.target_operations_float = target_operations_float
        self.ledger_path = ledger_path
        self._load_ledger()

    def _load_ledger(self):
        """Loads balances from persistent storage."""
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                data = json.load(f)
                self.operations_wallet_balance = data.get("ops_balance", 0.0)
                self.creator_dividend_balance = data.get("creator_balance", 0.0)
        else:
            self.operations_wallet_balance = 0.0
            self.creator_dividend_balance = 0.0
            self._save_ledger()

    def _save_ledger(self):
        """Saves current balances to persistent storage."""
        data = {
            "ops_balance": self.operations_wallet_balance,
            "creator_balance": self.creator_dividend_balance,
            "last_updated": os.path.getmtime(self.ledger_path) if os.path.exists(self.ledger_path) else time.time()
        }
        with open(self.ledger_path, 'w') as f:
            json.dump(data, f, indent=4)

    def process_incoming_revenue(self, amount: float):
        """Routes incoming revenue intelligently based on operational needs."""
        logger.info(f"Processing new revenue event: ${amount:.2f}")
        
        deficit = self.target_operations_float - self.operations_wallet_balance
        
        if deficit > 0:
            # AI needs funds to hit its operational baseline.
            if amount >= deficit:
                # Top up the ops wallet to max, send the rest to creator
                self.operations_wallet_balance += deficit
                remainder = amount - deficit
                self.creator_dividend_balance += remainder
                logger.info(f"Topped up Ops Wallet by ${deficit:.2f}. Sent ${remainder:.2f} to Creator Dividend.")
            else:
                # Not enough to top up completely, AI takes everything
                self.operations_wallet_balance += amount
                logger.info(f"All incoming funds (${amount:.2f}) retained by Ops Wallet to meet float deficit.")
        else:
            # Ops wallet is full. All funds go to the creator.
            self.creator_dividend_balance += amount
            logger.info(f"Ops Wallet full. Entire ${amount:.2f} routed to Creator Dividend.")
            
        self._save_ledger()
        self.print_ledgers()

    def process_drawdown(self, amount: float):
        """Deducts trading losses. Drains the ops wallet first, then the creator dividend."""
        logger.warning(f"Processing drawdown event: -${amount:.2f}")
        
        if self.operations_wallet_balance >= amount:
            self.operations_wallet_balance -= amount
            logger.warning(f"Ops Wallet absorbed the entire loss (${amount:.2f}).")
        else:
            remaining_loss = amount - self.operations_wallet_balance
            logger.warning(f"Ops Wallet wiped out (Deducted ${self.operations_wallet_balance:.2f}).")
            self.operations_wallet_balance = 0.0
            
            if self.creator_dividend_balance >= remaining_loss:
                self.creator_dividend_balance -= remaining_loss
                logger.warning(f"Remaining loss (${remaining_loss:.2f}) deducted from Creator Dividend.")
            else:
                logger.critical(f"CATASTROPHIC LOSS: Entire treasury wiped. Deficit: -${remaining_loss - self.creator_dividend_balance:.2f}")
                self.creator_dividend_balance = 0.0
                
        self._save_ledger()
        self.print_ledgers()

    def print_ledgers(self):
        """Prints current internal balances."""
        logger.info(f"--- LEDGER UPDATE ---")
        logger.info(f"Operations Wallet    : ${self.operations_wallet_balance:.2f} (Target: ${self.target_operations_float:.2f})")
        logger.info(f"Creator Dividend     : ${self.creator_dividend_balance:.2f}")
        logger.info(f"---------------------")

import time

if __name__ == "__main__":
    router = TreasuryRouter(target_operations_float=50.00)
    router.print_ledgers()
    
    logger.info("Treasury Router active and monitoring ledgers...")
    try:
        while True:
            # In a real system, this would listen to a queue or check an API.
            # Here we just keep the process alive so the Daemon doesn't restart it endlessly.
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Treasury Router shutting down.")
