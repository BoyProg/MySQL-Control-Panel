#####

##{
# Name     : Boy Programmer 
# FaceBook : https://www.facebook.com/boy.programmer
## }

##{
# This Application can : 
# # # # # # # View Data Table 
		# # # AND (
			# 1- add and delete database 
			# 2- add and delete table 
			# 3- update and insert data into table
			# 4- delete and add column 
			# 5- delete row form table 
		# # #	)
# # # # # # # (^_-) (^_^) 
## }
####
from PySide.QtGui import *
import sql_,WTL,Wdailogs
#########################
# WTL             :~class( 'edit', 'label', 'treeWidget','Table', 'Window')
# Wdailogs        :~('da_edit', 'dialog', 'edit', 'tEdit_sql', MsgBox_2)
#sql_.class(MySQL):~['add_Tcol', 'close_all', 'connect', 'create_data','drop_data',
					# .. 'create_table', 'dataCol', 'delete_Tcol', 'delete_Trow', 
					# .. 'drop_table', 'getColumns', 'getDataBase', 'getTables',
					# .. 'insert_DT', 'off', 'returnConfig', 'update_DT']
########################




# # MessageBox  # 
class MsgBox(QMessageBox):
	def __init__(self):
		super(MsgBox,self).__init__()
		self.on = None
	def showMsg(self,msg):
		self.resize(1600,400)
		self.setIcon(self.Warning)
		self.setText("<h4><br > %s </h4>"%msg)
		self.setWindowTitle("Warning")
		self.setStandardButtons(self.Yes | self.No)
		self.buttonClicked.connect(self.ret)
		self.show()
		self.exec_()
	def ret(self,g):
		self.on = str(g.text()).strip("&")
### End




class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		self.setStyleSheet(open('s/app.css','r').read()) # Style For Window # 
		self.ref = False #
		self.resize(800,400)
		self.setContentsMargins(-6,-6,-6,-6)
		self.setMinimumSize(600,300)
		self.setWindowTitle("MySQL Control Panel")
		self.setWindowIcon(QIcon("ico.png"))
		self.setUpAction()
		self.win = WTL.Window()
		self.mySQL = sql_.MySQL(QMessageBox) 
		self.win.init(self.mySQL)
		self.win.ref = self.ref
		sql_.refresh = self.refresh_
		self.setCentralWidget(self.win)

	# Run Dialog Connect # 
	def connect_(self):
		Wdailogs.dialog(self,self.mySQL)
		if self.mySQL.do:
			self.win.con()


	# This is Action Menue Bar # Get From Wdailogs # 
	def Edit(self,text):
		self.da_edit = Wdailogs.da_edit(self,self.mySQL,self.win.Data_Name,self.win.table_Name)
		
		dic_ = {
			"Create Database" : self.da_edit.data,
			"Delete Database" : self.da_edit.data,
			"Delete Table"    : self.da_edit.drop_table,
			"Create Table"	  : self.da_edit._table,
			"Insert Data"     : self.da_edit.insert_t,
			"UpDate Data"     : self.da_edit.update_t,
			"Delete Row"      : self.da_edit.rm_row,
			"Delete Column"	  : self.da_edit.delete_Tcol,
			"add Column"      : self.da_edit.add_col
		}
		dic_[text.text()](text)

	# This refresh All Widget #
	def refresh_(self):
		if self.mySQL.do:
			if self.win.ref:
				self.mySQL.connect(**self.mySQL.returnConfig())
				self.win.con()
				if self.win.Data_Name in self.mySQL.getDataBase():
						if self.win.table_Name in self.mySQL.getTables(self.win.Data_Name):
							self.win.setInTable(self.win.table_Name)
						else:
							self.win.table.clear();self.win.table.setRowCount(0)
							self.win.table.setColumnCount(0)
				else:
					self.win.table.clear();self.win.table.setRowCount(0)
					self.win.table.setColumnCount(0)
				
	def setUpAction(self):
	# Menue Bar # 
		bar  = self.menuBar() # 0
		main = bar.addMenu("Main") # 1
		edit = bar.addMenu("Edit") # 2

	### Main #
		self.connect = QAction('Connect',self,triggered=self.connect_)
		self.refresh = QAction('Refresh',self,triggered=self.refresh_)
		self._exit = QAction('Exit',self,triggered=self.close)
		# ### EndMain #

	### Edite #
		database = edit.addMenu("Database")
		table = edit.addMenu("Table")




		# database
		self.cr_data = QAction('Create Database',self,triggered=lambda:self.Edit(self.cr_data))
		self.rm_data = QAction('Delete Database',self,triggered=lambda:self.Edit(self.rm_data))

  		# TABLE
		self.cr_table = QAction('Create Table',self,triggered=lambda:self.Edit(self.cr_table))
		self.rm_table = QAction('Delete Table',self,triggered=lambda:self.Edit(self.rm_table))
		self.Insert_  = QAction('Insert Data',self,triggered=lambda:self.Edit(self.Insert_))
		self.Up_date  = QAction('UpDate Data',self,triggered=lambda:self.Edit(self.Up_date))
		self.rm_row_   = QAction('Delete Row',self,triggered=lambda:self.Edit(self.rm_row_))
		self.ad_col   = QAction('add Column',self,triggered=lambda:self.Edit(self.ad_col))
		self.rm_col   = QAction('Delete Column',self,triggered=lambda:self.Edit(self.rm_col))
		# ### End Edit #


	## add Action 
		# Main #
		main.addAction(self.connect) # 1
		main.addAction(self.refresh) # 2
		main.addAction(self._exit)   # 3
		
		#Edit.Database#
		database.addAction(self.cr_data) # 1
		database.addAction(self.rm_data) # 2
		#Edit.Table#
		table.addAction(self.cr_table) 	 # 1
		table.addAction(self.rm_table)   # 2
		table.addAction(self.Insert_)  	 # 3
		table.addAction(self.Up_date)  	 # 4
		table.addAction(self.rm_row_)    # 5
		table.addAction(self.ad_col)     # 6
		table.addAction(self.rm_col)   	 # 7
		# # endAdd ###


	def closeEvent(self,event):
		msg = MsgBox()
		if event:
			msg.showMsg('Exit')
			if msg.on == 'Yes':
				if self.mySQL.do:
					self.mySQL.close_all()
				event.accept()
			else:
				event.ignore()


def run():
	import sys
	app = QApplication(sys.argv)
	MainWin = MainWindow()
	MainWin.show()
	app.exec_()
if __name__ == '__main__':
	run()