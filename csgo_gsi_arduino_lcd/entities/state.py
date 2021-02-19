from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class State:
    health: int
    armor: int
    round_kills: int
    round_killhs: int
    money: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            health=int(data["health"]),
            armor=int(data["armor"]),
            round_kills=int(data["round_kills"]),
            round_killhs=int(data["round_killhs"]),
            money=int(data["money"]),
        )
