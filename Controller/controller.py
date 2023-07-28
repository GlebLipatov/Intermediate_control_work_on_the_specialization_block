from datetime import datetime

from Model.note import Note
from Model.notes import Notes
from View.View import View


class controller:
    """

    Класс, который обрабатывает загружает, изменяет, добавляет, сохраняет данные при работе с классом Notes и
    выводит на интерфейс через класс View.

    """

    __path: str
    __model: Notes
    __view: View

    def __init__(self, path: str):
        self.__path = path
        self.__model = Notes()
        self.__view = View()

    def start(self):

        """

        Запускает программу.

        """

        view = self.__view

        view.greeting()
        is_continue = True
        while is_continue:
            user_choice = view.prompt_main_menu()

            match user_choice:
                case 'read':
                    is_read = self.read()
                    view.attempt_message(is_read, user_choice)
                case 'show':
                    note_id = self.show()
                    if note_id > 0:
                        note: Note = self.__model.get_all_notes().get(note_id)
                        view.show_note(note)
                case 'add':
                    is_added = self.add()
                    view.attempt_message(is_added, user_choice)
                case 'modifier':
                    is_modifier = self.modifier()
                    view.attempt_message(is_modifier, user_choice)
                case 'delete':
                    is_delete = self.delete()
                    view.attempt_message(is_delete, user_choice)
                case 'save':
                    is_save = self.save()
                    view.attempt_message(is_save, user_choice)
                case 'quit':
                    view.quit()
                    is_continue = False

    def read(self) -> bool:

        """
        Загружает и обрабатывает данные из файла формата .csv .

        :return: bool для оповещения о результате работы метода
        """

        notes_list_from_file: list[str] = self.__load(self.__path)
        notes_parsed: dict[int, Note] = self.__parse(notes_list_from_file)
        self.__model.load_notes(notes_parsed)

        if len(self.__model.get_all_notes()) > 0:
            return True
        else:
            return False

    def __load(self, path: str) -> list:
        """
        Загружает данные из файла по указанному пути и возвращет в виде list: str
        :param path: путь к файлу для загруки данных
        :return: list: str с данными из файла
        """
        with open(path, 'r', encoding='utf-8') as file:
            data = file.readlines()
        return data

    def __parse(self, notes_list: list[str]) -> dict[int, Note]:
        """

        Обрабатывает данные из загруженного файла и возвращает dict[int, Note]

        :param notes_list: Лист с данными загруженными из файла.
        :return: парсит и возвращает данные ввиде dict[int, Note]
        """
        notes: dict[int, Note] = {}

        for line in notes_list:
            note_data = line.split(';')

            id = int(note_data[0])
            title = note_data[1]
            body = note_data[2]
            last_modified_date = datetime.fromisoformat(note_data[3].replace('\n', ''))

            new_note = Note(id, title)
            new_note.set_body(body)
            new_note.set_last_modified_date(last_modified_date)
            notes[id] = new_note
        return notes

    def show(self) -> int:
        """

        Выводит все данные или выборку по дате через View.
        Выбор заметки(Note) для просмотра.

        :return: id выбранной заметки
        """
        view = self.__view
        notes: dict[int, Note] = self.__model.get_all_notes()

        user_choice_show_menu: str = view.prompt_show_menu()

        if user_choice_show_menu.__eq__('all'):
            view.show_notes(notes)
        elif user_choice_show_menu.__eq__('select'):
            selected_date: datetime = view.prompt_select_date()
            notes: dict[int, Note] = self.get_selected_notes(selected_date)
            view.show_notes(notes)

        return view.prompt_notes_menu(notes)

    def get_selected_notes(self, date: datetime) -> dict[int, Note]:
        """

        Отбиравет все заметки до указанной даты включительно.

        :param date: дата до которой включительно будут отобранны заметки(Note)
        :return: словарь заметок dict(int, Note), где ключ это id заметки(Note), а значение заметка(Note)
        """
        all_notes = self.__model.get_all_notes()
        selected_notes: dict[int, Note] = {}

        for note in all_notes.values():
            if note.get_last_modified_date() <= date:
                selected_notes[note.get_id()] = note

        return selected_notes

    def add(self) -> bool:
        """

        Добавляет новую заметку

        :return: bool для оповещения о результате работы метода
        """
        new_note_id = self.__model.get_id_next()
        new_note_title = self.__view.prompt_add_new_note()
        new_note = Note(new_note_id, new_note_title)

        new_note_body = self.__view.prompt_input_body()
        new_note.set_body(new_note_body)

        return self.__model.add(new_note)

    def save(self) -> bool:
        """

        Сохраняет данные заметок(Note) в файл в формате .csv по пути __path.

        :return: bool для оповещения о результате работы метода
        """
        if len(self.__model.get_all_notes()) > 0:
            notes = ''
            for note in self.__model.get_all_notes().values():
                notes += note.__repr__() + '\n'
            with open(self.__path, 'w', encoding='utf-8') as file:
                file.writelines(notes)
                return True
        return False

    def modifier(self) -> bool:
        """

        Изменяет название(title) и/или тело(body) заметки(Note)

        :return: bool для оповещения о результате работы метода
        """
        view: View = self.__view
        model: Notes = self.__model
        notes: dict[int, Note] = self.__model.get_all_notes()

        view.show_notes(notes)
        note_id: int = view.prompt_notes_menu(notes)
        user_choice_modifier_menu: str = view.prompt_modifier_menu()

        new_title: str
        new_body: str

        match user_choice_modifier_menu:
            case 'title':
                new_title = view.prompt_new_title()
                return model.modifier(note_id, new_title=new_title,)
            case 'body':
                new_body = view.prompt_new_body()
                return model.modifier(note_id, new_body=new_body)
            case 'all':
                new_title = view.prompt_new_title()
                new_body = view.prompt_new_body()
                return model.modifier(note_id, new_title, new_body)

    def delete(self) -> bool:
        """

        Удаляет заметку.

        :return: bool для оповещения о результате работы метода
        """
        note_id: int = self.show()
        self.__model.get_all_notes().__delitem__(note_id)
        return True
