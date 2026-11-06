from pathlib import Path

from app.models import Ledger


LEDGER_PATH = Path(__file__).resolve().parent.parent / "ledger.json"


def load_ledger(path: Path = LEDGER_PATH) -> Ledger:
    return Ledger.model_validate_json(path.read_text(encoding="utf-8"))
