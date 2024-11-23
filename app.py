import sys
from PySide6.QtWidgets import QApplication
from view import TreeWindow


def main():
    app = QApplication(sys.argv)
    view = TreeWindow()
    # person_model = PersonModel()
    # person_viewmodel = PersonViewModel(person_model, view, person_id)

    # view.set_age_button.clicked.connect(person_viewmodel.update_age)
    # view.chage_name_button.clicked.connect(person_viewmodel.update_name)

    # person_viewmodel.notify_person_data()

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
