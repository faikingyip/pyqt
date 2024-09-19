import os
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTextEdit,
    QFileDialog,
    QInputDialog,
    QFontDialog,
    QColorDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QTextCursor, QColor, QAction

from exception.exceptions import InvalidNoteSaveFileFormatException
from ui.notepad.note_saver import QTextEditFileNoteSaverManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = None
        self.new_act = None
        self.open_act = None
        self.save_act = None
        self.quit_act = None
        self.undo_act = None
        self.redo_act = None
        self.cut_act = None
        self.copy_act = None
        self.paste_act = None
        self.find_act = None
        self.font_act = None
        self.color_act = None
        self.highlight_act = None
        self.about_act = None

        self.initialize_ui()

    def initialize_ui(self):
        """Set up the application's GUI."""
        self.setMinimumSize(400, 500)
        self.setWindowTitle("5.1 – Rich Text Notepad GUI")
        self.setup_main_window()
        self.create_actions()
        self.create_menu()
        self.show()

    def setup_main_window(self):
        """Create and arrange widgets in the main window."""
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.remove_highlights)
        self.setCentralWidget(self.text_edit)

    def create_actions(self):
        """Create the application's menu actions."""

        # Create actions for File menu
        self.new_act = QAction(QIcon("images/new_file.png"), "New")
        self.new_act.setShortcut("Ctrl+N")
        self.new_act.triggered.connect(self.clear_text)
        self.open_act = QAction(QIcon("images/open_file.png"), "Open")
        self.open_act.setShortcut("Ctrl+O")
        self.open_act.triggered.connect(self.open_file)
        self.save_act = QAction(QIcon("images/save_file.png"), "Save")
        self.save_act.setShortcut("Ctrl+S")
        self.save_act.triggered.connect(self.save_to_file)
        self.quit_act = QAction(QIcon("images/exit.png"), "Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)

        # Create actions for Edit menu
        self.undo_act = QAction(QIcon("images/undo.png"), "Undo")
        self.undo_act.setShortcut("Ctrl+Z")
        self.undo_act.triggered.connect(self.text_edit.undo)
        self.redo_act = QAction(QIcon("images/redo.png"), "Redo")
        self.redo_act.setShortcut("Ctrl+Shift+Z")
        self.redo_act.triggered.connect(self.text_edit.redo)
        self.cut_act = QAction(QIcon("images/cut.png"), "Cut")
        self.cut_act.setShortcut("Ctrl+X")
        self.cut_act.triggered.connect(self.text_edit.cut)
        self.copy_act = QAction(QIcon("images/copy.png"), "Copy")
        self.copy_act.setShortcut("Ctrl+C")
        self.copy_act.triggered.connect(self.text_edit.copy)
        self.paste_act = QAction(QIcon("images/paste.png"), "Paste")
        self.paste_act.setShortcut("Ctrl+V")
        self.paste_act.triggered.connect(self.text_edit.paste)
        self.find_act = QAction(QIcon("images/find.png"), "Find All")
        self.find_act.setShortcut("Ctrl+F")
        self.find_act.triggered.connect(self.search_text)

        # Create actions for Tools menu
        self.font_act = QAction(QIcon("images/font.png"), "Font")
        self.font_act.setShortcut("Ctrl+T")
        self.font_act.triggered.connect(self.choose_font)
        self.color_act = QAction(QIcon("images/color.png"), "Color")
        self.color_act.setShortcut("Ctrl+Shift+C")
        self.color_act.triggered.connect(self.choose_font_color)
        self.highlight_act = QAction(QIcon("images/highlight.png"), "Highlight")
        self.highlight_act.setShortcut("Ctrl+Shift+H")
        self.highlight_act.triggered.connect(self.choose_font_background_color)

        # Create actions for Help menu
        self.about_act = QAction("About")
        self.about_act.triggered.connect(self.about_dialog)

    def create_menu(self):
        """Create the application's menu bar."""
        self.menuBar().setNativeMenuBar(False)

        # Create File menu and add actions
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_act)
        file_menu.addSeparator()
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_act)

        # Create Edit menu and add actions
        edit_menu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(self.undo_act)
        edit_menu.addAction(self.redo_act)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_act)
        edit_menu.addAction(self.copy_act)
        edit_menu.addAction(self.paste_act)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_act)

        # Create Tools menu and add actions
        tool_menu = self.menuBar().addMenu("Tools")
        tool_menu.addAction(self.font_act)
        tool_menu.addAction(self.color_act)
        tool_menu.addAction(self.highlight_act)

        # Create Help menu and add actions
        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_act)

    def clear_text(self):
        """Clear the QTextEdit field."""

        answer = QMessageBox.question(
            self,
            "Clear Text",
            "Do you want to clear the text?",
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.Yes,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.text_edit.clear()

    def open_file(self):
        """Open a text or html file and display its contents
        in the text edit field."""

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "HTML Files (*.html);;Text Files (*.txt)"
        )
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                notepad_text = f.read()
            self.text_edit.setText(notepad_text)

    def save_to_file(self):
        """If the save button is clicked, display dialog
        asking user if they want to save the text in the text
        edit field to a text or rich text file."""

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "HTML Files (*.html);;Text Files (*.txt)"
        )

        try:
            file_note_saver_manager = QTextEditFileNoteSaverManager(
                file_name, self.text_edit
            )
            note_saver = file_note_saver_manager.create_note_saver()
            note_saver.save()
        except InvalidNoteSaveFileFormatException:
            QMessageBox.information(
                self, "Not Saved", "Text not saved.", QMessageBox.StandardButton.Ok
            )

    def search_text(self):
        """Search for text."""

        # Display input dialog to ask user for text to find
        find_text, ok = QInputDialog.getText(self, "Search Text", "Find:")
        if ok:
            extra_selections = []

            # Set the cursor to the beginning
            self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)
            color = QColor(Qt.GlobalColor.gray)
            while self.text_edit.find(find_text):

                # Use ExtraSelection() to mark the text you
                # are searching for as gray
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(color)

                # Set the cursor of the selection
                selection.cursor = self.text_edit.textCursor()
                extra_selections.append(selection)

            # Highlight all selections in the QTextEdit widget
            self.text_edit.setExtraSelections(extra_selections)

    def remove_highlights(self):
        """Reset extra selections after editing text."""
        self.text_edit.setExtraSelections([])

    def choose_font(self):
        """Select a font from the QFontDialog."""
        current = self.text_edit.currentFont()
        opt = QFontDialog.FontDialogOption.DontUseNativeDialog
        font, ok = QFontDialog.getFont(current, self, options=opt)
        if ok:
            self.text_edit.setCurrentFont(font)

    def choose_font_color(self):
        """Select a font from the QColorDialog."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)

    def choose_font_background_color(self):
        """Select a color for text's background."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextBackgroundColor(color)

    def about_dialog(self):
        """Display the About dialog."""
        QMessageBox.about(
            self,
            "About Notepad",
            """<p>Beginner's Practical Guide to PyQt</p>
            <p>Project 5.1 - Notepad GUI</p>""",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
