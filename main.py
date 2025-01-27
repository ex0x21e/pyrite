import sys
import shutil
import subprocess
import signal
import os
import readline

#TODO: REFACT CODE(modules functions and comments). HELP. TAB AUTOCOMPLETE. PIPING. GREP. CHEK INPUT BUFFER AFTER CTRL-C
#Support for background processes (&)

#buildins
def echo_handler(args):
    print(" ".join([arg.strip("'").strip('"')  for arg in args]))

def exit_handler(args):
    try:
        status = abs(int(args[0])) if args else 0
        print(f"exiting with status {status}")
        sys.exit(status) 
    except ValueError:
        print(f"exiting with status {status}")
        sys.exit(-1)

def cd_handler(args):
    if len(args) > 1:
        print("cd: too many arguments", file=sys.stderr)
    else:
        target_dir = args[0] if args else "~"
    try:
        os.chdir(os.path.expanduser(target_dir)) # <-- here!
    except FileNotFoundError:
        print("cd: No such file or directory", file=sys.stderr)


def pwd_handler(args=None):
    print(os.getcwd())

def type_handler(args):
    if len(args) > 1:
        print("type: too many arguments", file=sys.stderr)
        return
    cmd = args[0]
    if cmd in builtins_fn:
        print(f"{cmd} is a shall buildin")
    else:
        path = shutil.which(cmd)
        if path:
            print(f"{cmd} is {path}")
        else:
            print(f"{cmd} not found")
#external

def external_commands_handler(cmd, args):
    path = shutil.which(cmd)
    if path:
        try:
            subprocess.run([cmd] + args)
        except subprocess.CalledProcessError as e:
            print(f"error call command {e.returncode}")
    else:
        print(f"{cmd} not found")

def sig_int_handle(signal_num, frame):
     print("ctrl-c pressed")
     sys.stdout.write("$ ") #ctr-c
     sys.stdout.flush() # обновить приглашение $ в терминале сразу после очистки буфера ввода


#registarate sig_int_handle
signal.signal(signal.SIGINT, sig_int_handle)

builtins_fn = {
    "echo": echo_handler,
    "type": type_handler,
    "exit": exit_handler,
    "pwd" : pwd_handler,
    "cd"  : cd_handler
}

def buildins_handle(cmd, args):
    if cmd in builtins_fn:
        builtins_fn[cmd](args)
    else:
        print(f"{cmd} comand not found")

def parse_and_exec(command, buildins):
    tokens = command.split()
    cmd, args = tokens[0], tokens[1:]
    if cmd in buildins:
        buildins_handle(cmd, args)
    else:
        external_commands_handler(cmd, args)


def main(): 
    #buildins commands
    builtins = {
        "echo": "echo is a shell builtin",
        "exit": "exit is a shell builtin",
        "type": "type is a shell builtin",
        "pwd":  "pwd is a shell builtin",
        "cd":   "cd is a shell builtin"
    }

    while True:
        try:
            sys.stdout.write(f"pyrite:{os.getcwd()}$ ")
            if command := input():
                parse_and_exec(command, builtins)
                
        except EOFError: #ctrl-d
            print("Exiting...")
            sys.exit()
            
if __name__ == "__main__":
    main()
