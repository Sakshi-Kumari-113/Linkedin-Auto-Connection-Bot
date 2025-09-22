import mysql.connector
from prettytable import PrettyTable
from configparser import ConfigParser


#Setting up Config file
file = 'config.ini'
config = ConfigParser()
config.read(file)


class DataBase:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=config['MySQL Credentials']['MYSQL_HOST'],
            user=config['MySQL Credentials']['MYSQL_USER'],
            password=config['MySQL Credentials']['MYSQL_PASSWORD'],
            database=config['MySQL Credentials']['MYSQL_DATABASE']
        )
        self.mycursor = self.db.cursor()
    def Create_Table(self):
        create_table_query = f"CREATE TABLE profile (Name Varchar(50),Position Varchar(500),LinkedIN_ID Varchar(500),Phone_no int,Email_ID varchar(200),Connection_Request varchar(50),Primary Key(LinkedIN_ID))"
        self.mycursor.execute(create_table_query)

    def Describe(self,describe=False):
      self.mycursor.execute("Describe profile")
      rows = self.mycursor.fetchall()
      table = PrettyTable()
      table.field_names = ["Field", "Type", "Null", "Key", "Default", "Extra"]
      for row in rows:
        table.add_row(row)

      if describe:
        print(table)
      field_column = [row[0] for row in rows]
      return field_column

    def Show_Content(self):

      table = PrettyTable()
      table.field_names = self.Describe()
      self.mycursor.execute("Select * from profile")
      rows = self.mycursor.fetchall()
      for row in rows:
        table.add_row(row)
      print(table)


if __name__=="__main__":
    db_obj = DataBase()
    db_obj.Create_Table()
    db_obj.Describe(describe=True)
    db_obj.Show_Content()



