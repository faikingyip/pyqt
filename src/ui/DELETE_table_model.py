import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QTableView,
    QHeaderView,
    QMessageBox,
    QVBoxLayout,
)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        """Set up the application's GUI."""
        self.setMinimumSize(1000, 500)
        self.setWindowTitle("SQL Table Model")
        self.create_connection()
        self.setup_main_window()
        self.show()

    def create_connection(self):
        """Set up the connection to the database.
        Check for the tables needed."""
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("accounts.db")
        if not database.open():
            print("Unable to open data source file.")
            sys.exit(1)  # Error code 1 - signifies error
        # Check if the tables we need exist in the database
        tables_needed = {"accounts"}
        tables_not_found = tables_needed - set(database.tables())
        if tables_not_found:
            QMessageBox.critical(
                None,
                "Error",
                f"""<p>The following tables are missing
                from the database: {tables_not_found}</p>""",
            )
            sys.exit(1)  # Error code 1 - signifies error

    def setup_main_window(self):
        """Create and arrange widgets in the main window."""
        # Create the model
        model = QSqlTableModel()
        model.setTable("accounts")
        table_view = QTableView()
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        # Populate the model with data
        model.select()
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(table_view)
        self.setLayout(main_v_box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
