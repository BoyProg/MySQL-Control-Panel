from PySide.QtGui import *
from PySide.QtCore import *
import re

class syntax(QSyntaxHighlighter):
	def __init__(self,parent):
		super(syntax,self).__init__(parent)
		self.highlightRules = []
		keyword = QTextCharFormat()
		keyword.setForeground(QColor(249,38,89))
		keywords = open('SQL_COM.TXT','r').read().split("\n")
		for i in keywords:
			self.highlightRules.append((QRegExp("\\b%s\\b"%i),keyword))

		keyword = QTextCharFormat()
		keyword.setForeground(QColor(Qt.blue))
		self.highlightRules.append((QRegExp(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b'),keyword))

	def highlightBlock(self,text):
		for pattern, form in self.highlightRules:
			expression = QRegExp(pattern)
			index = expression.indexIn(text)
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat(index, length, form)
				index = expression.indexIn(text, index + length)


class editText(QTextEdit):
	def __init__(self):
		super(editText,self).__init__()
		self._completer = None
		self.setStyleSheet("""
			color:black;
			background-color:#eec;
			selection-background-color:rgb(73,72,62);
			font-size:14px;
			""")
		self.completer = QCompleter(self)
		self.completer.setModel(QStringListModel(
			['BIGINT', 'INTEGER', 'INT', 'SMALLINT', 'TINYINT',
			 'BIT', 'DECIMAL','NUMERIC', 'MONEY','SMALLMONEY', 'FLOAT',
			 'REAL', 'DATETIME','SMALDATETIME','DATE', 'TIME', 'CHAR',
			 'VARCHAR', 'TEXT', 'NCHAR', 'NVARCHAR', 'NTEXT','BINARY',
			 'VARBINARY', 'IMAGE', 'AUTO_INCREMENT', 'UNSIGNED',
			 'PRIMARY KEY','NOT NULL', 'NULL', 'DEFAULT','UNIQUE',
			 'REFERENCES','CUSTOMERS', 'FOREIGN KEY', 'CHECK'
			  ]))
		#self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
		self.completer.setWrapAround(False)
		self.setCompleter(self.completer)
		self.syntax = syntax(self.document())
		self.cursorPositionChanged.connect(self.positionInBlock)


	def setCompleter(self, c):
		if self._completer is not None:
			self._completer.activated.disconnect()

		self._completer = c

		c.setWidget(self)
		c.setCompletionMode(QCompleter.PopupCompletion)
		c.setCaseSensitivity(Qt.CaseInsensitive)
		c.activated.connect(self.insertCompletion)

	def completer(self):
		return self._completer

	def insertCompletion(self, Textcomplet):

		tc = self.textCursor()
		tc.movePosition(tc.StartOfWord,tc.MoveAnchor)
		tc.select(tc.WordUnderCursor)
		tc.insertText(Textcomplet)
		self.setTextCursor(tc)

	def positionInBlock(self):
		tc1 = self.textCursor()
		return (tc1.position())
		
	def getText(self):
		return self.toPlainText()

	def textUnderCursor(self):
		tc = self.textCursor()
		tc.select(tc.WordUnderCursor)  
		s = (tc.selectedText())
		if not self.positionInBlock()-1 == -1:
			if s != ' ' :
				try:
					return s[:s.rindex(self.getText()[self.positionInBlock()-1])+1]
				except:
					return ' '
		else:
			return ' '


	def keyPressEvent(self, e):
		if self._completer is not None and self._completer.popup().isVisible():
		# The following keys are forwarded by the completer to the widget.
			if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape,Qt.Key_Tab, Qt.Key_Backtab):
				e.ignore()
		# Let the completer do default behavior.
				return

		isShortcut = ((e.modifiers() & Qt.ControlModifier) != 0 and e.key() == Qt.Key_E)
		if self._completer is None or not isShortcut:
		# Do not process the shortcut when we have a completer.
			super(editText, self).keyPressEvent(e)

		ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
		if self._completer is None or (ctrlOrShift and len(e.text()) == 0):
			return

		eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
		hasModifier = (e.modifiers() != Qt.NoModifier) and not ctrlOrShift
		completionPrefix = self.textUnderCursor()

		if not isShortcut and (hasModifier or len(e.text()) == 0 or len(completionPrefix) < 1 or e.text()[-1] in eow):
			self._completer.popup().hide()
			return

		if completionPrefix != self._completer.completionPrefix():
			self._completer.setCompletionPrefix(completionPrefix)
			self._completer.popup().setCurrentIndex(
			self._completer.completionModel().index(0, 0))

		cr = self.cursorRect()
		cr.setWidth(self._completer.popup().sizeHintForColumn(0) + self._completer.popup().verticalScrollBar().sizeHint().width())
		self._completer.complete(cr)

