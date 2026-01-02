import os
import glob
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

SANDBOX = os.path.expanduser("~/easycmd-sandbox")
os.makedirs(SANDBOX, exist_ok=True)
os.chdir(SANDBOX)

BEGINNER_HELP = """
Beginner Commands:
cd <folder>        - Change directory
dir                - List files and folders
mkdir <folder>     - Create a new folder
rmdir <folder>     - Remove an empty folder
type <file>        - Display file contents
del <file|*.ext>   - Delete a file
copy <source> <destination> - Copy files
move <source> <destination> - Move files
version            - Show Windows version
showdate           - Show current system date
sysinfo            - Show system info
ping <hostname>    - Ping a host
ipconfig           - Show IP addresses
compare <file1> <file2> - Compare files
notepad <file>     - Open file in Notepad
walkthrough        - Beginner walkthrough
walkthrough2       - Advanced beginner Windows commands
walkthrough3       - Batch files workshop
help               - Show this help
exit               - Exit the sandbox
"""

# ------------------------------
# Walkthrough Steps
# ------------------------------

WALKTHROUGH1 = [
    {"message": "Welcome to the first walkthrough! First, list files in the current directory using dir or ls.",
     "expected": ["dir", "ls"], "onsuccess": "Great! You see the files and folders."},

    {"message": "Create a folder named practice using mkdir.\nHint : mkdir <foldername>",
     "expected": ["mkdir practice"], "onsuccess": "Practice folder created!"},

    {"message": "Change into the practice directory using cd.\nHint : cd <foldername>",
     "expected": ["cd practice"], "onsuccess": "You are now inside the practice folder."},

    {"message": "Create a file named notes.txt using notepad.\nHint : notepad <filename>",
     "expected": ["notepad notes.txt"], "onsuccess": "File created."},

    {"message": "List files again to confirm.",
     "expected": ["dir", "ls"], "onsuccess": "Walkthrough complete!"}
]

WALKTHROUGH2 = [
    {"message": "Let's check the Windows version using version command.",
     "expected": ["version"], "onsuccess": "Windows version displayed!"},

    {"message": "Check the IP addresses of your device using ipconfig.",
     "expected": ["ipconfig"], "onsuccess": "IP addresses shown!"},

    {"message": "Ping google.com to check connectivity.\nHint : ping <target>",
     "expected": ["ping google.com", "ping google"], "onsuccess": "Ping successful!"},

    {"message": "Create a folder named HCK on the desktop using mkdir HCK.",
     "expected": ["mkdir hck"], "onsuccess": "Folder HCK created!"},

    {"message": "Create a file new.txt inside HCK with content 'Herald College Kathmandu'.",
     "expected": ["notepad hck/new.txt"], "onsuccess": "new.txt created!"},

    {"message": "Delete the new.txt file inside HCK.\nHint : del <filename>",
     "expected": ["del hck/new.txt"], "onsuccess": "File deleted!"},

    {"message": "Remove the folder HCK.\nHint : rmdir <foldername>\nKeep in mind, a folder must be empty is we want to remove using only the rmdir command.",
     "expected": ["rmdir hck"], "onsuccess": "Folder removed!"}
]

WALKTHROUGH3 = [
    {"message": "Let's create a batch file hello.bat using notepad.",
     "expected": ["notepad hello.bat"], "onsuccess": "Batch file created!"},

    {"message": "Write echo Hello World in the batch file and save it.",
     "expected": ["edit hello.bat", "notepad hello.bat"], "onsuccess": "Hello World added to batch file."},

    {"message": "Run the batch file using hello.bat",
    "expected": ["hello.bat", "run hello.bat"], "onsuccess": "Batch file executed!\nCongratulations! You have completed the walkthrough for batch file creation."}
]


def inside_sandbox(path):
    return os.path.commonpath([SANDBOX, os.path.abspath(path)]) == SANDBOX

def format_prompt():
    cwd = os.getcwd()
    folder_name = os.path.basename(cwd)
    return f"\n{Fore.GREEN}{folder_name}{Style.RESET_ALL}> "

def execute_command(cmdline):
    parts = cmdline.split()
    if not parts:
        return

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd == "cd":
        if not args:
            print("Usage: cd <folder>")
            return
        target = args[0]
        new_path = os.path.abspath(os.path.join(os.getcwd(), target))

        if not os.path.exists(new_path):
            print(Fore.RED + f"❌ Path not found: {target}")
            return

        if not os.path.isdir(new_path):
            print(Fore.RED + f"❌ Not a directory: {target}")
            return

        if not inside_sandbox(new_path):
            print(Fore.RED + "❌ Cannot leave sandbox!")
            return

        os.chdir(new_path)
        return

    if cmd == "del":
        if not args:
            print(f"Usage: del <filename|*.ext>")
            return
        pattern = args[0]
        matches = glob.glob(os.path.join(os.getcwd(), pattern))
        if not matches:
            print(Fore.RED + f"❌ No files match: {pattern}")
            return
        for f in matches:
            if os.path.isfile(f):
                os.remove(f)
                print(Fore.GREEN + f"Deleted {os.path.basename(f)}")
        return

    os.system(cmdline)


def run_walkthrough(steps):
    print(Fore.CYAN + "\n📘 EasyCMD Walkthrough")
    print("Type the commands as instructed. Type 'exit' to quit.\n")

    for step in steps:
        while True:
            print(Fore.YELLOW + step["message"])
            user_input = input(format_prompt()).strip()

            if user_input.lower() == "exit":
                print(Fore.CYAN + "Exiting walkthrough.")
                return

            if user_input.lower() in step["expected"]:
                execute_command(user_input)
                print(Fore.GREEN + "✔ Correct!\n")
                print(Fore.GREEN + step["onsuccess"])
                break
            else:
                print(
                    Fore.RED
                    + "❌ Not quite.\n"
                    + Fore.YELLOW
                    + "Try one of these:\n  "
                    + "\n  ".join(step["expected"])
                    + "\n"
                )

    print(Fore.CYAN + "Walkthrough complete! You're ready to explore on your own.\n")
    print(Fore.CYAN + "Visit https://www.freecodecamp.org/news/command-line-commands-cli-tutorial/ for a more indepth tutorial to CLI commands.\n")


def main():
    print(Fore.CYAN + "✅ Entering sandbox...\n")
    print("Welcome to the terminal sandbox! You can test and learn terminal commands inside this sandox. (type exit to exit the sandbox)\n")
    print(Fore.CYAN + "Type 'walkthrough-help' and press enter for a guided walkthrough into terminal commands!\n")
    os.chdir(SANDBOX)

    while True:
        try:
            cmdline = input(format_prompt()).strip()
            if not cmdline:
                continue

            cmd = cmdline.split()[0].lower()

            if cmd == "exit":
                print(Fore.CYAN + "✅ Exiting sandbox...")
                break

            elif cmd == "help":
                print(BEGINNER_HELP)

            elif cmd == "walkthrough1":
                run_walkthrough(WALKTHROUGH1)

            elif cmd == "walkthrough2":
                run_walkthrough(WALKTHROUGH2)

            elif cmd == "walkthrough3":
                run_walkthrough(WALKTHROUGH3)
            elif cmd == "walkthrough-help":
                print(Fore.CYAN + "List of all the walkthroughs:\n")
                print("walkthrough1 : Helps to learn changing and making directories in the terminal.\n")
                print("walkthrough2 : Windows beginner commands like ping, version, ipconfig along with more file manipulation commands.\n")
                print("walkthrough3 : Teaches batch file creation, editing and running. (used for terminal automation)\n")
                print(Fore.CYAN + "Usage : type the walkthough you want to go through in the terminal for the walkthrough to begin!\n")
                print(Fore.CYAN + "Example : 'walkthrough1' to go through walkthrough1")

            else:
                execute_command(cmdline)

        except KeyboardInterrupt:
            print()
        except EOFError:
            print(Fore.CYAN + "\n✅ Exiting sandbox...")
            break

# ------------------------------
# Entry Point
# ------------------------------

if __name__ == "__main__":
    main()

