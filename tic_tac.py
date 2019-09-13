from PyQt5 import QtCore, QtGui, QtWidgets
from AI import BoardAI
import random
import sys


class Main(QtWidgets.QWidget):
    """
    A class to be an instance of a GUI. The logic for the front end is also going to be set up here.
    However, the calculations and the AI are set up in a different file.

    """

    def __init__(self):
        """The initialization of the GUI where everything is set up without the need of inserting arguments.
        This GUI is basically the attempt of making an AI win against a regular user playing tic tac toe.
        There are also is also a lot of customization available from modifying code.
        In addition, there is an option that can be checked to enable random results which proves
        that the AI is impossible to beat.

        :var results: a list containing all the results from the ai.evaluate (from BoardAI)
        :var delay: an int delay between wins in a tic tac toe
        :var symbol: a str symbol, either 'X' or 'O'. represents the current turn.
        :var buttons: a dictionary that will later be filled up with objects. Holds QtWidgets.QPushButton()
        :var decos: a dictionary that will later be filled up with objects. Holds QtWidgets.QPushButton()
        :var board: a list of 9 str objects which all represent the board that is being held within the GUI.

        :returns: None

        """

        super(Main, self).__init__()

        self.setWindowTitle('Tic Tac Toe vs an AI')
        self.results = []
        self.delay = 1000
        self.symbol = 'X'
        self.buttons = {}
        self.decos = {}
        self.board = ['', '', '',
                      '', '', '',
                      '', '', '']

        x = QtWidgets.QDesktopWidget().availableGeometry().center().x()
        y = QtWidgets.QDesktopWidget().availableGeometry().center().y()
        self.setGeometry(x/2, y/4, x, y)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)

        self.checkBox = QtWidgets.QCheckBox()
        self.checkBox.setText('Random')
        self.checkBox.clicked.connect(self.random)

        # Label for data
        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet('''
        font-size: 15px;
        color: black;
        font-family: Segoe UI''')
        self.label.setText('\n'*8)

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setText('Clear')
        self.pushButton.clicked.connect(self.clear_all)
        self.pushButton.setStyleSheet(f'''
        QPushButton:!hover{{
        background-color: none;
        border: none;

        color: black;
        font-size: 55px;
        font-family: Segoe UI
        }}

        QPushButton:hover{{
        background-color: #cfcfcf;
        border: none
        }}

        QPushButton:pressed{{
        background-color: #828282
        }}
        ''')

        # Init Buttons
        for i in range(9):
            self.buttons[i] = QtWidgets.QPushButton()
            self.buttons[i].setMinimumSize(QtCore.QSize(150, 150))
            self.buttons[i].setStyleSheet(f'''
            QPushButton:!hover{{
            background-color: none;
            border: none;
            
            color: black;
            font-size: 55px;
            font-family: Segoe UI
            }}
            
            QPushButton:hover{{
            background-color: #cfcfcf;
            border: none
            }}

            QPushButton:pressed{{
            background-color: #828282
            }}
                ''')

        # Connects button to clicked_connect
        self.buttons[0].clicked.connect(lambda: self.clicked_connect(0))
        self.buttons[1].clicked.connect(lambda: self.clicked_connect(1))
        self.buttons[2].clicked.connect(lambda: self.clicked_connect(2))
        self.buttons[3].clicked.connect(lambda: self.clicked_connect(3))
        self.buttons[4].clicked.connect(lambda: self.clicked_connect(4))
        self.buttons[5].clicked.connect(lambda: self.clicked_connect(5))
        self.buttons[6].clicked.connect(lambda: self.clicked_connect(6))
        self.buttons[7].clicked.connect(lambda: self.clicked_connect(7))
        self.buttons[8].clicked.connect(lambda: self.clicked_connect(8))

        # Init Decoration
        for i in range(8):
            self.decos[i] = QtWidgets.QGroupBox()
            self.decos[i].setStyleSheet('''
            background-color: black;
            border: 10px solid black
            ''')

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # Adds to layout
        self.gridLayout.addWidget(self.checkBox, 1, 1)
        self.gridLayout.addWidget(self.buttons[0], 2, 1)
        self.gridLayout.addWidget(self.buttons[1], 2, 3)
        self.gridLayout.addWidget(self.buttons[2], 2, 5)

        self.gridLayout.addWidget(self.buttons[3], 4, 1)
        self.gridLayout.addWidget(self.buttons[4], 4, 3)
        self.gridLayout.addWidget(self.buttons[5], 4, 5)

        self.gridLayout.addWidget(self.buttons[6], 6, 1)
        self.gridLayout.addWidget(self.buttons[7], 6, 3)
        self.gridLayout.addWidget(self.buttons[8], 6, 5)

        self.gridLayout.addWidget(self.decos[0], 2, 2, 5, 1)
        self.gridLayout.addWidget(self.decos[1], 2, 4, 5, 1)
        self.gridLayout.addWidget(self.decos[2], 3, 1)
        self.gridLayout.addWidget(self.decos[3], 3, 3)
        self.gridLayout.addWidget(self.decos[4], 3, 5)
        self.gridLayout.addWidget(self.decos[5], 5, 1)
        self.gridLayout.addWidget(self.decos[6], 5, 3)
        self.gridLayout.addWidget(self.decos[7], 5, 5)

        self.gridLayout.addItem(spacerItem, 6, 6)
        self.gridLayout.addItem(spacerItem1, 6, 0)
        self.gridLayout.addItem(spacerItem2, 9, 3)

        self.gridLayout.addWidget(self.label, 11, 1, 1, 5)
        self.gridLayout.addWidget(self.pushButton, 10, 1, 1, 5)

        self.setLayout(self.gridLayout)
        self.setStyleSheet('''
        background-color: white''')

        # Timer for delay between wins and clears
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.delay)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clear)


    def clicked_connect(self, number):
        """Connects click to self.add_grade. (Exists for readability)

        :param number int: index to add to the board
        :return: None
        """

        self.add_grade(number)


    def add_grade(self, number):
        """Add a grade. Also switches the symbol, because a turn is made. Connect with self.update_buttons

        :param number int: index to add to the board
        :return: None
        """

        if self.board[number] == '':
            self.board[number] = self.symbol

            if self.symbol == 'X':
                self.symbol = 'O'
            else:
                self.symbol = 'X'


        self.buttons[number].setDisabled(True)
        self.update_buttons()


    def update_buttons(self):
        """Update buttons with the values on self.board and assign it to the buttons in the GUI.
        Connect with check win.
        Append self.check_win to self.results

        :return: None
        """

        for i in range(9):
            self.buttons[i].setText(f'{self.board[i]}')
        x = self.check_win()
        if x is not None:
            self.results.append(x)


    def check_win(self):
        """Check if the current board is winning or not.

        :return: self.symbol if win, 'Tie' if tie
        """

        for i in range(3):
            # Horizontal
            if self.board[0+(i*3)] == self.board[1+(i*3)] == self.board[2+(i*3)] and self.board[0+(i*3)] != '':
                self.won([0+(i*3), 1+(i*3), 2+(i*3)])
                return self.symbol

            # Vertical
            if self.board[0+i] == self.board[3+i] == self.board[6+i] and self.board[0+i] != '':
                self.won([0+i, 3+i, 6+i])
                return self.symbol

            # Diagonals
            if self.board[0] == self.board[4] == self.board[8] and self.board[0] != '':
                self.won([0, 4, 8])
                return self.symbol

            if self.board[2] == self.board[4] == self.board[6] and self.board[2] != '':
                self.won([2, 4, 6])
                return self.symbol

            # Tie
            if '' not in self.board:
                self.won()
                return 'Tie'

        # If it is Os turn, then let AI do the decision.
        # ai.best_move() Returns the index for the new grade
        if self.symbol == 'O':
            ai = BoardAI(self.board, self.symbol)
            self.add_grade(ai.best_move())

        # Random grade
        if self.checkBox.isChecked():
            self.timer.setInterval(0)
            self.random()
        else:
            self.timer.setInterval(self.delay)

        self.update_labels()
        return None


    def won(self, positions=-1):
        """Win. Make the lines that won bold.

        :param positions list or int: the indexes where the player won, or the line. If positions is -1 then tie.
        :return: None
        """

        # Enable buttons (because when they are clicked they get disabled)
        for x in self.buttons:
            self.buttons[x].setDisabled(True)

        # Make the lines bold
        font = QtGui.QFont()
        font.setBold(True)

        if positions != -1:
            for i in positions:
                self.buttons[i].setStyleSheet(f'''
            QPushButton:!hover{{
            background-color: none;
            border: none;
            
            color: red;
            font-size: 55px;
            font-family: Segoe UI
            }}
            
            QPushButton:hover{{
            background-color: #cfcfcf;
            border: none
            }}

            QPushButton:pressed{{
            background-color: #828282
            }}
            ''')
                self.buttons[i].setFont(font)
        else:
            # Tie, make all bold
            for x in self.buttons:
                self.buttons[x].setStyleSheet(f'''
                QPushButton:!hover{{
                background-color: none;
                border: none;

                color: red;
                font-size: 55px;
                font-family: Segoe UI
                }}

                QPushButton:hover{{
                background-color: #cfcfcf;
                border: none
                }}

                QPushButton:pressed{{
                background-color: #828282
                }}
                ''')
                self.buttons[x].setFont(font)


        # Starts timer until clear
        self.timer.start()


    def warning(self, text):
        """Display a warning message to the user.

        :param text str: text to show in warning message
        :return: None
        """

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setWindowIcon(QtGui.QIcon("icon.png"))
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.msg.setText(text)
        self.msg.setWindowTitle("Error")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.retval = self.msg.exec_()


    def clear(self):
        """Clear the board and reset values.

        :return: None
        """

        self.board = ['']*9
        font = QtGui.QFont()
        font.setBold(False)

        for x in self.buttons:
            self.buttons[x].setDisabled(False)
            self.buttons[x].setFont(font)
            self.buttons[x].setStyleSheet(f'''
            QPushButton:!hover{{
            background-color: none;
            border: none;
            
            color: black;
            font-size: 55px;
            font-family: Segoe UI
            }}
            
            QPushButton:hover{{
            background-color: #cfcfcf;
            border: none
            }}

            QPushButton:pressed{{
            background-color: #828282
            }}
            ''')

        self.symbol = 'X'
        self.update_buttons()

        # The checkbox is the random checkbox.
        if self.checkBox.isChecked():
            self.random()


    def random(self):
        """Select a random value from availables and add.

        :return: None
        """

        try:
            self.add_grade(self.random_available())
        except ValueError:
            pass

        self.update_labels()


    def update_labels(self):
        """Update labels with win and loss percentage.

        :return: None
        """

        x_win = self.results.count('O')
        o_win = self.results.count('X')
        tie = self.results.count('Tie')
        total = len(self.results)

        try:
            self.label.setText(f'''
        Percentage of X (player, random) winning:   {round((x_win / total) * 100, 4)}%
        Percentage of O (AI) winning: {round((o_win / total) * 100, 4)}%
        Percentage of ties: {round((tie / total) * 100, 4)}%

        Total games: {total}
        Total wins (O): {o_win}
        Total wins (X): {x_win}''')
        except ZeroDivisionError:
            pass


    def random_available(self):
        """Get random available.

        :return: random available from self.board.
        """

        available = [str(index) for index, value in enumerate(self.board) if value == '' and self.buttons[index].isEnabled() == True]
        return int(''.join(random.sample(available, 1)))


    def clear_all(self):
        """Clear every piece of data in the class. (connects with self.clear)

        :return: None
        """

        self.results = []
        self.label.setText('\n'*8)
        self.clear()


# EXEC
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    GUI = Main()
    app.setStyle('Fusion')
    GUI.show()
    sys.exit(app.exec_())
