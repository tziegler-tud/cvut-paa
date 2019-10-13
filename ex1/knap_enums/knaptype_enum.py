from enum import Enum


class KnapTypeEnum(Enum):
    DECISIVE = 0
    CONSTRUCTIVE = 1

    def getName(self):
        return str(self)

    def equals(self, obj):
        if isinstance(obj, KnapTypeEnum):
            return self.value == obj.value
        else:
            return False

    def getDataOffset(self):
        if self.equals(KnapTypeEnum.DECISIVE):
            return 1
        else:
            return 0


