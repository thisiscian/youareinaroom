#!/usr/bin/python3.4
import cmd
import database
import admin.unhandled

def intro_handler(header,message,hint):
	'''
	This is a wrapper to produce clean, centered intro text for the `cmd` class
	'''
	import os
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
		admin.unhandled.db=self.db
		self.unhandled=self.db.find_unhandled_commands()
		print('\x1b[2J\x1b[;H') ## this clears the terminal, and moves the cursor to the top left corner (equivalent to the `clear` command)
		self.intro=intro_handler('Welcome to the YouAreInARoom admin interface.',
														 'There {verb} {unhandled_count} unhandled command{s}'.format(s='s' if not len(self.unhandled) == 1 else '', verb='are' if not len(self.unhandled) == 1 else 'is', unhandled_count=len(self.unhandled)),
														 'Enter \'help\' if you need help, or \'help COMMAND\' if you need more help with a command',
												    )
		super(GameUpdater,self).__init__()
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
	def complete_show(self,text,line,begin,end): return [expansion for expansion in ['unhandled'] if expansion.startswith(text)]
	def do_show(self,line):
		'''Usage: show [unhandled]\n  unhandled [INDEX]: lists all unhandled commands, or the unhandled command that is described by the \'INDEX\' variable\n  state [NAME]: shows all states, or the state that is described by \'NAME\' '''
		command,*args=line.split(' ')
		if command == 'unhandled': admin.unhandled.show(args[0] if args else None)
		elif command ==  'state':  state(self.db, 'show', args)
		else: print(self.do_show.__doc__)

	def complete_add(self,text,line,begin,end): return [expansion for expansion in ['unhandled'] if expansion.startswith(text)]
	def do_add(self,line):
		'''Usage: add [unhandled]\n  unhandled: opens a file in vim, that can be edited to add an unhandled command'''
		command,*args=line.split(' ')
		if command == 'unhandled': admin.unhandled.add(' '.join(args))
		else: print(self.do_add.__doc__)

	def complete_remove(self,text,line,begin,end): return [expansion for expansion in ['unhandled'] if expansion.startswith(text)]
	def do_remove(self,line):
		'''Usage: remove [unhandled]\n  unhandled INDEX: removes the unhandled command indicated by the \'INDEX\' variable'''
		command,*args=line.split(' ')
		if command == 'unhandled': admin.unhandled.remove(int(args[0]) if args else None)
		else: print(self.do_remove.__doc__)

#	def complete_handle(self,text,line,begin,end): return [expansion for expansion in [] if expansion.startswith(text)]
#	def do_handle(self,line):
#		try:
#			index=int(line.split(' ')[0])
#		except:
#			print('You should fuck off without an argument')
#			return
#		item=self.unhandled[index]
#		print(item)
#		with tempfile.NamedTemporaryFile() as fh:
#			fh.write(bytes('### command ###\n{0}\n'.format(item[0]),'utf-8'))
#			fh.write(b'### state ###\n')
#			fh.write(b'### response ###\n')
#			fh.write(b'### new state ###\n')
#			fh.flush()
#			subprocess.call(['/usr/bin/vim',fh.name])		

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
