import sqlite3

class Database:
	__cursor=None
	__connection=None
	def __find_table(self, table_name):
		self.__cursor.execute('.tables ?', table_name);
		return self.__cursor.fetchall()
	def __create_table(self, table_name, values):
		command='create table if not exists %s (%s)' % ( table_name, ', '.join([ item[0]+' '+(item[1] if item[1] else 'text') for item in values.items() ]))
		self.__cursor.execute(command)
	def __init__(self, name, initial_state):
		self.initial_state=initial_state
		self.__connection=sqlite3.connect(name)
		self.__cursor=self.__connection.cursor()
		self.__create_table('users',{'user_id':'text','state':'text'})
		self.__create_table('interactions',{'required_state':'text','state_change':'text','message':'text'})
		self.__create_table('commands',{'command':'text', 'interaction_id':'int'})
		self.__connection.commit()
	def add_user(self, user_id):
		pass
	def link_statement_to_interaction(self, statement, interaction_id):
		pass
	def add_interaction(self):
		pass
	def find_interaction(self):
		pass
	def find_user(self):
		pass
	
#import os
#import sqlite3
#import cmd
#from collections import OrderedDict

#database=Database('test.db',{})

#def parse_variable(variable):
#  match=var_regex.findall(variable)
#  if len(match)==1:
#    return match[0];
#  elif len(match)==1:
#    raise Exception("parse_variable didn't find any matches to the variable "+variable)
#  else:
#    raise Exception('parse_variable: should only find one match to variable, found multiple('+len(match)+') in '+variable)
#
#def search(variable):
#  try:
#    (table,conditions,returns)=parse_variable(variable)
#  except:
#    return []
#  wheres=dict([(i[0],i[1]) for i in re.findall('(.+?)=(.+?)(,|$)', conditions)])
#  if not returns: returns='*'
#  return get_element(table,returns,wheres)
#
#
#
#def create_table(cursor, table_name, values):
#	exstr='create table %s (%s)' % ( table_name, ', '.join([ item[0]+' '+(item[1] if item[1] else 'text') for item in values.items() ]))
#	print(exstr)
#	cursor.execute(exstr)
#
#def add_element_to_table(cursor,table_name,values):
#	exstr='insert into %s values (?%s)' % (table_name, ',?'*(len(values)-1))
#	print(exstr, values)
#	cursor.execute(exstr, values)
#
#def print_table(cursor,table_name):
#	print(cursor.execute('select * from %s' % table_name).fetchall())
#
#def commit_changes(connection):
#	connection.commit()
#
#def open_connection_to_database(name):
#	if os.path.isfile(name):
#		os.rename(name,name+'.backup')
#	connection=sqlite3.connect(name)
#	cursor=connection.cursor()
#	return connection,cursor
#
#def close_connection_to_database(connection):
#	connection.close()
#
#class DatabaseGeneratorUI(cmd.Cmd):
#	'''User Interface for BTPP Database Generator'''
#	prompt='dg> '
#	intro='Database Generator for BTPP website\nRun this only when the database needs to be entirely regenerated\nFor a list of commands, try entering \'help\''
#	def do_greet(self, line=''):
#		print('Database Generator for BTPP website\n')
#		print('Run this only when the database needs to be entirely regenerated')
#
#	def do_EOF(self,line=''):
#		print('\nQuitting...')
#		return self.do_exit()
#	def do_exit(self,line=''):
#		return True
#	def postloop(self):
#		print()
#	def cmdloop(self):
#		try:
#			cmd.Cmd.cmdloop(self)
#		except KeyboardInterrupt as e:
#			self.do_EOF()
#
#DatabaseGeneratorUI().cmdloop()
#exit(0)

#connection,cursor=open_connection_to_database(database_name)
#create_table(cursor, 'pages',OrderedDict([('page_name','text'),('element_name','text'), ('element_value','text')]))
#add_element_to_table(cursor,'pages',['base', 'logo_text','Birmingham Trust for <br/> Psychoanalytic Psychotherapy'])
#add_element_to_table(cursor,'pages',['base', 'logo_image','nope'])
#add_element_to_table(cursor,'pages',['home', 'title','home'])
#
#create_table(cursor, 'menu',OrderedDict([('name','text'),('url','text'), ('content','text')]))
#add_element_to_table(cursor,'menu',['home','/btpp','home'])
#
#create_table(cursor, 'users',OrderedDict([('user_name','text'),('password','password')]))
#add_element_to_table(cursor,'users',['kevin','216cb14fe707daefb5c630e14d2c87b25922489457d176dac00dd32e32a9c3f48ef7c8682cff9d7d9a6c1759f622d9af262334b06f98e19f86622a26bb435dfb'])
#
#commit_changes(connection)
#close_connection_to_database(connection)
