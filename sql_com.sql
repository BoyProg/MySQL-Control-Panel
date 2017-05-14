CREATE DATABASE name_data;
DROP DATABASE name_data;
DROP TABLE table_name;
CREATE TABLE Name_table(
	id int(3) ;
	name text(14) null;
	password text(14) null;
)
update Name_table set (name="",password="");
ALTER TABLE admin DROP "password";   # delete Columns
DELETE FROM admin WHERE user="alaa"; # delete Data in Colome row
DELETE FROM admin WHERE user;        # delete Columns
ALTER TABLE admin add name_col type(int,text,float);

# name type len default collation attributes null index a_l 
# commends virtuality  MIME type 
