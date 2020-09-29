
import logging
import simplejson as json
from typing import Any, Dict

import pandas as pd


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Checker(object):
    """something"""

    def __init__(
        self, config, strict=True, silent=False
    ):
        super(Checker, self).__init__()
        self.config = self._read_json(config)
        self.strict = strict
        self.silent = silent

    @staticmethod
    def _read_json(filename: str) -> Dict[str, Any]:
        """"""
        with open(filename, "r") as f:
            config = json.load(f)

        return config

    def check(self, frame: pd.DataFrame) -> bool:
        """something"""
        results = []

        for col in self.config.keys():
            logging.info(f"Column: {col}")

            if col not in frame.columns:
                logging.warn("Column not found.")
                continue

            expected = set(self.config[col])
            observed = set(frame[col].unique())
            result = expected.symmetric_difference(observed)

            logging.info(f"Result: {result}")
            results.append(result == set())

        return all(results)


if __name__ == '__main__':
    cc = Checker("examples/pkmn.json")

    df = pd.read_csv("examples/pkmn_stats.csv")

    print(cc.check(df))
