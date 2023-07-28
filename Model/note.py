from datetime import datetime


class Note:
    __id: int
    __title: str
    __body: str
    __last_modified_date: datetime

    def __init__(self, id: int, title: str):
        self.__id = id
        self.__title = title
        self.__last_modified_date = datetime.now()

    def get_id(self) -> int:
        return self.__id

    def get_title(self) -> str:
        return self.__title

    def set_title(self, new_title: str):
        self.__title = new_title

    def get_body(self) -> str:
        return self.__body

    def set_body(self, new_body: str):
        self.__body = new_body

    def get_last_modified_date(self) -> datetime:
        return self.__last_modified_date

    def set_last_modified_date(self, last_modified_date: datetime):
        self.__last_modified_date = last_modified_date
    def update_last_modifier_date(self):

        self.__last_modified_date = datetime.now()

    def __str__(self) -> str:
        return f'{self.__id} {self.__title} {self.__body} {self.__last_modified_date}'

    def __repr__(self) -> str:
        return f'{self.__id};{self.__title};{self.__body};{self.__last_modified_date}'

    def __le__(self, other):
        if isinstance(other, Note):
            return self.__last_modified_date <= other.get_last_modified_date()
        elif not isinstance(other, Note):
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Note):
            return self.__last_modified_date < other.get_last_modified_date()
        elif not isinstance(other, Note):
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.__last_modified_date == other.get_last_modified_date()
        elif not isinstance(other, Note):
            return NotImplemented
