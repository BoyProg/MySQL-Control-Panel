from PySide.QtGui import (QTreeWidget,QTableWidget,
							QTableWidgetItem,QTreeWidgetItem,QWidget,
							QLabel,QVBoxLayout,QSplitter,
							QFont)
import edit

class treeWidget(QTreeWidget):
	def __init__(self,mysql):
		super(treeWidget,self).__init__()
		self.mysql = mysql;self.li = []
		self.headerItem().setText(0,"Database")

	def add_to_tree(self):
		if self.mysql.do:
			self.nDataBase = self.mysql.getDataBase()
			for i in self.nDataBase:
				item_m = QTreeWidgetItem(self)
				item_m.setStatusTip(0,'main')
				item_m.setText(0,"%s"%i)
				if i in self.li:
					item_m.setExpanded(True)
				self.table = self.mysql.getTables(i)
				for j in self.table:
					item_c = QTreeWidgetItem(item_m)
					item_c.setStatusTip(0,i)
					item_c.setText(0,"%s"%j)



class Table(QTableWidget):
	def __init__(self):
		super(Table,self).__init__()

		
class label (QLabel):
	def __init__(self,text):
		super(label,self).__init__()
		self.setText(text)
		self.setFont(QFont("",10))
		self.setFixedHeight(35)


class Window(QWidget):
	def init(self,self_mysql):
		self.ref = False;self.ndb = False;
		self.Data_Name = None; self.table_Name=None;
		
		self.mysql = self_mysql
		self.table = Table()
		self.tree  = treeWidget(self.mysql)
		text 	   = ("<center><h1 style=';color:Lightblue;'>MySQL<small style='color:#0099CC;'> Control Panel</small></h1></center>")
		self.vbox  = QVBoxLayout(self)
		self.split = QSplitter()
		self.tree.setHidden(True)
		self.tree.itemClicked.connect(self.setInTable)
		self.tree.itemExpanded.connect(self.expand)
		self.tree.itemCollapsed.connect(self.collaps)
		self.split.addWidget(self.tree)
		self.split.addWidget(self.table)
		self.split.setSizes([60,400])
		self.vbox.addWidget(label(text))
		self.vbox.addWidget(self.split)
		self.vbox.setContentsMargins(-18,-18,-18,-18)
	def expand(self,it):
		if it.isExpanded():
			if not it.text(0) in self.tree.li:
				self.tree.li.append(it.text(0))
	def collaps(self,it):
		if it.text(0) in self.tree.li:
			self.tree.li.remove(it.text(0))
	# set Name 'database & table' in TreeList # 
	def con(self):
		self.tree.clear()
		if self.tree.isHidden:
			self.tree.setHidden(False)
		self.tree.headerItem().setText(0,self.Data_Name)
		self.tree.add_to_tree()
		self.ref = True

	def setInTable(self,nt):
		if not str(nt).startswith('<'):
			table = nt
			self.table_Name = nt
		else:
			if nt.statusTip(0) != 'main':
				self.tree.headerItem().setText(0,nt.statusTip(0))
				self.ndb = nt.statusTip(0)
				self.Data_Name = nt.statusTip(0)
				self.table_Name = nt.text(0)
			else:
				self.tree.headerItem().setText(0,nt.text(0))
				self.Data_Name = nt.text(0)
				self.table_Name = None
		if self.ndb:
			if self.table_Name in self.mysql.getTables(self.Data_Name):
				self.setDataInTable(self.table_Name)
				self.ref = True
		else:
			pass

	# Set Data Table In TableWidget #
	def setDataInTable(self,tab):
		Icol = 0
		if self.ndb:
			data_dic = self.mysql.dataCol(self.ndb,tab)
			cols = self.mysql.getColumns(self.ndb,tab)
			self.table.setColumnCount(len(cols))
			if data_dic != None :
				self.table.setRowCount(int(data_dic[1]))
				for col in cols:
					item = QTableWidgetItem
					self.table.setHorizontalHeaderItem(Icol, item(col))
					Irow = 0
					for row in data_dic[0][col]:
						self.item = QTableWidgetItem(str(row))
						self.item.setFont(QFont("andalus",12))
						self.table.setItem(Irow,Icol,self.item)
						Irow+=1
					Icol+=1