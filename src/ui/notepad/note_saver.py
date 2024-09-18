from abc import ABC, abstractmethod

from exception.exceptions import InvalidNoteSaveFileFormatException
from PyQt6.QtWidgets import QTextEdit


class ValueExtractor(ABC):

    def extract_value(self) -> str:
        return self.perform_extract_value()

    @abstractmethod
    def perform_extract_value(self) -> str:
        """Factory method"""


class QTextEditPlainTextValueExtractor(ValueExtractor):

    def __init__(self, q_text_edit: QTextEdit) -> None:
        super().__init__()
        self.q_text_edit = q_text_edit

    def perform_extract_value(self) -> str:
        """Factory method"""
        return self.q_text_edit.toPlainText()


class QTextEditHtmlValueExtractor(ValueExtractor):

    def __init__(self, q_text_edit: QTextEdit) -> None:
        super().__init__()
        self.q_text_edit = q_text_edit

    def perform_extract_value(self) -> str:
        """Factory method"""
        return self.q_text_edit.toHtml()


class NoteSaver(ABC):

    def save(self) -> None:
        """Calls the subclass implemented method to save the information"""
        self.perform_save()

    @abstractmethod
    def perform_save(self) -> None:
        """Factory method"""


class QTextEditPlainTextFileNoteSaver(NoteSaver):

    def __init__(self, file_name: str, q_text_edit: QTextEdit) -> None:
        super().__init__()
        self.file_name = file_name
        self.q_text_edit = q_text_edit

    def perform_save(self) -> None:
        value = QTextEditPlainTextValueExtractor(self.q_text_edit).extract_value()
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(value)


class QTextEditHtmlFileNoteSaver(NoteSaver):

    def __init__(self, file_name: str, q_text_edit: QTextEdit) -> None:
        super().__init__()
        self.file_name = file_name
        self.q_text_edit = q_text_edit

    def perform_save(self) -> None:
        value = QTextEditHtmlValueExtractor(self.q_text_edit).extract_value()
        with open(self.file_name, "w", encoding="utf-8") as f:
            f.write(value)


class NoteSaverManager(ABC):
    @abstractmethod
    def create_note_saver(self) -> NoteSaver:
        """Factory method"""


class QTextEditFileNoteSaverManager(NoteSaverManager):

    def __init__(self, file_name: str, q_text_edit: QTextEdit) -> None:
        super().__init__()
        self.file_name = file_name
        self.q_text_edit = q_text_edit

    def create_note_saver(self) -> NoteSaver:
        """Factory method"""

        if self.file_name.endswith(".txt"):
            return QTextEditPlainTextFileNoteSaver(self.file_name, self.q_text_edit)
        elif self.file_name.endswith(".html"):
            return QTextEditHtmlFileNoteSaver(self.file_name, self.q_text_edit)
        else:
            raise InvalidNoteSaveFileFormatException(self.file_name)
