from datetime import datetime
from Model.note import Note


class View:
    """

    Выводит данные полученные из экземпляра класса Controller в консоль.

    """
    __commands: list[str]
    __attempts: dict[str, list[str]]

    def __init__(self):
        self.__commands = self.__load_commands()
        self.__attempts = self.__load_attempts()

    def greeting(self):
        print('---- Заметки ----')

    def show_notes(self, notes: dict[int, Note]):
        for note in notes.values():
            id = note.get_id()
            title = note.get_title()
            last_modifier_date = note.get_last_modified_date()

            print(f'id: {id} title: {title}, last modifier: {last_modifier_date}')

    def show_note(self, note: Note):
        id = note.get_id()
        title = note.get_title()
        body = note.get_body()
        last_modifier_date = note.get_last_modified_date()

        print(f'id: {id}, title: {title}, body: {body}, last modifier: {last_modifier_date}')

    def prompt_main_menu(self) -> str:
        commands = ', '.join(self.__commands)
        while True:
            input_from_user = input(f'Введите команду({commands}): ')

            if input_from_user.lower() in self.__commands:
                return input_from_user

    def prompt_show_menu(self) -> str:
        while True:
            input_from_user = input('Показать заметки.\nВведите команду(all, select): ')

            if input_from_user.__eq__('all') or input_from_user.__eq__('select'):
                return input_from_user

    def prompt_notes_menu(self, notes: dict[int, Note]) -> int:
        while True:
            input_from_user = input('Введите команду(id заметки, back): ').lower()

            if input_from_user.__eq__('back'):
                return -1
            elif input_from_user.isdigit() and int(input_from_user) in notes:
                return int(input_from_user)

    def prompt_add_new_note(self) -> str:
        return input('Введите название заметки: ')

    def prompt_input_body(self) -> str:
        return input('Введите данные: ')

    def prompt_select_date(self) -> datetime:
        while True:
            input_year: str = ''
            input_month: str = ''
            input_day: str = ''

            while True:
                input_year = input('Введите год(гггг): ')
                if len(input_year) == 4 and input_year.isdigit() and int(input_year) <= datetime.now().year:
                    break
            while True:
                input_month = input('Введите месяц(мм): ')
                if len(input_month) == 2 and input_month.isdigit() and 1 <= int(input_month) <= 12:
                    break
            while True:
                input_day = input('Введите день(дд): ')
                if len(input_day) == 2 and input_day.isdigit() and 1 <= int(input_day) <= 31:
                    break

            return datetime(int(input_year), int(input_month), int(input_day), 23, 59, 59)

    def prompt_modifier_menu(self) -> str:
        while True:
            input_from_user: str = input('Изменить название, тело, все(title, body, all): ')

            if input_from_user.lower().__eq__('title') or \
                    input_from_user.lower().__eq__('body') or \
                    input_from_user.lower().__eq__('all'):
                return input_from_user

    def prompt_new_title(self) -> str:
        return input('Введите новое название заметки: ')

    def prompt_new_body(self) -> str:
        return input('Введите новое тело заметки: ')

    def attempt_message(self, is_done, attempt: str):
        attempts: list[str] = self.__attempts[attempt]

        if is_done:
            print(attempts.__getitem__(0))
        else:
            print(attempts.__getitem__(1))

    def quit(self):
        print('Пока!')

    def __load_attempts(self) -> dict[str, list[str]]:
        attempts: dict[str, list[str]] = {}

        attempts['save'] = ['Сохранение выполненно!', 'Сохранение не выполненно!']
        attempts['read'] = ['Данные загруженны!', 'Не получилось загрузить данные!']
        attempts['add'] = ['Заметка добавленна!', 'Не получилось добавить заметку!']
        attempts['modifier'] = ['Заметка измененна!', 'Не получилось изменить заметку!']
        attempts['delete'] = ['Заметка удалена!', 'Не получилось удалить заметку!']
        return attempts

    def __load_commands(self) -> list[str]:
        commands: list[str] = ['read', 'show', 'add', 'modifier', 'delete', 'save', 'quit']
        return commands
