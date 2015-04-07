import sqlite3

class Database:
	__cursor=None
	__connection=None
	def __find_table(self, table_name):
		self.__cursor.execute('.tables ?', table_name);
		return self.__cursor.fetchall()
	def __create_table(self, table_name, values):
		command='create table if not exists %s (%s)' % ( table_name, values)
		try:
			self.__cursor.execute(command)
		except:
			print('Bad command: {0}'.format(command))
			raise
		
	def __init__(self, name):
		self.__connection=sqlite3.connect(name)
		self.__cursor=self.__connection.cursor()
		self.__create_table('users','user_id,state')
		self.__create_table('interactions','required_state,state_change,messages')
		self.__create_table('commands','command,interaction_ids,required_state')
		self.__create_table('state','value_combination,description')
		self.__create_table('state_masks','state,description')
		self.__connection.commit()
	def find_state(self, user_id):
		self.__cursor.execute('select state from users where user_id=?', (user_id,))
		result=self.__cursor.fetchone()
		if not result:
			return None
		else:
			return result[0]
	def add_user(self, user_id):
		if not self.find_state(user_id):
			self.__cursor.execute('insert into users values (?,0)', (user_id,))
			self.__connection.commit()
	def change_state(self,user_id,change):
		state=self.find_state(user_id)
		if not state:
			raise Exception('changing state of user_id that cannot be found')
		for c in change.split(','):
			(index,value)=c.split('=')
			state[index]=value
		if not state:
			return '0'
		else:
			return state
	def update_state(self,user_id,new_state):
		self.__cursor.execute('update users set state=? where user_id=?', (state,user_id))	
		self.__connection.commit()
	def find_unhandled_commands(self):
		return self.__cursor.execute('select command from commands where interaction_ids="-1"').fetchall()
	def find_command(self,command):		
		return self.__cursor.execute('select interaction_ids from commands where command=?', (command,)).fetchall()
	def add_command(self,command):
		if not self.find_command(command):
			self.__cursor.execute('insert into commands values (?,"-1")',(command,))
			self.__connection.commit()


