import re
from typing import override

from LivinGrimoirePacket.AXPython import RailChatBot


class PopulatorFunc:
    def __init__(self):
        self.regex = ""

    def populate(self, railbot: RailChatBot, str1: str):
        _ = self
        _ = railbot
        _ = str1



class RailChatBotPopulator:
    def __init__(self, railbot:RailChatBot):
        self.railbot = railbot
        self.catch: set[str] = set()
        self.funcs: dict[str, PopulatorFunc] = {}  # regext, func

    def add_func(self, func: PopulatorFunc):
        if len(func.regex)>0:
            self.funcs[func.regex] = func

    def populate(self, str1: str):
        if str1 in self.catch:
            return
        self.catch.add(str1)
        for regex, func in self.funcs.items():
            self.funcs[regex].populate(self.railbot,str1)

class PricePerUnit(PopulatorFunc):
    def __init__(self):
        super().__init__()
        self.regex = "price per unit"
    @override
    @override
    def populate(self, railbot: RailChatBot, str1: str):
        """
        Extracts product and cost-per-unit from strings like:
        'apples costs 10.99 for 2 units'
        Returns 5 instead of 5.00 for whole numbers.
        """

        pattern = (
            r"^(?P<product>\w+)\s+costs\s+"
            r"(?P<cost>\d+(?:\.\d+)?)\s+for\s+"
            r"(?P<units>\d+)\s+units$"
        )

        clean = str1.strip()
        match = re.match(pattern, clean, re.IGNORECASE)
        if not match:
            return False

        product = match.group("product")
        cost = float(match.group("cost"))
        units = int(match.group("units"))

        cost_per_unit = cost / units

        # Format with 2 decimals, then strip trailing zeros and dot
        cost_per_unit_str = f"{cost_per_unit:.2f}".rstrip("0").rstrip(".")

        railbot.learn_key_value(f"{product} price per unit", cost_per_unit_str)
        return True




