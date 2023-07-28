from Model.note import Note


class Notes:

    """

    Класс, содержащий словарь заметок в котором ключ это id экзепляра класса Note, а значение экземпляр класса Note.
    Класс содержит методы необходимые для выполнения различных действий над коллекцией заметок(add, modifier, delete,
    load_notes, get_all_notes, get_id_next).

    """

    __notes: dict[int, Note]
    __id_next = 1

    def __init__(self):
        self.__notes = {}

    def get_all_notes(self) -> dict[int, Note]:
        return self.__notes

    def add(self, new_note: Note) -> bool:
        if len(self.__notes) == 0:
            self.__notes[new_note.get_id()] = new_note
            self.__id_next += 1
            return True

        if new_note.get_id() not in self.__notes:
            self.__notes[new_note.get_id()] = new_note
            self.__id_next += 1
            return True
        else:
            return False

    def modifier(self, note_id: int, new_title: str = 'empty', new_body: str = 'empty') -> bool:
        note: Note = self.__notes.get(note_id)

        if not new_title.__eq__('empty'):
            note.set_title(new_title)
        if not new_body.__eq__('empty'):
            note.set_body(new_body)
        note.update_last_modifier_date()

        return True

    def delete(self, note_id: int) -> bool:
        note: Note = self.__notes.get(note_id)
        if note in self.__notes.values():
            self.__notes.__delitem__(note_id)
            return True
        else:
            return False

    def get_id_next(self) -> int:
        return self.__id_next

    def set_id_next(self, id_current):
        self.__id_next = id_current + 1

    def load_notes(self, notes: dict[int, Note]):
        self.__notes = notes
        self.get_next_id_from_load_notes(notes)

    def get_next_id_from_load_notes(self, notes: dict[int, Note]):
        max_id: int = 0
        for note in notes.keys():
            if note > max_id:
                max_id = note
        self.__id_next = max_id + 1
