#__author__ = rahul raj
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import unquote
from decouple import config
import re

#global variable and initialised to 0. represent the maximum value of id present in file_store.txt
max_id=0

class Serve(BaseHTTPRequestHandler):

	# GET method
	def do_GET(self):
		url=self.path
		global max_id
		try:
			if(self.check_for_URL(unquote(url))):
				qParams=parse.parse_qs(parse.urlsplit(url).query)
				file_=parse.urlsplit(url).path[1:]
				if(qParams['action'][0]=='create'):
					max_id=self.create(file_,qParams['string'][0],max_id)
				elif(qParams['action'][0]=='list'):
					self.list(file_)
				elif(qParams['action'][0]=='view'):
					self.view(file_,qParams['id'][0])
				elif(qParams['action'][0]=='delete'):
					self.delete(file_,qParams['id'][0])
				elif(qParams['action'][0]=='update'):
					if(int(qParams['id'][0])>max_id):
						max_id=self.create(file_,qParams['string'][0],max_id)
					else:
						self.update(file_,qParams['id'][0],qParams['string'][0])
				else:
					print("No!")
			else:
				raise NameError
		except:
			error="URL Not Found!"
			self.send_response(404)
			self.end_headers()
			self.wfile.write(bytes(error, 'utf-8'))

	#check for correct URL.
	def check_for_URL(self,path):
		# different regex pattern for different API
		regex=["/file_store\.txt\?action=list$",
				"/file_store\.txt\?action=create&string=[a-zA-Z0-9,.! ]+$",
				"/file_store\.txt\?action=update&id=[0-9]+&string=[a-zA-Z0-9,.! ]+$",
				"/file_store\.txt\?action=view&id=[0-9]+$",
				"/file_store\.txt\?action=delete&id=[0-9]+$"]
		for pattern in regex:
			if(re.match(pattern,path)):
				return True
		return False

	#For action create
	def create(self,file_name,s,idx):
		try:
			if(file_name=='file_store.txt'):
				with open(file_name,"a") as f:		
						# print(idx)
						text=str(idx+1)+":"
						text=text+s
						text=text+"\n"
						# print(text)
						f.write(text)
						self.send_response(200)
						self.end_headers()
						self.wfile.write(bytes("OK", 'utf-8'))
						return (idx+1)
			else:
				raise FileNotFoundError
		except:
				error="File not found!"
				self.send_response(404)
				self.end_headers()
				self.wfile.write(bytes(error, 'utf-8'))
				return idx

	#for action update
	def update(self,file_name,idx,string):
		try:
			if(file_name=='file_store.txt'):
				line_to_up=""
				file=""
				with open(file_name,'r') as f:
					self.send_response(200)
					self.end_headers()
					file=f.read()
					f.seek(0)
					line_to_up=""
					for line in f:
						# print(line.split(':')[-1])
						if(line.split(':')[0]==idx):
							line_to_up=line
				with open('file_store.txt','w') as f:
					for line in file.split('\n'):
						if(line!=line_to_up.split('\n')[0] and line!=""):
							f.write(line+'\n')
						elif(line!=""):
							string=":"+string
							string=string+"\n"
							line=str(idx)+string
							f.write(line)
				self.wfile.write(bytes("OK", 'utf-8'))
			else:
				raise FileNotFoundError
		except:
			error="File not found!"
			self.send_response(404)
			self.end_headers()
			self.wfile.write(bytes(error, 'utf-8'))
	
	#for action delete
	def delete(self,file_name,idx):
		try:
			if(file_name=='file_store.txt'):
				line_to_delete=""
				file=""
				with open(file_name,'r') as f:
					self.send_response(200)
					self.end_headers()
					file=f.read()
					f.seek(0)
					for line in f:
						if(line.split(':')[0]==str(idx)):
							line_to_delete=line
				with open('file_store.txt','w') as f:
					for line in file.split('\n'):
						# print("1",line)
						if(line!=line_to_delete.split('\n')[0] and line!=""):
							f.write(line+'\n')
						elif(line!=""):
							line=str(idx)+":\n"
							f.write(line)
				self.wfile.write(bytes("OK", 'utf-8'))
			else:
				raise FileNotFoundError
		except:
			error="File not found!"
			self.send_response(404)
			self.end_headers()
			self.wfile.write(bytes(error, 'utf-8'))

	#for action list
	def list(self,file_name):
		try:
			if(file_name=='file_store.txt'):
				with open(file_name,'r') as f:
					self.send_response(200)
					self.end_headers()
					for line in f:
						self.wfile.write(bytes(line, 'utf-8'))
			else:
				raise FileNotFoundError
		except:
			error="File not found!"
			self.send_response(404)
			self.end_headers()
			self.wfile.write(bytes(error, 'utf-8'))

	#for acrion view
	def view(self,file_name,idx):
		# print(idx)
		try:
			if(file_name=='file_store.txt'):
				flag=0
				with open(file_name,'r') as f:
					self.send_response(200)
					self.end_headers()
					line_to_view=""
					s=str(idx)+":"
					for line in f:
						if(line.split(':')[0]==idx and line.split('\n')[0]!=s):
							line_to_view=line.split('\n')[0]
							flag=1
					if(flag==1):
						self.wfile.write(bytes(line_to_view, 'utf-8'))
					else:
						line_to_view="No Data Found!"
						self.wfile.write(bytes(line_to_view, 'utf-8'))
			else:
				raise FileNotFoundError
		except:
				error="File not found!"
				self.send_response(404)
				self.end_headers()
				self.wfile.write(bytes(error, 'utf-8'))

#main 
httpd=HTTPServer((config("IP"),int(config("PORT"))),Serve)
print("Server Started Successfully!")
httpd.serve_forever()