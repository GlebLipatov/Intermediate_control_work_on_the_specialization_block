from Controller.controller import controller
from Model.note import Note

if __name__ == '__main__':
    path = 'notes.csv'
    notes = controller(path)
    notes.start()