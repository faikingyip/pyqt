import sys, os
from typing import List
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QTableView,
    QHeaderView,
    QAbstractItemView,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlRelation,
    QSqlRelationalTableModel,
    QSqlRelationalDelegate,
)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

WINDOW_TITLE = "Account Management"


Base = declarative_base()


class AccountEntity(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    department = Column(String)
    country_id = Column(Integer)


# SQLAlchemy engine and session setup
engine = create_engine("sqlite:///accounts.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class AccountsTableItemModel:
    def __init__(
        self,
        id: int = None,
        employee_id: int = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        department: str = None,
        country_id: int = None,
    ) -> None:

        self.id = id
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.department = department
        self.country_id = country_id


class AccountsTableModel(QAbstractTableModel):
    def __init__(self, accounts: List[AccountsTableItemModel]):
        super().__init__()
        self.accounts: List[AccountsTableItemModel] = accounts

    def data(self, index: QModelIndex, role: int):

        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        account = self.accounts[index.row()]

        if index.column() == 0:
            return account.id
        if index.column() == 1:
            return account.employee_id
        if index.column() == 2:
            return account.first_name
        if index.column() == 3:
            return account.last_name
        if index.column() == 4:
            return account.email
        if index.column() == 5:
            return account.department
        if index.column() == 6:
            return account.country_id

        return None

    def rowCount(self, index=QModelIndex()):
        """Returns the number of rows"""
        _ = index
        return len(self.accounts)

    def columnCount(self, index=QModelIndex()):
        """Returns the column count"""
        _ = index
        return 7

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """Enable editing of the table"""
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False

        if not value:
            return False

        account = self.accounts[index.row()]
        if index.column() == 0:  # Edit id
            account.id = value
        if index.column() == 1:  # Edit employee_id
            account.employee_id = value
        elif index.column() == 2:  # Edit first_name
            account.first_name = value
        elif index.column() == 3:  # Edit last_name
            account.last_name = value
        elif index.column() == 4:  # Edit email
            account.email = value
        elif index.column() == 5:  # Edit department
            account.department = value
        elif index.column() == 6:  # Edit country_id
            account.country_id = int(value)

        # session.commit()  # Commit changes to the database
        self.dataChanged.emit(index, index, (Qt.ItemDataRole.DisplayRole,))
        return True

    def flags(self, index):
        """Enable editing of the table"""
        if index.column() >= 0:  # Allow editing for all columns except the id column
            return (
                Qt.ItemFlag.ItemIsEditable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsSelectable
            )
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """Set header names"""
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return ["ID", "Employee ID", "First", "Last", "Email", "Dept.", "Country"][
                section
            ]
        return super().headerData(section, orientation, role)

    # def removeRow(self, row, parent=QModelIndex()):
    #     """Remove the selected row from the table"""
    #     self.beginRemoveRows(parent, row, row)
    #     account_to_delete = self.accounts[row]
    #     session.delete(account_to_delete)  # Remove from database
    #     session.commit()  # Commit to DB
    #     self.accounts.pop(row)  # Remove from internal list
    #     self.endRemoveRows()

    # def addRow(
    #     self,
    #     id: int,
    #     employee_id: int,
    #     first_name: str,
    #     last_name: str,
    #     email: str,
    #     department: str,
    #     country_id: int,
    # ):
    #     """Add a row to the end of the table"""
    #     self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
    #     new_account = AccountsTableItemModel(
    #         id=id,
    #         employee_id=employee_id,
    #         first_name=first_name,
    #         last_name=last_name,
    #         email=email,
    #         department=department,
    #         country_id=country_id,
    #     )
    #     session.add(new_account)  # Add to database
    #     session.commit()  # Commit to DB, assigns ID automatically
    #     self.accounts.append(new_account)  # Add to internal list
    #     self.endInsertRows()

    def add_empty_row(self):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.accounts.append(AccountsTableItemModel())
        self.endInsertRows()

    def removeRow(self, row, parent=QModelIndex()):
        """Remove the selected row from the table"""
        self.beginRemoveRows(parent, row, row)
        # account_to_delete = self.accounts[row]
        self.accounts.pop(row)  # Remove from internal list
        self.endRemoveRows()

    def sort(self, column: int, order=Qt.SortOrder.AscendingOrder):
        """Sort rows"""
        if column == 0:  # Sort by 'id'
            self.accounts.sort(
                key=lambda i: i.id, reverse=order == Qt.SortOrder.DescendingOrder
            )
        elif column == 1:  # Sort by 'employee_id'
            self.accounts.sort(
                key=lambda i: i.employee_id,
                reverse=order == Qt.SortOrder.DescendingOrder,
            )
        elif column == 2:  # Sort by 'first_name'
            self.accounts.sort(
                key=lambda i: i.first_name,
                reverse=order == Qt.SortOrder.DescendingOrder,
            )
        elif column == 3:  # Sort by 'last_name'
            self.accounts.sort(
                key=lambda i: i.last_name,
                reverse=order == Qt.SortOrder.DescendingOrder,
            )
        elif column == 4:  # Sort by 'email'
            self.accounts.sort(
                key=lambda i: i.email,
                reverse=order == Qt.SortOrder.DescendingOrder,
            )
        elif column == 5:  # Sort by 'department'
            self.accounts.sort(
                key=lambda i: i.department,
                reverse=order == Qt.SortOrder.DescendingOrder,
            )
        elif column == 6:  # Sort by 'email'
            self.accounts.sort(
                key=lambda i: i.country_id,
                reverse=order == Qt.SortOrder.DescendingOrder,
            )
        self.layoutChanged.emit()  # Notify the view that the model has changed


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.model: AccountsTableModel = None
        self.table_view = None

        self.initialize_ui()

    def initialize_ui(self):
        """Set up the application's GUI."""
        self.setMinimumSize(1000, 600)
        self.setWindowTitle(WINDOW_TITLE)
        # self.create_connection()
        self.create_model()
        self.setup_main_window()
        self.show()

    def create_model(self):
        """Fetch data and bind to model"""
        # accounts = session.query(Accounts).all()
        accounts: List[AccountsTableItemModel] = []
        accounts.append(
            AccountsTableItemModel(
                id=1,
                employee_id="1000",
                first_name="Mark",
                last_name="Bass",
                email="mark.bass@example.com",
                department="Fulfilment",
                country_id=1,
            )
        )
        accounts.append(
            AccountsTableItemModel(
                id=2,
                employee_id="1001",
                first_name="Jamie",
                last_name="Oliver",
                email="jamie.oliver@example.com",
                department="Kitchen",
                country_id=2,
            )
        )
        accounts.append(
            AccountsTableItemModel(
                id=3,
                employee_id="1002",
                first_name="Gordon",
                last_name="Ramsey",
                email="gordon.ramsey@example.com",
                department="Kitchen",
                country_id=1,
            )
        )
        self.model = AccountsTableModel(accounts)

    def setup_main_window(self):
        """Create and arrange widgets in the main window."""
        icons_path = "icons"
        title = QLabel("Account Management System")
        title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        title.setStyleSheet("font: bold 24px")
        add_product_button = QPushButton("Add Employee")
        add_product_button.setIcon(QIcon(os.path.join(icons_path, "add_user.png")))
        add_product_button.setStyleSheet("padding: 10px")
        add_product_button.clicked.connect(self.add_item)
        del_product_button = QPushButton("Delete")
        del_product_button.setIcon(QIcon(os.path.join(icons_path, "trash_can.png")))
        del_product_button.setStyleSheet("padding: 10px")
        del_product_button.clicked.connect(self.delete_item)

        # Set up sorting combobox
        sorting_options = [
            "Sort by ID",
            "Sort by Employee ID",
            "Sort by First Name",
            "Sort by Last Name",
            "Sort by Department",
            "Sort by Country",
        ]
        sort_combo = QComboBox()
        sort_combo.addItems(sorting_options)
        sort_combo.currentTextChanged.connect(self.set_sorting_order)
        buttons_h_box = QHBoxLayout()
        buttons_h_box.addWidget(add_product_button)
        buttons_h_box.addWidget(del_product_button)
        buttons_h_box.addStretch()
        buttons_h_box.addWidget(sort_combo)

        # Widget to contain editing buttons
        edit_container = QWidget()
        edit_container.setLayout(buttons_h_box)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        horizontal = self.table_view.horizontalHeader()
        horizontal.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical = self.table_view.verticalHeader()
        vertical.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # Instantiate the delegate
        delegate = QSqlRelationalDelegate()
        self.table_view.setItemDelegate(delegate)

        # Main layout
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(title, Qt.AlignmentFlag.AlignLeft)
        main_v_box.addWidget(edit_container)
        main_v_box.addWidget(self.table_view)
        self.setLayout(main_v_box)

    def add_item(self):
        """Add a new record to the last row of the table."""
        self.model.add_empty_row()

    def delete_item(self):
        """Delete an entire row from the table."""
        current_item = self.table_view.selectedIndexes()
        if len(current_item):
            self.model.removeRow(current_item[0].row())

    def set_sorting_order(self, text):
        """Sort the rows in the table."""
        if text == "Sort by ID":
            self.model.sort(0, Qt.SortOrder.AscendingOrder)
        elif text == "Sort by Employee ID":
            self.model.sort(1, Qt.SortOrder.AscendingOrder)
        elif text == "Sort by First Name":
            self.model.sort(2, Qt.SortOrder.AscendingOrder)
        elif text == "Sort by Last Name":
            self.model.sort(3, Qt.SortOrder.AscendingOrder)
        elif text == "Sort by Email":
            self.model.sort(4, Qt.SortOrder.AscendingOrder)
        elif text == "Sort by Department":
            self.model.sort(5, Qt.SortOrder.AscendingOrder)
        elif text == "Sort by Country":
            self.model.sort(6, Qt.SortOrder.AscendingOrder)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
