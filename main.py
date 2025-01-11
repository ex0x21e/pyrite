import sys
import shutil
import subprocess
import signal
import os
import readline

#TODO: ADD too much arguments warning. REFACT CODE(modules functions and comments). HELP. TAB AUTOCOMPLETE. PIPING. GREP . CHEK INPUT BUFFER AFTER CTRL-C
#Support for background processes (&)

def sig_int_handle(signal_num, frame):
     print("ctrl-c pressed")
     sys.stdout.write("$ ") #chek stream after ctr-c
     sys.stdout.flush() # обновить приглашение $ в терминале сразу после очистки буфера ввода


#registarate sig_int_handle
signal.signal(signal.SIGINT, sig_int_handle)

def main(): 
    #buildins commands
    builtins = {
        "echo": "echo is a shell builtin",
        "exit": "exit is a shell builtin",
        "type": "type is a shell builtin",
        "pwd":  "pwd is a shell builtin"
    }

    while True:
        try:
            sys.stdout.write("$ ")
            if command := input():
                match command.split():
                    case ["echo", *args]:
                        print(" ".join([arg.strip("'").strip('"') for arg in args]))
                        
                    case ["exit", status]:
                            print(f"exiting with status {status}")
                            sys.exit(int(status))
                    case ["exit"]:
                        sys.exit(0)

                    case ["type", cmd]:
                        path = shutil.which(cmd)
                        
                        if cmd in builtins:
                                print(f"{builtins[cmd]}")
                        elif path:
                            print(f"{cmd} is {path}")
                        else:
                            print(f'{cmd}: not found')
                            
                    case ["cd", dir]: 
                        try:
                            if dir == "~":
                                os.chdir(os.path.expanduser("~"))
                            else:
                                os.chdir(dir)

                        except FileNotFoundError:
                                print(f"cd: {dir}: No such file or directory")

                    case ["cd"]:
                        os.chdir(os.path.expanduser("~"))
                        
                    case ["pwd"]:
                            print(os.getcwd())
                

                    #external commands
                    case [cmd, *args]:
                        path = shutil.which(cmd)
                        if path:
                            try:
                                subprocess.run([cmd] + args)
                            except subprocess.CalledProcessError as e: #print falied code
                                print(f"error called external command {cmd}: returned code {e.returncode}")
                        else:
                            print(f"external command {command}: not found")
                    case _:
                        print(f"{command}: not found")
                
        except EOFError: #ctrl-d
            print("Exiting...")
            sys.exit()
            

if __name__ == "__main__":
    main()
