"""CLI: train the VisaFit screener model."""
from __future__ import annotations

import json

from visafit.ml import train


def main() -> None:
    meta = train()
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
