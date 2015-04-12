import sqlite3
import re

class Table:
	def __init__(self, cursor, connection, name, columns):
		self.cursor=cursor
		self.connection=connection
		self.name=name
		self.columns=columns
		self.cursor.execute('create table if not exists {name} ({columns})'.format(name=name, columns=','.join(columns)))
	
	def add(self, values):
		'''adds the values contained in list to the table'''
		if not isinstance(values,tuple) and not isinstance(values,list):
			raise Exception('Expected \'values\' variable to be a list')
		elif not len(values) == len(self.columns):
			raise Exception('Adding incorrect number of values to table \'{name}\''.format(name=self.name))
		vmarks=','.join(['?']*len(values))
		self.cursor.execute('insert into {name} values ({vmarks})'.format(name=self.name,vmarks=vmarks),values)
		self.connection.commit()
		return True

	def remove(self, rowid):
		'''removes the entry uniquely identified by \'rowid\' from the table'''
		self.cursor.execute('delete from {name} where rowid=?'.format(name=self.name),str(rowid))
		self.connection.commit()
		return True

	def show(self, wheres):
		'''shows entries that are filtered by the \'where\' dictionary, e.g. {\'rowid\':0} will show the first entry'''
		if not isinstance(wheres,dict):
			raise Exception('Expected \'wheres\' variable to be a dictionary')
		else:
			keys=wheres.keys()
			values=[ wheres[key] for key in keys ]
			wmarks=','.join([ str(key)+'=?' for key in keys])
			self.cursor.execute('select rowid,* from {name} where {wmarks}'.format(name=self.name,wmarks=wmarks),values)
		output=self.cursor.fetchall()	
		return output

	def update(self, rowid, values):
		'''updates the entry uniquely identified by \'rowid\' integer with the data stored in the \'values\' list'''
		vmarks=','.join(['?']*len(values))
		self.cursor.execute('update {name} set {vmarks} where rowid=?'.format(name=self.name,vmarks=vmarks),values+(rowid))
		self.connection.commit()
		return True

	def info(self):
		pass

	def parse(self,command,*args):
		if command == 'add':
			print(args)
			return self.add(args)
		elif command == 'remove':
			return self.remove(args[0])
		elif command == 'show':
			if not args or args[0] == 'all':
				wheres={1:1}
			else:
				wheres=dict(re.findall('(?:(\w+)=(\w+))',','.join(args)))
			return self.show(wheres)
		elif command == 'update':
			return self.update(args[0],*args[1:])

class Database:
	def __init__(self,name):
		self.connection=sqlite3.connect(name)
		self.cursor=self.connection.cursor()
	
		setattr(self,'user', Table(self.cursor,self.connection,'user',['twitter_id','current_state']))
		setattr(self,'interaction', Table(self.cursor,self.connection,'interaction',['required_state','state_change','messages']))
		setattr(self,'unhandled', Table(self.cursor,self.connection,'unhandled',['message','state_when_sent']))
		setattr(self,'command', Table(self.cursor,self.connection,'command',['message','required_state','valid_interactions']))
		setattr(self,'state', Table(self.cursor,self.connection,'state',['description','valid_values']))

	def __create_table(self, name, values):
		setattr(self, name, Table(self.cursor, self.connection, name, values))
		
	def parse(self, line):
		command, table, *args=line.split(' ')
		table=re.sub('s$','',table)
		table_object=getattr(self, table)
		return getattr(table_object,'parse')(command,*args)

	def translate_state_to_words(self,state):
		output={}
		for i in range(0,int(len(state)/2)):
			index=int(state[2*i:2*i+2],16)
			entry=self.state.show({'rowid':i+1})[0]
			key=entry[1]
			values=entry[2].split(',')
			if index > len(values):
				raise Exception('Given value index for \'{key}\' is outside the range of values found'.format(key=str(key)))
			output[key]=values[index]
		return output	
	
	def translate_words_to_state(self,words):
		string=''
		entries=self.state.parse('show','all')
		for entry in entries:
			if entry[1] in words:
				value=words[entry[1]]
				values=entry[2].split(',')	
				if value not in values:
					raise Exception('Given value \'{value}\' cannot be found for state \'{state}\''.format(state=entry[1],value=value))
				hx=hex(values.index(value))[2:]
				padded_hex=hx.zfill(2)
				string+=padded_hex
			else:
				string+='00'
		return string
