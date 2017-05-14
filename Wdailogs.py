from PySide.QtGui import (QDialog,QLabel,QLineEdit,QTableWidgetItem,
							QPushButton,QFont,QMessageBox,QVBoxLayout,QFormLayout,QHBoxLayout)
from PySide.QtCore import Qt
import edit,WTL




class MsgBox_2(QMessageBox):
	def showMsg(self,msg):
		self.setIcon(self.Warning)
		self.setText("<h4><br > %s </h4>"%msg)
		self.setWindowTitle("Warning")
		self.setStandardButtons(self.Ok)
		self.show()
		self.exec_()



# # Dialog Connect to MySQL  # 
class dialog(QDialog):
	def __init__(self,self_Main,self_mysql):
		super(dialog,self).__init__(self_Main)
		self.my_sql = self_mysql
		self.showMsg = True
		self.setWindowTitle("Connect MySQL")
		host = QLineEdit()
		user = QLineEdit()
		Pass = QLineEdit()
		dbs	 = QLineEdit()
		host.setPlaceholderText("HostName . . .")
		user.setPlaceholderText("UserName . . .")
		Pass.setPlaceholderText("Password . . .")
		dbs.setPlaceholderText ("DataBase . . .")
		vbox = QVBoxLayout(self)
		lis  = (host,user,Pass,dbs)
		for i in lis:
			vbox.addWidget(i)
		but = QPushButton("Connect . . .")
		but.setFlat(True)
		but.clicked.connect(lambda:self.setConfig(host.text(),user.text(),Pass.text(),dbs.text()))
		vbox.addWidget(but)
		self.exec_()
	def closeEvent(self,event):
		if event:
			if self.showMsg:
				event.accept

	def setConfig(self,host,user,Pass='',dbs=''):
		self.config = {'host':host,'user':user,'password':Pass,'database':dbs}
		sh = self.my_sql.connect(**self.config)
		if self.my_sql.do:
			self.showMsg = False 
			self.close()


# Dialogs Action Menu Bar # 
class da_edit():
	def __init__(self,prat,self_mysql,Data_Name,Table_Name):
		
		self.app = prat
		self.mySQL = self_mysql
		self.Data_Name = Data_Name
		self.table_Name = Table_Name
    # Dialogs For Action (Create & Delete Database,, delete Tabel)
	def data(self,a):
		if self.mySQL.do:
			di_ac = {
				"Create Database" : self.mySQL.create_data,
				"Delete Database" : self.mySQL.drop_data,	
			}
			da = QDialog(self.app)
			da.setFixedSize(300,100)
			form = QFormLayout(da)
			lin = QLineEdit()
			lin.setFont(QFont("",14))
			but = QPushButton("%s"%str(a.text()).split(' ')[0])
			but.clicked.connect(lambda:di_ac[a.text()](lin.text()))
			form.addRow(QLabel("<h3>Name Database</h3>"),lin)
			form.setSpacing(30)
			form.addRow(but)
			da.setWindowTitle("%s"%a.text())
			da.exec_()
			self.app.ref = True
		else:
			MsgBox_2().showMsg("Error: Can't Connect to MySQL Server ")

	def drop_table(self,a):
		if self.mySQL.do:
			if self.Data_Name != None:
				da = QDialog(self.app)
				da.setWindowTitle("%s From %s"%(a.text(),self.Data_Name))
				da.setFixedSize(300,100)
				form = QFormLayout(da)
				lin = QLineEdit()
				lin.setFont(QFont("",14))
				but = QPushButton("Delete Table")
				but.clicked.connect(lambda:self.mySQL.drop_table(self.Data_Name,lin.text()))
				form.addRow(QLabel("<h3>Name Table</h3>"),lin)
				form.setSpacing(30)
				form.addRow(but)
				self.app.ref = True
				da.exec_()
			else:
				MsgBox_2().showMsg("Plz Select Database")
		else:
			MsgBox_2().showMsg("Error: Can't Connect to MySQL Server ")


    # This Daiglog Crate Table # 
	def _table(self,a):
		if self.mySQL.do:
			da_2 = QDialog(self.app)
			if self.Data_Name != None:
				da_2.setWindowTitle("%s in %s"%(a.text(),self.Data_Name))
				da_2.resize(500,280)
				line = QLineEdit()
				edi_t = edit.editText()
				but  = QPushButton('Create')
				vbox = QVBoxLayout(da_2)
				form = QFormLayout()
				form.addRow(QLabel("Name Table"),line)
				vbox.addLayout(form)
				vbox.addWidget(edi_t)
				vbox.addWidget(but)
				but.clicked.connect(lambda:self.mySQL.create_table(self.Data_Name,line.text(),edi_t.toPlainText()))
				self.app.ref = True
				da_2.exec_()
			else:
				MsgBox_2().showMsg("Plz Select Database ")

    # This Insert Data in To Table Mysql
	def insert_t(self,a):
		if self.mySQL.do:
			da_3 = QDialog(self.app)
			if self.table_Name != None :
				da_3.setWindowTitle("Insert InTo %s.%s"%(self.Data_Name,self.table_Name))
				da_3.resize(600,100)
				tab = WTL.Table()
				but = QPushButton("Inset")
				tab.setRowCount(1)
				cols = self.mySQL.getColumns(self.Data_Name,self.table_Name)
				tab.setColumnCount(len(cols))
				for ind in range(len(cols)):
					item = QTableWidgetItem
					tab.setHorizontalHeaderItem(ind, item(cols[ind]))
				vbox = QVBoxLayout(da_3)
				vbox.addWidget(tab)
				vbox.addWidget(but)
				but.clicked.connect(lambda:self.mySQL.insert_DT(self.Data_Name,self.table_Name,tab))
				self.app.ref = True
				da_3.exec_()
			else:
				MsgBox_2().showMsg("Plz Select Table %s"%self.Data_Name)

		else:
			MsgBox_2().showMsg("Error: Can't Connect to MySQL Server ")

	# This Update Data #
	def update_t(self,a):
		if self.mySQL.do:
			da_3 = QDialog(self.app);d_list = [];
			if self.table_Name != None :
				da_3.setWindowTitle("Update Table %s.%s"%(self.Data_Name,self.table_Name))
				da_3.resize(600,100)
				tab = WTL.Table()
				line_1 = QLineEdit()
				line_2 = QLineEdit()
				but = QPushButton("Update")
				tab.setRowCount(1)
				cols = self.mySQL.getColumns(self.Data_Name,self.table_Name)
				tab.setColumnCount(len(cols))
				for ind in range(len(cols)):
					item = QTableWidgetItem
					tab.setHorizontalHeaderItem(ind, item(cols[ind]))
				vbox = QVBoxLayout(da_3)
				hbox = QHBoxLayout()
				vbox.addWidget(tab)
				for i in (QLabel("Where: "),line_1,QLabel("="),line_2):
					hbox.addWidget(i)
				vbox.addLayout(hbox)
				vbox.addWidget(but)
				but.clicked.connect(lambda:self.mySQL.update_DT(self.Data_Name,self.table_Name,str(line_1.text()+"='%s'"%line_2.text()),tab))
				self.app.ref = True
				da_3.exec_()
			else:
				MsgBox_2().showMsg("Plz Select Table From %s"%self.Data_Name)
		else:
			MsgBox_2().showMsg("Error: Can't Connect to MySQL Server ")

	# This Delete row From Table #
	def rm_row(self,a):
		if self.mySQL.do:
			da_2 = QDialog(self.app)
			if self.table_Name != None:
				da_2.setWindowTitle("Delete Row From %s.%s"%(self.Data_Name,self.table_Name))
				da_2.setFixedSize(400,50)
				line_1 = QLineEdit()
				line_2 = QLineEdit()
				but  = QPushButton('Delete')
				hbox = QHBoxLayout(da_2)
				for i in (QLabel("Delete Where: "),line_1,QLabel("="),line_2,but):
					hbox.addWidget(i)
				but.clicked.connect(lambda:self.mySQL.delete_Trow(self.Data_Name,self.table_Name,str(line_1.text()+"='%s'"%line_2.text())))
				self.app.ref = True
				da_2.exec_()
			else:
				MsgBox_2().showMsg("Select  Table  From %s"%self.Data_Name)
		else:
			MsgBox_2().showMsg("Error: Can't Connect to MySQL Server ")
	# Delete Column Form Table MySQL #
	def delete_Tcol(self,a):
		if self.mySQL.do:
			da_2 = QDialog(self.app)
			if self.table_Name != None:
				self.app.ref = True
				da_2.setWindowTitle("Delete Column From %s.%s"%(self.Data_Name,self.table_Name))
				da_2.setFixedSize(300,50)
				line_1 = QLineEdit()
				but  = QPushButton('Delete')
				hbox = QHBoxLayout(da_2)
				for i in (QLabel("Name Column: "),line_1,but):
					hbox.addWidget(i)
				but.clicked.connect(lambda:self.mySQL.delete_Tcol(self.Data_Name,self.table_Name,str(line_1.text())))
				da_2.exec_()
			else:
				MsgBox_2().showMsg("Select  Table From  %s"%self.Data_Name)		
		else:
			MsgBox_2().showMsg("Error: Can't Connect to MySQL Server ")
	# add Column Into Table Mysql
	def add_col(self,a):
		if self.mySQL.do:
			da_2 = QDialog(self.app)
			if self.table_Name != None:
				self.app.ref = True
				da_2.setWindowTitle("Delete Column From %s.%s"%(self.Data_Name,self.table_Name))
				da_2.setFixedSize(600,50)
				line_1 = edit.editText()
				but  = QPushButton('ADD')
				hbox = QHBoxLayout(da_2)
				for i in (QLabel("New Column: "),line_1,but):
					hbox.addWidget(i)
				but.clicked.connect(lambda:self.mySQL.add_Tcol(self.Data_Name,self.table_Name,line_1.toPlainText()))
				da_2.exec_()
			else:
				MsgBox_2().showMsg("Select  Table From %s"%self.Data_Name)		
		else:
			MsgBox_2().showMsg("Error: Can't Connect to MySQL Server ")
