from tkinter import *
from tkinter import messagebox
import mysql.connector

status = False
r_status = False
register_state = True
register_state_1 = True
user_id = ''
warn = 0
time_count = 500

def login_using_user(password):
    global user_id, status, register_state_1

    register_state_1 = True
    status = False

    # Creating and executing the login interface
    def login_interface():
        global register_state_1
        register_state_1 = False

        # Deleting the login or register screen
        try:
            screen.destroy()
        except:
            pass

        # Function for checking the password
        def get_password():
            global status, user_id, warn

            # Getting the user id and password
            user_id = user_entry.get().lower()
            password = password_entry.get()
            warning_count = warn

            # Checking the user id and password
            if user_id not in records:

                if warning_count in (0, 1):

                    warning_count += 1
                    warn = warning_count
                    available = 3 - warning_count
                    user_entry.delete(0, END)
                    password_entry.delete(0, END)
                    messagebox.showwarning('WARNING', 'USER not found')

                elif warning_count == 2:

                    # Displaying and ending the login screen
                    warning_count = 3
                    warn = warning_count
                    messagebox.showerror('ERROR', '3 WRONG ATTEMPTS')
                    root.destroy()
                    status = False

            elif records[user_id] != password:

                if warning_count in (0, 1):
                    # Clearing the entry field
                    user_entry.delete(0, END)
                    password_entry.delete(0, END)

                    # Displaying the error
                    warning_count += 1
                    warn = warning_count
                    available = 3 - warning_count
                    messagebox.showwarning('WARNING', 'PASSWORD does not match')

                elif warning_count == 2:

                    # Displaying and ending the login screen
                    warning_count = 3
                    warn = warning_count
                    messagebox.showerror('ERROR', '3 WRONG ATTEMPTS')
                    root.destroy()
                    status = False

            else:
                user_entry.delete(0, END)
                password_entry.delete(0, END)

                # Displaying the message and ending the screen
                messagebox.showinfo('SUCCESS', 'SUCCESSFULLY LOGGED IN')
                root.destroy()

                status = True

        # Initializing the screen
        root = Tk()
        root.title('LOGIN')

        # Getting the records
        database = mysql.connector.connect(host='localhost', user='root', password='tharun', database='vaccine_project')
        cursor = database.cursor()
        cursor.execute('select * from passwords;')
        result = cursor.fetchall()
        records = {}
        for i in result:
            records.update({i[0]: i[1]})

        # Labels and buttons
        u_label = Label(root, text='User')
        u_label.grid(row=0, column=1)

        user_entry = Entry(root, width=30)
        user_entry.grid(row=0, column=2)

        p_label = Label(root, text='Password')
        p_label.grid(row=1, column=1)

        password_entry = Entry(root, show='*', width=30)
        password_entry.grid(row=1, column=2)

        login = Button(root, text='LOGIN', command=get_password)
        login.grid(row=2, column=1, columnspan=2)

        # Initiating the loop
        root.mainloop()

        if not status and warn < 3:
            login_using_user(password)

    # Creating and executing the register interface
    def register_interface():
        global register_state_1
        register_state_1 = False

        # Destroying the existing login or register screen
        screen.destroy()

        # Defining a function to register a record and add it to the database
        def insert_records():
            global user_id, status, r_status

            # Getting the user id and password
            user_id = user_entry.get().lower()
            password = password_entry.get()

            # Checking the existing records
            if password == '' or user_id == '':
                user_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showwarning('WARNING', 'USER or PASSWORD cannot be empty')

            elif user_id not in records:
                records[user_id] = password
                r_status = True

                # Adding the user to the database
                cursor.execute('Insert into passwords values(\'%s\',\'%s\')' % (user_id, password))
                database.commit()

                # Showing the success message and proceeding to log in to interface
                messagebox.showinfo("SUCCESS", "SUCCESSFULLY REGISTERED")
                root.destroy()

                login_interface()

            # Displaying error and getting a valid user and password
            else:
                user_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showwarning('WARNING', 'USER already exists')
                
        # Register interface
        root = Tk()
        root.title('REGISTER')

        # Getting the records
        database = mysql.connector.connect(host='localhost', user='root', password='tharun', database='vaccine_project')
        cursor = database.cursor()
        cursor.execute('select * from passwords;')
        result = cursor.fetchall()
        records = {}
        for i in result:
            records.update({i[0]: i[1]})

        # Labels and buttons
        u_label = Label(root, text='User')
        u_label.grid(row=0, column=1)

        user_entry = Entry(root, width=30)
        user_entry.grid(row=0, column=2)

        p_label = Label(root, text='Password')
        p_label.grid(row=1, column=1)

        password_entry = Entry(root, show='*', width=30)
        password_entry.grid(row=1, column=2)

        login = Button(root, text='REGISTER', command=insert_records)
        login.grid(row=2, column=1, columnspan=2)

        root.mainloop()

        if not r_status:
            login_using_user(password)

    def exit_button():
        choice = messagebox.askyesno("EXIT", "Do you want to exit???")
        if choice:
            screen.destroy()

    # Database
    new_database = mysql.connector.connect(host='localhost', user='root', password=password)
    new_cursor = new_database.cursor()
    new_cursor.execute('create database if not exists vaccine_project')
    new_cursor.execute('use vaccine_project')
    new_cursor.execute('create table if not exists passwords(user_id varchar(20), password varchar(20))')

    # Login or Register screen
    screen = Tk()
    screen.title('REGISTER AND LOGIN')

    login_button = Button(screen, text='LOGIN', padx=97, pady=4, command=login_interface, state=NORMAL, font=('Times', 15))
    login_button.grid(row=0, column=0, sticky=W+E)

    register_button = Button(screen, text='REGISTER', padx=61, pady=4, command=register_interface, state=NORMAL, font=('Times', 15))
    register_button.grid(row=1, column=0, sticky=W+E)

    exit_button_display = Button(screen, text='EXIT', padx=100, pady=4, command=exit_button, state=NORMAL, font=('Times', 15))
    exit_button_display.grid(row=2, column=0, sticky=W+E)

    screen.protocol('WM_DELETE_WINDOW', exit_button)

    screen.mainloop()

    return user_id, status
