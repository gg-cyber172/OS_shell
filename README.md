# OS_shell
Name: Gergely Gellert 
MYSHELL	General User Guide						

Launching the Shell
You can launch the shell by 2 methods through the terminal command line. One involves giving it an extra argument when launching from Terminal (E.g. python3 myshell.py text.txt). This will open up the file provided in the terminal, read it and execute any commands found there. Not providing an extra arguement when launching the shell will make it ask the user for prompts.

Internal Help Document Commands
	Press the enter key to continue down the helpfile
	Press the q key to quit out of the helpfile
-------------------------------------------------------------------------------------------------------
Internal Commands
	cd - Usage- cd <directory>
	Description: Changes current working directory to directory specified. If no directory is specified then the current directory is reported. Invalid directory paths will be reported as errors. Also changes the PWD variable in the environment strings when the directory is changed.
	
	clr - Usage- clr
	Description: Clears the screen.
	
	dir - Usage- dir or dir <directory>
	Description: Lists contents or directory specified. If no directory is specified it'll list the contents of the current working directory. Invalid directory paths will be reported as errors.
	
	environ - Usage- environ
	Description: Provides a list of all current environment attributes.
	
	echo - Usage- echo <message>
	Description: Returns the string you input
	
	help - Usage- help
	Internal commands: q - Quits the manual
	Description: Displays this manual
	
	pause - Usage- pause
	Description: Pauses the shell until the enter key is pressed
	
	quit - Usage- quit
	Description: Quits the shell

Any other commands given will be interpreted as program invocation. (E.g. inputting python3 myshell.py will launch another instance of the shell within the shell)
-------------------------------------------------------------------------------------------------------
Input/Output redirection and Background processing

Input/Output redirection is simply redirecting the program to take input from the location you specified and forward it's output to the location you also specified. Current internal commands that support Output redirection are
	-dir
	-environ
	-echo
	-help
		  
	Input redirection - Usage- Input a < followed by a file name. (E.g. dir < input.txt)
	Description: This will change the input stream (place where it gets it's input from) of the command given to be the file given. Only works for external commands.
		  
	Output redirection - Usage- Input a > or >> followed by a file name (E.g. dir > output.txt or dir >> output.txt)
	Description: This will change the output stream (place where it forwards it's output to) of the command given to the specified file. If the file that is given doesn't exist it'll be created. The ">" symbol will truncate anything in the file when writing while the ">>" symbol will simply append the output to the bottom of the file.
		  
	Background processing - Usage- Input & at the end of your command line. (E.g echo hello &)
	Description: By putting an ampersand (&) at the end of your command it'll return you to the command line immediately and execute the program in the background. The only commands that don't support background execution are the help and pause commands since it doesn't make sense for them to run in the background since they require user input.
	

