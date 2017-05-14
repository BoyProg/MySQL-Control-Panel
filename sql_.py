import mysql.connector as db

refresh = "Functuon main_app.refresh_"

class MsgBox():
	def __init__(self,MsageBox):
		self.msg = MsageBox()
	def setMsg(self,msg):
		self.msg.setIcon(self.msg.Warning)
		self.msg.setText("<h4><br > %s </h4>"%msg)
		self.msg.setWindowTitle("Warning")
		self.msg.setStandardButtons(self.msg.Ok | self.msg.Cancel)
		self.msg.show()
		self.msg.exec_()

class MySQL(object):
	off = None
	def __init__(self,msg):
		super(MySQL, self).__init__()
		self.do = None
		self.msg = MsgBox(msg)

	def connect(self,**conf):
		self.config = conf
		try:
			self.con = db.connect(**self.config)
			self.cur = self.con.cursor(buffered=True,dictionary=True)
			self.do = True
		except db.Error as er:
				self.do = False
				self.msg.setMsg("\n"+er.msg.split("(")[0])
	def close_all(self):
		self.con.close()
		self.cur.close()

	def getDataBase(self):
		if self.do:
			try:
				li_d = []
				self.cur.execute("show databases;")
				for i in self.cur.fetchall():
					li_d.append(i['Database'])
				return li_d
			except db.Error as er :
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])



	def getColumns(self,data,table):
		if self.do:
			try:
				NCol = []
				self.cur.execute("use %s;"%data)
				for i in self.cur.execute("show columns from %s"%(table),multi=True):

					if i.with_rows:
						for j in i.fetchall():

							NCol.append(j["Field"])
				return (NCol)
			except db.Error as er :
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])

	def dataCol(self,DataBase,NTabel):
		if self.do:
			try:
				col = self.getColumns(DataBase,NTabel);dic={};row_len = []
				for i in col :
					dic.update({i:[]})
				self.cur.execute("use %s;"%DataBase)
				self.cur.execute("select * from %s where 1"%(NTabel))
				a = self.cur.fetchall()
				for i in a:
					for j in col:
						dic[j].append(i[j])
				for i in dic:
					row_len.append(len(dic[i]))
				row_len.sort()
				return(dic,row_len[-1])
			except db.Error as er:
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])
		

	def getTables(self,data):
		if self.do:
			try :
				self.cur.execute("SHOW TABLES FROM %s;"%data)
				n = []
				for i in self.cur.fetchall():
					n.append(i["Tables_in_%s"%data])
				return n
			except db.Error as er :
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])

	# craete
	def create_data(self,name):
		if name.strip() != "":
			try:
				self.cur.execute("CREATE DATABASE %s;"%name)
				refresh()
			except db.Error as er :
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])
		else:
			self.msg.setMsg("\n Name Is Empty")
	def create_table(self,N_data,N_table,t_info):
		if N_table.strip() != "":
				try:
					self.cur.execute("use %s;"%N_data)
					self.cur.execute("CREATE TABLE %s (%s)"%(N_table,t_info))
					self.con.commit()
					refresh()
				except db.Error as er :
					if er:
						self.msg.setMsg("\n"+er.msg.split("(")[0])
		else:
			self.msg.setMsg("\n Table Name Is Empty (=_=)!")
	# drop 
	def drop_data(self,name):
		try:
			if name.strip() != '' :
				self.cur.execute("DROP DATABASE %s;"%name)
				self.con.commit()
				refresh()
			else:
				self.msg.setMsg("\n Name Is Empty ")
		except db.Error as er :
			if er:
				self.msg.setMsg("\n"+er.msg.split("(")[0])
	def drop_table(self,da,tb):
		try:
			if tb.strip() != '':
				self.cur.execute("DROP TABLE %s.%s;"%(da,tb))
				refresh()
			else:
				self.msg.setMsg("Name Is Empty")
		except db.Error as er:
			if er:
				self.msg.setMsg("\n"+er.msg.split("(")[0])
	## end 
	def insert_DT(self,dt,ntb,tb):
		dc_d_table = {"cols":[],'values':[]}
		for i in range(0,tb.columnCount()):
			n_C = tb.horizontalHeaderItem(i).text()
			if not str(tb.item(0,i)) == "None":
				v = tb.item(0,i).text()
				if v != "":
					dc_d_table["cols"].append(n_C)
					dc_d_table["values"].append("'%s'"%v)
		try:
			self.cur.execute("INSERT INTO %s.%s (%s) VALUES (%s);"%(dt,ntb,(",".join(dc_d_table['cols'])),(','.join(dc_d_table["values"]))))
			self.con.commit()
			refresh()
			tb.clearContents ()
		except db.Error as er :
			if er:
				self.msg.setMsg("\n"+er.msg.split("(")[0])
	def update_DT(self,dt,ntb,where,tb):
		li_d_table = []
		for i in range(0,tb.columnCount()):
			n_C = tb.horizontalHeaderItem(i).text()
			if not str(tb.item(0,i)) == "None":
				v = tb.item(0,i).text()
				if v != "":
					li_d_table.append(str("%s='%s'"%(n_C,v)))

		arg_update = ",".join(li_d_table)
		if not "" in where.split("="):
			try:
				self.cur.execute("UPDATE %s.%s SET %s WHERE %s"%(dt,ntb,arg_update,where))
				self.con.commit()
				tb.clearContents()
				refresh()
			except db.Error as er :
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])
		else:
			self.msg.setMsg("\n Error In Where")
	def delete_Trow(self,dt,ntb,where):
		if not "" in where.split("="):
			try:
				self.cur.execute("DELETE FROM %s.%s WHERE %s;"%(dt,ntb,where))
				self.con.commit()
				refresh()
			except db.Error as er :
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])
		else:
			self.msg.setMsg("\n Error In Where")

	def delete_Tcol(self,dt,ntb,n_col):
		if n_col.strip() != "":
			try:
				self.cur.execute("ALTER TABLE %s.%s DROP %s;"%(dt,ntb,n_col))
				self.con.commit()
				refresh()
			except db.Error as er :
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])
		else:
			self.msg.setMsg("\n Name Column is Empty")

	def add_Tcol(self,dt,ntb,info_col):
		if info_col.strip() != "":
			try:
				self.cur.execute("ALTER TABLE %s.%s ADD %s "%(dt,ntb,info_col))
				self.con.commit()
				refresh()
			except db.Error as er :
				if er:
					self.msg.setMsg("\n"+er.msg.split("(")[0])
		else:
			self.msg.setMsg("\n Name Column is Empty")


	def returnConfig(self):
		return self.config


# # Test # #
# mysql = MySQL("Hello")
# config = {"host":"127.0.0.1","user":"root",'database':''}
# mysql.connect(**config)
# mysql.sql_muillte('show databases; use test; select * from boy;')
# mysql.con.commit()
# # end # #