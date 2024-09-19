import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QInputDialog,
)
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table_widget = None

        self.quit_act = None
        self.add_row_above_act = None
        self.add_row_below_act = None
        self.add_col_before_act = None
        self.add_col_after_act = None
        self.delete_row_act = None
        self.delete_col_act = None
        self.clear_table_act = None
        self.item_text = None

        self.initialize_ui()

    def initialize_ui(self):
        """Set up the application's GUI."""
        self.setMinimumSize(1000, 500)
        self.setWindowTitle("Spreadsheet - QTableWidget Example")

        # Used for copy and paste actions
        self.item_text = None
        self.setup_main_window()
        self.create_actions()
        self.create_menu()
        self.show()

    def setup_main_window(self):
        """Create and arrange widgets in the main window."""
        self.table_widget = QTableWidget()
        # Set initial row and column values
        self.table_widget.setRowCount(10)
        self.table_widget.setColumnCount(10)
        # Set focus on cell in the table
        self.table_widget.setCurrentCell(0, 0)
        # When the horizontal headers are double-clicked,
        # emit a signal
        h_header = self.table_widget.horizontalHeader()
        h_header.sectionDoubleClicked.connect(self.change_header)
        self.setCentralWidget(self.table_widget)

    def create_actions(self):
        """Create the application's menu actions."""
        # Create actions for File menu
        self.quit_act = QAction("Quit", self)
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)
        # Create actions for Table menu
        self.add_row_above_act = QAction("Add Row Above", self)
        self.add_row_above_act.triggered.connect(self.add_row_above)
        self.add_row_below_act = QAction("Add Row Below", self)
        self.add_row_below_act.triggered.connect(self.add_row_below)
        self.add_col_before_act = QAction("Add Column Before", self)
        self.add_col_before_act.triggered.connect(self.add_column_before)
        self.add_col_after_act = QAction("Add Column After", self)
        self.add_col_after_act.triggered.connect(self.add_column_after)
        self.delete_row_act = QAction("Delete Row", self)
        self.delete_row_act.triggered.connect(self.delete_row)
        self.delete_col_act = QAction("Delete Column", self)
        self.delete_col_act.triggered.connect(self.delete_column)
        self.clear_table_act = QAction("Clear All", self)
        self.clear_table_act.triggered.connect(self.clear_table)

    def create_menu(self):
        """Create the application's menu bar."""
        self.menuBar().setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.quit_act)
        # Create table menu and add actions
        table_menu = self.menuBar().addMenu("Table")
        table_menu.addAction(self.add_row_above_act)
        table_menu.addAction(self.add_row_below_act)
        table_menu.addSeparator()
        table_menu.addAction(self.add_col_before_act)
        table_menu.addAction(self.add_col_after_act)
        table_menu.addSeparator()
        table_menu.addAction(self.delete_row_act)
        table_menu.addAction(self.delete_col_act)
        table_menu.addSeparator()
        table_menu.addAction(self.clear_table_act)

    def contextMenuEvent(self, event):
        """Create context menu and additional actions."""
        context_menu = QMenu(self)
        context_menu.addAction(self.add_row_above_act)
        context_menu.addAction(self.add_row_below_act)
        context_menu.addSeparator()
        context_menu.addAction(self.add_col_before_act)
        context_menu.addAction(self.add_col_after_act)
        context_menu.addSeparator()
        context_menu.addAction(self.delete_row_act)
        context_menu.addAction(self.delete_col_act)
        context_menu.addSeparator()

        # Create actions specific to the context menu
        copy_act = context_menu.addAction("Copy")
        paste_act = context_menu.addAction("Paste")
        context_menu.addSeparator()
        context_menu.addAction(self.clear_table_act)

        # Execute the context_menu and return the action
        # selected. mapToGlobal() translates the position
        # of the window coordinates to the global screen
        # coordinates. This way we can detect if a right-click
        # occurred inside of the GUI and display the context
        # menu
        action = context_menu.exec(self.mapToGlobal(event.pos()))

        # Check for actions selected in the context menu that
        # were not created in the menu bar
        if action == copy_act:
            self.copy_item()
        if action == paste_act:
            self.paste_item()

    def change_header(self):
        """Change horizontal headers by returning the text
        from input dialog."""
        col = self.table_widget.currentColumn()
        text, ok = QInputDialog.getText(self, "Enter Header", "Header text:")
        if ok and text != "":
            self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem(text))

    def copy_item(self):
        """If the current cell selected is not empty,
        store the text."""
        if self.table_widget.currentItem() != None:
            text = self.table_widget.currentItem().text()
            self.item_text = text

    def paste_item(self):
        """Set item for selected cell."""
        if self.item_text != None:
            row = self.table_widget.currentRow()
            column = self.table_widget.currentColumn()
            self.table_widget.setItem(row, column, QTableWidgetItem(self.item_text))

    def add_row_above(self):
        current_row = self.table_widget.currentRow()
        self.table_widget.insertRow(current_row)

    def add_row_below(self):
        current_row = self.table_widget.currentRow()
        self.table_widget.insertRow(current_row + 1)

    def add_column_before(self):
        current_col = self.table_widget.currentColumn()
        self.table_widget.insertColumn(current_col)

    def add_column_after(self):
        current_col = self.table_widget.currentColumn()
        self.table_widget.insertColumn(current_col + 1)

    def delete_row(self):
        current_row = self.table_widget.currentRow()
        self.table_widget.removeRow(current_row)

    def delete_column(self):
        current_col = self.table_widget.currentColumn()
        self.table_widget.removeColumn(current_col)

    def clear_table(self):
        self.table_widget.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
