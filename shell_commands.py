#Name: Gergely Gellert 
#Student Number: 17379616
import os, cmd, sys, threading, multiprocessing,subprocess
lock=threading.Lock()
shell= os.getcwd()+"/myshell"   #Path to where shell is originally
help_file=os.getcwd()+"/readme" #Hardwired path to the helpfile
output_set={">":"w",">>":"a","<":"r"} #Set used later to identify how I should open files
class Project_nofile(cmd.Cmd):
	
	def do_clr(self,args): #Command that clears the screen
		"""Clears the screen.\nUsage: clr"""
		if len(args): #Checks if the command had any extra arguements
			if  args[-1].strip()=="&": #If it's an ampersand sign run this command in the background as a child process
				self.background(self.do_clr,args[:-1].strip())#If so run this command in the background minus the ampersand sign in the arguements
			else: #Any other arguements for this command means it wasn't called correctly so it displays an error message
				print("Invalid invocation of clr, please see the help function for correct use")
		else:#If there's no extra arguements it clears the screen by printing this string
			print ("\033[2J\033[H", end="")
	def do_dir(self,args):#Command to list files in a directory
		"""Lists files in directory given, will display a list of files in current directory if none is given.\nUsage: dir <directory>"""
		try:
			stdin,stdout,input_loc,output_loc=self.filter(args)#Checks the arguement string for any input/output redirections and if so extracts them from the arguements
			if args and args[-1].strip()=="&":#Once again checks if the ampersand sign is present, if so run the command in the background as a child process
				self.background(self.do_dir,args[:-1].strip())
			elif stdout:#If there is an output redirection do this instead
				if (args.split()[:output_loc]):#Since you can invoke dir 2 different ways this checks if there's a directory supplied
					self.writing(self.list_files("".join(args.split()[:output_loc])), stdout, args.split()[output_loc])#If so go to the writing function with the directory supplied
				else:#Else go to the writing function with the current directory
					self.writing(self.list_files(os.curdir),stdout, args.split()[output_loc])
			else:
				if args: #If there's no output redirection and there's a directory given list the files in that directory
					print(self.list_files(args))
				else:#Else list the files in the current directory
					print(self.list_files(os.curdir))
					
		except FileNotFoundError:#If a directory couldn't be found it displays the corresponding error message
			mes="Error directory \""+args+"\" not found"
			if stdout:#If there was output redirection instead print the error message there	
				self.writing(mes, stdout,args.split()[output_loc])
			else:#Else print it on screen
				print(mes)
	def do_echo(self,args):#Command to display a message
		"""Displays message inputted.\nUsage: echo <message>"""
		if (len(args)):#Check if there's any message to be displayed, if there isn't don't do anything
			if args[-1].strip()=="&":#Checks for ampersand sign to see if it should run this command in the background as a child process or not
				self.background(self.do_echo,args[:-1].strip())
			else:
				stdin,stdout,input_loc,output_loc=self.filter(args)#Filters out the input and output files 
				if stdout:#If there is an output redirection write to file instead of screen
					self.writing(" ".join(args.split()[:output_loc]),stdout,args.split()[output_loc])#Call the write to file function with the output
				else:
					print(" ".join(f for f in args.split("") if len(f)))#Print out the message while eliminating any extra white spaces and tabs

	def do_pause(self,args):#Function that pauses all of the terminal's actions till the enter key is pressed
		"""Pauses the program until the Enter key is pressed.\nUsage: pause"""
		if args:#Checks if there's any extra arguements given
			if args[-1].strip()=="&":#If there's an ampersand sign, don't run it in the background since it requires user input, no point running it in the background
				print("Invalid invocation of pause, pause doesn't support background initialisation")
			else:#Any other arguements is invalid so error message is displayed
				print("Invalid invocation of pause, please see the help function for correct use")
		else:
			lock.acquire()#To completely pause the terminal we acquire locks to ensure nothing is run or written to files
			i=input()
			lock.release()

	def do_cd(self,args):#Command to change the current working directory
		"""Changes the current directory.\nUsage: cd <directory>"""
		if (len(args)):#If there's arguements present then try change the directory to the arguement present
					try:
						if args[-1].strip()=="&":#Again if Ampersand sign is present then run it in the background as a child process
							self.background(self.do_cd,args[:-1].strip())
						else:
							os.chdir(args)#Changes the current working directory to the directory given
							os.environ["PWD"]=os.getcwd()#Update the PWD dictonary entry in the environment strings to the new directory
							self.prompt=os.environ["PWD"]+"/>"#Update the prompt to the new working directory
					except (FileNotFoundError):#If the directory isn't present report this error
						print("Error no \"",args,"\" directory found, please try again")
		else:#If no directory is present then report the current directory
			print("Your current directory is ",os.getcwd()+"/")
	
	def do_environ(self,args):#Command to list all environment strings
		"""Lists all the environment variables\nUsage: environ"""
		results=""
		for s in os.environ:#Creates a string with all the keys and values from the list of dictionaries in os.environ
			results+="Key= "+s+" File= "+os.environ[s]+"\n"
		if args:
			if args[-1].strip()=="&":#Run in background as a child process if ampersand symbol is present
				self.background(self.do_environ,args[:-1].strip())
			else:
				stdin,stdout,input_loc,output_loc=self.filter(args)#Filter the arguements to check for any I/O redirection
				if stdout:#If there is output redirection, redirect the output to the file
					self.writing(results.rstrip(), stdout,args.split()[output_loc])#Call writing function to write to the file along with what type of writing it should do
		else:#Else just display the results to the screen
					print(results.rstrip())
					
	def do_help(self,args):#Help function 
			lines=self.open_file_read(help_file)#Read the help manual into a variable
			if args:#If there's any extra arguements filter them to see what to do
				stdin,stdout,input_loc,output_loc=self.filter(args)
				if args[-1]=="&":#If & is present, display an error message since it requires user input
					print("Invalid invocation of help, help doesn't support background initialisation")
				elif stdout:#If there is output redirection do this instead
					s_fin=""
					for s in lines:
							s_fin+=s#Create a string of the help file to output to a file
					self.writing(s_fin,stdout,args.split()[output_loc])#Write help file to file
				else:#Any other arguements is invalid so display an error
					mess="Invalid invocation of pause, correct use of help function is \"help > <outputfile>\""
					if stdout:
					 	self.writing(mess,stdout,args.split()[output_loc])
					else:
						print(mess)
			else:#Create the help file environment
				j,s=0,""
				while s!="q":#Quit the manual if q is inputted
					try:
						for i in range(j,j+20):	#Print 20 lines of the manual
							print(lines[i].strip())
						j+=20
						s=input()#Wait for next input after printing 20 lines of the manual
					except IndexError:#If it reaches the end of the file return to normal shell
						return
								
	def default(self,args):#Command to execute any commands that are not internal commands. It supports input and output redirection since I finished the project before the specs were changed and it's more effort to modify and remove the input redirection so it's staying in there
		try:
			if len(args):#If there's any extra arguements check for &, I/O redirection etc
					if args[-1].strip()=="&":#If & is present run this program in the background in a child process
						self.background(self.default,args[:-1].strip())
					else:
						stdin,stdout,input_loc,output_loc=self.filter(args)
						if stdin or stdout:#If there's either input or output redirection 
								if stdin and stdout:#If there's both input and output redirection 
									subprocess.Popen(args.split()[:input_loc],stdin=self.open_file(stdin, args.split()[input_loc]),stdout=self.open_file(stdout, args.split()[output_loc]))#This uses the subprocess library with the Popen function. 
									#The Popen function runs external commands while being able to give it arguements, edit it's input and outputfile stream while also forking and creating a child process to run the program in. 
								elif stdin and not(stdout):#If there's only an input redirection then I only edit the input file stream
									p=subprocess.Popen(args.split()[:input_loc],stdin=self.open_file(stdin, args.split()[input_loc]))
									print(p.communicate()[0].decode("utf-8"))#Because there's no output file stream I have to manual communicate with the process and decode it's output
								else:#If there's only output redirection then I only edit the output file stream
									p=subprocess.Popen(args.split()[:output_loc],stdout=self.open_file(stdout, args.split()[output_loc]))						
						else:#If there's no output or input redirection at all then just run the external program as normal
								p=multiprocessing.Process(target=subprocess.call,args=(args.split(),))	
								p.start()
								p.join()
						
		except (FileNotFoundError):#If the external command isn't found then print these errors. 
			print("Not a command")
		except AttributeError:
			print("Not a command")
		
	def do_quit(self,args):#Command to quit the shell
		"""Quits the program.\nUsage: quit"""
		print("Quitting the shell")#End message
		raise SystemExit#Quits the system

	def emptyline(self):#When no command is inputted the shell does nothing
		pass
			
	def writing(self,args,output,w_type):#Function to write to files
		lock.acquire()#Acquires lock to ensure no other program can interupt it
		with open(output,output_set[w_type]) as f_out:#Opens file with appropriate type of output, write for > and append for >> 
			f_out.write(args)#Writes output into file
		f_out.close()#Closes file
		lock.release()#Releases the lock
		
	def list_files(self,dirc):	#Subfunction of the dir command to list files in a directory
		s,files="",os.listdir(dirc)#Gets a list of files in a directory
		for f in files:
			s+=f+"\n"	#Creates a string of all files in a directory and puts it in a variable
		return s.rstrip()#Returns the String

	def open_file(self,input_f,f_type):#Function to return a file reading iterator
		f=open(input_f,output_set[f_type])#Opens the file in the appropriate viewing setting
		return f#returns the itterator
	
	def open_file_read(self, input_f):#Subfunction to open a file and read all it's lines into a variable
		with open(input_f,"r") as f_in:#Opens the file as read
			lines=f_in.readlines()		#Fetches all the lines of the file
		return lines#Returns the lines
	def filter(self,args):#Function to check if there's any I/O redirection in a command's argument
		i,input_f,output_f,input_loc,output_loc=1,"","",0,0#i is set to 1 since the file is after the redirection symbol
		for s in args.split():#Scans through the arguements
			if s=="<":#If it hits the input symbol record the location of it and the file name after the symbol
				input_f=args.split()[i]
				input_loc=i-1
			if s==">" or s==">>":#If it hits either output symbol record the location of it and the file of it after
				output_f=args.split()[i]
				output_loc=i-1
			i+=1
		return input_f,output_f,input_loc,output_loc#Return all the information gathered
			
	def background(self,command,args):#Function to run internal commands in the background by spawning a child process 
		multiprocessing.Process(target=command, args=(args,)).start()#Launches a child process with the target being the internal command it came from
