from enum import Enum


class Status(Enum):
    NONE = 0
    BOMB = 1
    NOT_FREEZETIME = 2
    FREEZETIME = 3
    DEFUSED = 4
    EXPLODED = 5

    @classmethod
    def from_round_phase_dict(cls, data: str):
        return cls.FREEZETIME if data == "freezetime" else cls.NOT_FREEZETIME

    @classmethod
    def from_bomb_dict(cls, data: str):
        if data == "planted":
            return cls.BOMB
        elif data == "defused":
            return cls.DEFUSED
        elif data == "exploded":
            return cls.EXPLODED
        else:
            return cls.NONE
