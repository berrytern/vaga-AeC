import re
from datetime import datetime


class EnumOp:
    @classmethod
    def is_operator(cls, op):
        return re.match("^(gt|gte|lt|lte)$", op)


class TypeOp:
    def __init__(self, name):
        self.name = self.__validation(name)
        self.op, self.value = self.__segmentation()
        self.value = self.value_validation(self.value)

    def __validation(self, value):
        if not isinstance(value, str):
            raise ValueError("invalid type")
        return value

    @classmethod
    def value_validation(cls, value: str):
        return value

    @classmethod
    def get_index(cls, value: str):
        return value.find(":")

    @classmethod
    def validate_format(cls, value: str = "", index: int = None):
        index = index if index else cls.get_index(value)
        if index == 2 or index == 3:
            return EnumOp.is_operator(value[:index])
        return False

    def __segmentation(self):
        index = self.get_index(self.name)
        if self.validate_format(self.name, index=index):
            op = self.name[:index]
            value = self.name[index + 1 :]  # noqa: E203
            return op, value
        raise Exception("invalid format")


class TypeOpStr(TypeOp):
    def value_validation(cls, value: str) -> str:
        return value


class TypeOpInt(TypeOp):
    def value_validation(self, value: str) -> int:
        if value.isdigit():
            return int(value)
        raise ValueError("invalid type of value")


class TypeOpFloat(TypeOp):
    @classmethod
    def value_validation(cls, value: str, raise_err=True):
        if re.match("([+-]?([0-9]*[.])?[0-9]+)$", value):
            return float(value)
        if raise_err:
            raise ValueError("invalid type of value")


class TypeOpBool(TypeOp):
    @classmethod
    def value_validation(cls, value: str):
        if value == "0" or value.upper() == "FALSE":
            return False
        if value == "1" or value.upper() == "TRUE":
            return True
        raise ValueError("invalid type of value")


class TypeOpDate(TypeOp):
    @classmethod
    def value_validation(cls, value: str, raise_err=True):
        if re.match(
            r"(^\d{4}-((0[1-9])|(1[0-2]))-(0[1-9]|[1-2][0-9]|3[0-1])T([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]))$",
            value,
        ):
            try:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValueError("invalid time data, it does not exists.")
        if raise_err:
            raise ValueError("invalid format, must be YYYY-MM-DD")
