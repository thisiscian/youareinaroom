import tempfile
import subprocess 
import re

def modify_in_temp_file(*headers):
	with tempfile.NamedTemporaryFile() as fh:
		for key,value in headers:
			fh.write(bytes('### {key} ###\n{value}\n### /{key} ###\n'.format(key=key,value=value),'utf-8'))
		fh.flush()
		subprocess.call(['/usr/bin/vim',fh.name])
		fh.seek(0)
		contents=fh.read().decode('utf-8')
		output=[]
		for key,value in headers:
			output.append(re.findall('### {key} ###\n(.*?)\n### /{key} ###\n'.format(key=key),contents)[0])
		return output


