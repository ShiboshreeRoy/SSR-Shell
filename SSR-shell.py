import os
import tkinter as tk
from tkinter import messagebox

__author__ = "Shiboshree Roy"
__version__ = "2.0"
__shell_name__ = "SSR Shell"
__dev__ = "Shiboshree Roy"

class SSRShellApp:
    """
    SSR Shell - A Python-based shell GUI that provides an OS-like environment for executing basic commands.
    Supports commands like 'ls', 'cd', 'touch', 'pwd', 'cat', 'echo', and 'help'.
    Designed for simplicity with an interactive interface.
    """

    def __init__(self, root):
        self.root = root
        self.root.title(f"{__shell_name__}")
        self.root.geometry("900x600")
        self.root.config(bg="black")
        
        # Command Entry
        self.command_label = tk.Label(root, text="SSR Shell - Enter Command:", fg="lime", bg="black", font=("Courier New", 12))
        self.command_label.pack(pady=5)
        self.command_entry = tk.Entry(root, width=80, font=("Courier New", 12), fg="lime", bg="black")
        self.command_entry.pack(pady=5)
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.bind("<Control-l>", self.clear_output)
        self.command_entry.bind("<Up>", self.navigate_history)
        self.command_entry.bind("<Down>", self.navigate_history)

        # Set up command history
        self.command_history = []
        self.history_index = -1

        # Output Text Area
        self.output_area = tk.Text(root, width=100, height=25, wrap=tk.WORD, font=("Courier New", 12), bg="black", fg="lime")
        self.output_area.pack(pady=5)

        # Execute Button
        self.execute_button = tk.Button(root, text="Execute", command=self.execute_command, fg="white", bg="blue", font=("Courier New", 12))
        self.execute_button.pack(pady=5)

        # Display initial information about the shell, author, and version
        self.display_startup_info()

    def display_startup_info(self):
        info_text = f"""
        Welcome to {__shell_name__} - A Python-powered OS-like environment.
        Author : {__author__}
        Developer : {__dev__}
        Version : {__version__}
        
        Type 'help' for a list of available commands.
        """
        self.display_output(info_text, "green")

    def execute_command(self, event=None):
        command = self.command_entry.get().strip().split()
        if not command:
            return
        elif command[0] == "exit":
            self.exit_shell()
        elif command[0] == "ls":
            self.list_files(command)
        elif command[0] == "cd":
            self.change_directory(command)
        elif command[0] == "touch":
            self.create_file(command)
        elif command[0] == "pwd":
            self.print_working_directory()
        elif command[0] == "cat":
            self.cat_file(command)
        elif command[0] == "echo":
            self.echo(command)
        elif command[0] == "help":
            self.display_help()
        else:
            self.display_output(f"Unknown command: {command[0]}", "red")
        
        self.command_entry.delete(0, tk.END)
        self.command_history.append(" ".join(command))
        self.history_index = len(self.command_history)

    def list_files(self, command):
        show_all = "-a" in command
        files = os.listdir(".") if show_all else [f for f in os.listdir(".") if not f.startswith(".")]
        files.sort()
        self.display_output("\n".join(files), "blue")

    def change_directory(self, command):
        if len(command) > 1:
            path = command[1]
            try:
                os.chdir(path)
                self.display_output(f"Changed directory to {os.getcwd()}", "blue")
            except FileNotFoundError:
                self.display_output("Directory not found!", "red")
            except NotADirectoryError:
                self.display_output(f"{path} is not a directory!", "red")
        else:
            self.display_output("Usage: cd <directory>", "yellow")

    def create_file(self, command):
        if len(command) > 1:
            filename = command[1]
            try:
                with open(filename, "w") as f:
                    f.write("")
                self.display_output(f"File '{filename}' created.", "blue")
            except Exception as e:
                self.display_output(f"Error creating file: {e}", "red")
        else:
            self.display_output("Usage: touch <filename>", "yellow")

    def print_working_directory(self):
        self.display_output(os.getcwd(), "blue")

    def cat_file(self, command):
        if len(command) > 1:
            filename = command[1]
            try:
                with open(filename, "r") as f:
                    content = f.read()
                self.display_output(content, "blue")
            except FileNotFoundError:
                self.display_output(f"{filename} not found!", "red")
            except Exception as e:
                self.display_output(f"Error reading file: {e}", "red")
        else:
            self.display_output("Usage: cat <filename>", "yellow")

    def echo(self, command):
        self.display_output(" ".join(command[1:]), "green")

    def display_output(self, message, color="white"):
        self.output_area.insert(tk.END, f"{__shell_name__}:~$ {message}\n")
        self.output_area.tag_add(color, "1.0", "end")
        self.output_area.tag_config(color, foreground=color)
        self.output_area.see(tk.END)

    def display_help(self):
        help_text = """
        Available Commands:
        - ls        : List files in the current directory
        - cd <dir>  : Change directory
        - touch <filename>  : Create an empty file
        - pwd       : Print working directory
        - cat <file>: Display the content of a file
        - echo <msg>: Print the message to the terminal
        - help      : Show this help message
        - exit      : Exit the shell
        """
        self.display_output(help_text, "blue")

    def exit_shell(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            self.root.quit()

    def clear_output(self, event=None):
        self.output_area.delete(1.0, tk.END)

    def navigate_history(self, event):
        if event.keysym == 'Up' and self.history_index > 0:
            self.history_index -= 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        elif event.keysym == 'Down' and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.history_index])
        else:
            self.command_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SSRShellApp(root)
    root.mainloop()



