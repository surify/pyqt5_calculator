#!/usr/bin/env python

"""
THIS IS A BASIC CALCULATOR APPLICATION.
PYTHON3 AND PYQT5 MUST BE INSTALLED.
AUTHOR: P SURYA TEJA
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QApplication, QTextBrowser,
                             QLineEdit, QPushButton, QGridLayout)
from PyQt5.QtGui import QIcon


class Calculator(QWidget):
    """
    Creates the calculator window, adds the buttons and display panels.
    """
    def __init__(self, parent=None):
        """This method creates all the widgets, adds them to the layout
        and show the widget.
        """
        super(Calculator, self).__init__(parent)

        # result is displayed in this widget
        self.browser = QTextBrowser()
        self.browser.setFixedHeight(100)
        self.browser.setFocusPolicy(Qt.NoFocus)

        # user input is displayed in this widget
        # this is the only widget with focus in the entire application
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText('Press Enter to View Result')
        self.input_box.setFixedHeight(30)
        self.input_box.setAlignment(Qt.AlignRight)
        self.input_box.returnPressed.connect(self.calculate_result)

        # creating the buttons
        number_buttons_text = '0123456789'
        number_buttons = []

        # creating the number buttons with a loop as they are all similar
        for each in number_buttons_text:
            number_buttons.append(self.create_button(each))
        button_add = self.create_button('+', tooltip="Addition [+]")
        button_sub = self.create_button('-', tooltip="Subtraction [-]")
        button_mul = self.create_button('×', tooltip="Multiplication [*]")
        button_div = self.create_button('÷', tooltip="Division [/]")
        button_mod = self.create_button('%', tooltip="Remainder [%]")
        button_dot = self.create_button('.')
        button_eq_style = "QPushButton {background-color:#0077ff; color:white; font-size: 20px;}"
        button_eq = self.create_button('=', size=(50, 75),
                                       stylesheet=button_eq_style, slot=self.calculate_result,
                                       tooltip="Calculate Result")
        button_clear = self.create_button('Clear',
                                          slot=self.input_box.clear,
                                          tooltip="Clear Display [Esc]")
        button_undo = self.create_button('Undo',
                                         slot=self.input_box.undo,
                                         tooltip="Undo [Ctrl+Z]")

        # creating the layout and adding buttons, input and output widgets
        layout = QGridLayout()
        layout.addWidget(self.browser, 0, 0, 1, 5)
        layout.addWidget(self.input_box, 1, 0, 1, 5)
        layout.addWidget(number_buttons[1], 2, 0)
        layout.addWidget(number_buttons[2], 2, 1)
        layout.addWidget(number_buttons[3], 2, 2)
        layout.addWidget(button_add, 2, 3)
        layout.addWidget(button_clear, 2, 4)
        layout.addWidget(number_buttons[4], 3, 0)
        layout.addWidget(number_buttons[5], 3, 1)
        layout.addWidget(number_buttons[6], 3, 2)
        layout.addWidget(button_sub, 3, 3)
        layout.addWidget(button_undo, 3, 4)
        layout.addWidget(number_buttons[7], 4, 0)
        layout.addWidget(number_buttons[8], 4, 1)
        layout.addWidget(number_buttons[9], 4, 2)
        layout.addWidget(button_mul, 4, 3)
        layout.addWidget(button_eq, 4, 4, 2, 1)
        layout.addWidget(button_mod, 5, 0)
        layout.addWidget(number_buttons[0], 5, 1)
        layout.addWidget(button_dot, 5, 2)
        layout.addWidget(button_div, 5, 3)

        # setting some window properties
        self.setLayout(layout)
        self.setFixedSize(self.sizeHint())
        self.setWindowTitle("Calculator")
        self.show()

    def create_button(self, text=None, icon=None, tooltip=None,
                      size=None, stylesheet=None, slot=None):
        """Creates a button and sets its properties
        """
        # setting button's text
        if text:
            button = QPushButton(text)

        # if there is no text and there's an icon it will be set
        elif icon:
            button = QPushButton(QIcon(icon), '')

        # if there is no text and no icon the text 'button' will be used
        else:
            button = QPushButton('button')

        # setting button's tooltip
        if tooltip:
            button.setToolTip(tooltip)

        # setting button's size
        if size:
            button.setFixedSize(size[0], size[1])
        else:
            button.setFixedSize(50, 35)

        # setting button's styles
        if stylesheet:
            button.setStyleSheet(stylesheet)

        # connecting button to slot
        if slot:
            button.clicked.connect(slot)
        else:
            button.clicked.connect(self.update_input_box)
        button.setFocusPolicy(Qt.NoFocus)
        return button

    def key_press_event(self, event):
        """ Pressing escape key clears input box
        """
        if event.key() == Qt.Key_Escape:
            self.input_box.clear()
        # if event.key() in (Qt.Key_Return, Qt.Key_Enter):
        #     self.calculate_result()

    def update_input_box(self):
        """ Takes input from number buttons and operator buttons
            and adds them to the input screen. If 'equals to' button
            is pressed it calls the calculate_result method.
        """
        text = self.sender().text()
        if text != '=':
            self.input_box.insert(text)
        else:
            self.calculate_result()

    def calculate_result(self):
        """ Calculates the result of the expression in the input box
        and displayes it in the text browser.
        If there is an error, an error message is displayed in the browser.
        """
        text = self.input_box.text()

        # executes only if the input box is not empty
        if text:
            # replacing multiplication and division symbols with their programmatic counterparts
            replacements = {'×': '*', '÷': '/'}
            for each in replacements:
                text = text.replace(each, replacements[each])
            try:
                result = eval(text)
                self.browser.append("{} = <b>{}</b>".format(text, str(result)))
                self.input_box.clear()
                self.input_box.insert(str(result))

            # if there is any error in the expression entered it is shown in the text browser
            except Exception:
                self.browser.append("<font color=red>{}"
                                    "</font>".format('Expression is Invalid'))
                self.input_box.selectAll()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    app.exec_()
