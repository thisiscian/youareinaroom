#!/usr/bin/python3.4
import cmd
import readline
import database
import os 
import tempfile
import subprocess

def intro_handler(header,message,hint):
	width=int(os.popen('stty size','r').read().split()[1])
	header_pre=' '*int(width/2-2-len(header)/2)
	header_post=' '*int(width/2-2-len(header)/2+0.5)
	messages_pre=int(width/2-2-len(message)/2)
	messages_post=int(width/2-2-len(message)/2+0.5)
	output='\n'
	output+=' ╔'+'─'*(width-4)+'╗ \n'
	output+=' │'+header_pre+'\x1b[1m'+header+'\x1b[0m'+header_post+'│ \n'
	output+=' ╚'+'─'*(width-4)+'╝ \n'
	output+=' '*(messages_pre+1)+'┌'+'─'*len(message)+'┐\n'
	output+='  '+'═'*(messages_pre-1)+'╡'+message+'╞'+'═'*(messages_post-1)+'\n'
	output+=' '*(messages_pre+1)+'└'+'─'*len(message)+'┘\n'
	output+='\n'+hint
	return output

class GameUpdater(cmd.Cmd):
	prompt='\x1b[1mroom> \x1b[0m'
	undoc_header=None
	doc_header='\x1b[1mAvailable Commands\x1b[0m'
	ruler='─'
	def __init__(self, database):
		self.db=database
		self.unhandled=self.db.find_unhandled_commands()
		print('\x1b[2J\x1b[;H')
		self.intro=intro_handler('Welcome to the YouAreInARoom admin interface.',
												'There are {unhandled_count} unhandled commands'.format(unhandled_count=len(self.unhandled)),
												'Enter \'help\' if you need help'
												)
		super(GameUpdater,self).__init__()
	def print_topics(self,header,cmds,cmdlen,maxcol):
		if header is not None:                                                                                                                                              
			if cmds:                                                                                                                                                        
					self.stdout.write("%s\n"%str(header))                                                                                                                       
					if self.ruler:                                                                                                                                              
							self.stdout.write("%s\n"%str(self.ruler * len(header)))                                                                                                 
					self.columnize(cmds, maxcol-1)                                                                                                                              
					self.stdout.write("\n")    	

	def do_EOF(self,line):
		print('')
		return True
	def do_exit(self,line):
		"""Exits the program"""
		return True 

	def do_command(self,line):
		"""Usage: command [add|unhandled]
    add: adds a command to the story
    unhandled: lists the unhandled commands 
		"""
		args=line.split(' ')
		if len(args) is 0:
			return False
		subcmd=args[0]
		subline=''
		if len(args) > 2:
			subline=' '.join(args[1:])
		if subcmd == 'add':
			self.command_add(subline)
		elif subcmd == 'unhandled':
			self.command_unhandled(subline)
		
	def complete_command(self,text,line,begin,end):
		return [expansion for expansion in ['add', 'unhandled'] if expansion.startswith(text)]
		
	def do_show(self,line):
		command=line.split(' ')[0]
		newline=line.split(' ')[1:]
		if command == 'unhandled':
			self.command_unhandled(' '.join(newline))

	def command_unhandled(self,line):
		if not line:
			print('Listing unhandled commands...')
			self.unhandled=self.db.find_unhandled_commands()
			if len(self.unhandled) is 0:
				print('  No unhandled commands found')
			i=0
			for command in self.unhandled:
				print(str(i)+':'+command[0])
				i+=1
		else:
			args=line.split(' ')

	def command_add(self,line):
		command=input('Enter command: ')
		is_okay=None
		while is_okay not in ('y','n'):
			is_okay=input('You entered \"%s\"\nIs this okay? (y/n):\n' % command).lower()
		pass	

	def do_handle(self,line):
		try:
			index=int(line.split(' ')[0])
		except:
			print('You should fuck off without an argument')
			return
		item=self.unhandled[index]
		print(item)
		with tempfile.NamedTemporaryFile() as fh:
			fh.write(bytes('### command ###\n{0}\n'.format(item[0]),'utf-8'))
			fh.write(b'### state ###\n')
			fh.write(b'### response ###\n')
			fh.write(b'### new state ###\n')
			fh.flush()
			subprocess.call(['/usr/bin/vim',fh.name])		

if __name__=='__main__':
	import sys
	import os
	if len(sys.argv) < 2: 
		print("\x1b[31;1mError\x1b[0m: you should add a database, you fool")
		exit(1)
	database_path=sys.argv[1]
	if not os.path.isfile(database_path):
		print('Creating database...')
	db=database.Database(database_path)
	try:
		GameUpdater(db).cmdloop()
	except Exception as e:
		print(e)
		print('')
		exit(1)
