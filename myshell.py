#Name: Gergely Gellert 
#Student Number: 17379616
import os, cmd, sys, threading, multiprocessing, shell_commands
lock=threading.Lock()
shell= os.getcwd()+"/myshell"
def main():
	prompt= shell_commands.Project_nofile()	#Creates an instance of the shell
	if len(sys.argv)==1:#Check if there's a batchfile, if there isn't launch the terminal in user input mode
		prompt.prompt=	os.environ["PWD"]+"/>"#Set the prompt to be the current working directory
		prompt.cmdloop("Starting shell")#Start the shell loop with welcome message
	else:
		with open(sys.argv[1],"r") as f_in:#If there is a batchfile open it 
			argv_file=f_in.readlines()#Read all the lines in the file into a list
		for line in argv_file:#Go through each line
			prompt.onecmd(line.strip())#Treat each line as a one user input command in the shell
		print("Finished, quitting the shell")	#Finish with an exit message

if __name__=="__main__":
	main()
