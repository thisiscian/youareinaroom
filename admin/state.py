from admin.util import modify_in_temp_file

db=None

def __parse_index(cmd, index, unhandled):
	if not unhandled: 
		print('There are no unhandled commands to {command}'.format(command=cmd))
		return False
	elif index and not isinstance(index,int):
		print('Supplied \'INDEX\' argument is not an integer')
		return False
	elif index and len(unhandled) < index:
		print('Supplied \'INDEX\' argument is greater than the total number of unhandled commands'.format(index=index))
		return False
	return True

def add(command=None,state=None):
	command=' '.join(args)
	command,required_state=modify_in_temp_file(('command',command), ('required_state',''))	
	db.add_unhandled_command(command,required_state)

def show(index=None):
	unhandled=db.find_unhandled_commands() 
	if not __parse_index('show',index,unhandled): return False
	if index:
		print('Entry #{index}'.format(index=index))
		print('  command: {command}'.format(command=unhandled[index][1]))
	else:
		print('Listing all unhandled commands')
		for index in range(0,len(unhandled)):
			print('  Entry #{index}'.format(index=index))
			print('    command: {command}\n'.format(unhandled[index][1]))
	return True

def remove(index=None):	
	unhandled=db.find_unhandled_commands() 
	if not __parse_index('remove',index,unhandled): return False
	if not index:
		print('No \'INDEX\' argument supplied')
		return False
	else:
		print('Unhandled entry #{index} has been removed'.format(index=index))
		rowid=unhandled[index][0]
		db.remove_unhandled_command(rowid)	

