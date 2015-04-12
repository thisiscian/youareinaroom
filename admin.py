#!/usr/bin/python3.4
import cmd
import database
import os

def intro_handler(header,message,hint):
	'''This is a wrapper to produce clean, centered intro text for the `cmd` class'''
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
		print('\x1b[2J\x1b[;H') ## this clears the terminal, and moves the cursor to the top left corner (equivalent to the `clear` command)
		unhandled_count=len(db.unhandled.parse('all') or [])
		self.intro=intro_handler('Welcome to the YouAreInARoom admin interface.',
														 'There {verb} {unhandled_count} unhandled command{s}'.format(s='s' if not unhandled_count == 1 else '', verb='are' if not unhandled_count == 1 else 'is', unhandled_count=unhandled_count),
														 'Enter \'help\' if you need help, or \'help COMMAND\' if you need more help with a command',
												    )
		super(GameUpdater,self).__init__()
		self.tables=['user','state','command','unhandled','interaction']
	def print_topics(self,header,cmds,cmdlen,maxcol):
		if header is not None:                                                                                                                                              
			if cmds:                                                                                                                                                        
					self.stdout.write('{header}\n'.format(header=header))                                                                                                                       
					if self.ruler:                                                                                                                                              
							self.stdout.write('{ruler}\n'.format(ruler=self.ruler*len(header)))                                                                                                 
					self.columnize(cmds, maxcol-1)                                                                                                                              
					self.stdout.write('\n')    	

	def do_EOF(self,line):
		print('')
		return True
	def do_exit(self,line):
		'''Exits the program'''
		return True 

	#########
	# informative functions start here
	#########
	
	### functions for tab-completion
	def complete_show(self,text,line,begin,end): return [expansion for expansion in self.tables if expansion.startswith(text)]
	def complete_add(self,text,line,begin,end): return [expansion for expansion in self.tables if expansion.startswith(text)]
	def complete_remove(self,text,line,begin,end): return [expansion for expansion in self.tables if expansion.startswith(text)]
	def complete_update(self,text,line,begin,end): return [expansion for expansion in self.tables if expansion.startswith(text)]
	def complete_info(self,text,line,begin,end): return [expansion for expansion in self.tables if expansion.startswith(text)]

	def do_show(self,line):
		'''Usage: show [unhandled]\n  unhandled [INDEX]: lists all unhandled commands, or the unhandled command that is described by the \'INDEX\' variable\n  state [NAME]: shows all states, or the state that is described by \'NAME\' '''
		if not line:
			print(self.do_show.__doc__)
		else:
			output=db.parse('show '+line)
			if not output:
				print('No entries found')
			else:
				for line in output:
					print(line)

	def do_show_unhandled(self,line):
		'''unhandled help hint'''
		if not line: print(self.do_show.__doc__)
		else:
			output=db.unhandled.parse(line.split(' '))	
			if not output: print('No entries found')
			else: 
				for line in output: print(line)
	def do_add(self,line):
		'''Usage: add [user,state,unhandled] VALUES'''
		if not line:
			print(self.do_show.__doc__)
		else:
			output=db.parse('add '+line)
			if not output:
				print('Error: must define values')
			else:
				print('Added value')


	def do_remove(self,line):
		'''Usage: remove [unhandled]\n  unhandled INDEX: removes the unhandled command indicated by the \'INDEX\' variable'''
		if not line:
			print(self.do_show.__doc__)
		else:
			output=db.parse('remove '+line)
			if not output:
				print('Error: something failed with your command')
			else:
				print('Removed entry')

if __name__=='__main__':
	import sys, os
	if len(sys.argv) != 2: 
		print('\x1b[31;1mError\x1b[0m: exactly one argument is required')
		print('\x1b[32;1mUsage\x1b[0m: {arg0} DATABASE'.format(arg0=sys.argv[0]))
		print('       where DATABASE is the path to an existing database,')
		print('       or the name of a new story to be created.')
		exit(1)
	database_path=sys.argv[1]
	if not os.path.isfile(database_path):
		print('Creating new database...')
	db=database.Database(database_path)
	try:
		GameUpdater(db).cmdloop()
	except KeyboardInterrupt:
		print('\nExiting...')
		exit(1)
	except Exception as e:
		print(e)
		print('')
		exit(1)
