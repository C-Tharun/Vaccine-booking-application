from tkinter import *
from tkinter import ttk

# Importing connection
import mysql.connector
conn = mysql.connector.connect(user='root', password='tharun', host='localhost', database='vaccine_project')

def registration_form():
    patient_list.destroy()

    def register():
        name1 = name.get()
        con1 = contact.get()
        email1 = email.get()
        gen1 = gender.get()
        city1 = citychoosen.get()
        hospital1 = hospchoosen.get()
        date1 = datechoosen.get()
        slot1 = slotchoosen.get()
        vaccine1 = vaccine.get()
        hospital1 = hospital.replace(' ', '_')


        if name1 == '' or con1 == '' or email1 == '' or gen1 == 0 or city1.upper() == 'NONE' or hospital1 == 'NONE' or date1.upper() == 'NONE' or slot1.upper() == 'NONE' or vaccine1 == 0:
            message.set("Fill all the fields")

        elif len(con1) == 0 or not con1.isdigit() or len(con1)!=10 :
            message.set("Provide valid contact number")

        elif len(email1.split('@')) != 2 or email1[-4:] != '.com'or len(email1.split('@')[1].split('.')[0]) == 0:
            message.set("Provide valid email")

        else:
            cursor = conn.cursor()
            insert_stmt = "INSERT INTO patient_list(NAME, CONTACT, EMAIL, GENDER, CITY, USER_ID, VACCINE, dov, slot_no, hospital_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            if gen1 == 1:
                gen_name = 'Male'
            else:
                gen_name = 'Female'

            if vaccine1 == 1:
                vac_name = 'Covaccine'
            else:
                vac_name = 'Covishield'

            slot_no = ['8:30 - 9:00', '9:00 - 9:30', '9:30 - 10:00', '10:00 - 10:30'].index(slot1) + 1
            data = (name1, con1, email1, gen_name, city1, user_id, vac_name, date1, slot1, hospital1)

            cursor.execute(insert_stmt, data)
            cursor.execute('update %s set slot%d = slot%d - 1 where dov = "%s"' % (hospital1, slot_no, slot_no, date1))
            conn.commit()
            # conn.rollback()

            message.set("Stored successfully")

            reg_screen.destroy()

    

    def alter_tree(event):
        global city

        city = citychoosen.get()
        citychoosen.set(city)
        req_list = []
        cursor = conn.cursor()
        cursor.execute('select name from hospital where city = "%s"' % city)
        req_list = cursor.fetchall()
        req_list = [i[0] for i in req_list]

        hospchoosen['values'] = req_list

        hospchoosen.set('NONE')
        datechoosen.set('SELECT HOSPITAL')
        datechoosen['values'] = []
        slotchoosen.set('SELECT DATE')
        slotchoosen['values'] = []

    def alter_tree_1(event):
        global hospital

        hospital = hospchoosen.get()
        hospchoosen.set(hospital)
        hospital1 = hospital.replace(' ', '_')
        req_list = []
        cursor = conn.cursor()
        cursor.execute('create table if not exists %s(dov date primary key, slot1 int default 5, slot2 int default 5, slot3 int default 5, slot4 int default 5)' % hospital1)
        cursor.execute('delete from %s where dov < date(now())' % hospital1)
        for i in range(7):
            try:
                cursor.execute('insert into %s(dov) values((SELECT DATE_ADD(date(now()), INTERVAL %d DAY)));' % (hospital1, i))
            except:
                pass
        conn.commit()
        cursor.execute('select dov from %s where slot1 > 0 or slot2 > 0 or slot3 > 0 or slot4 > 0' % hospital1)
        req_list = cursor.fetchall()
        req_list = [i[0] for i in req_list]

        datechoosen['values'] = req_list

        datechoosen.set('NONE')
        slotchoosen.set('SELECT DATE')
        slotchoosen['values'] = []

    def alter_tree_2(event):
        global hospital, slot, date

        hospital1 = hospital.replace(' ', '_')
        date = datechoosen.get()
        datechoosen.set(date)
        req_list = []
        cursor = conn.cursor()
        cursor.execute('select slot1, slot2, slot3, slot4 from %s where dov = "%s"' % (hospital1, date))
        req_list = cursor.fetchall()[0]
        slot1, slot2, slot3, slot4 = req_list
        req_list = []
        if slot1 > 0:
            req_list.append('8:30 - 9:00')

        if slot2 > 0:
            req_list.append('9:00 - 9:30')

        if slot3 > 0:
            req_list.append('9:30 - 10:00')

        if slot4 > 0:
            req_list.append('10:00 - 10:30')

        slotchoosen['values'] = req_list

        slotchoosen.set('NONE')

    global reg_screen
    reg_screen = Tk()
    reg_screen.title("Registration Form")

    # Setting height and width of screen
    reg_screen.geometry("350x480")
    global message
    global name

    global email
    global gender
    global city
    global hospital
    global date
    global slot
    global vaccine

    name = StringVar()
    contact = StringVar()
    email = StringVar()
    gender = IntVar()
    vaccine = IntVar()
    city = StringVar()
    state = StringVar()
    message = StringVar()
    hospital = StringVar()
    date = StringVar()
    slot = IntVar()

    Label(reg_screen, width="300", text="Please enter details below", bg="lightblue", fg="red").pack()

    # Name Label
    Label(reg_screen, text="Name * ").place(x=20, y=40)

    # Name textbox
    Entry(reg_screen, textvariable=name).place(x=90, y=44)

    # Contact Label
    Label(reg_screen, text="Contact * ").place(x=20, y=80)

    # Contact textbox
    Entry(reg_screen, textvariable=contact).place(x=90, y=80)

    # email Label
    Label(reg_screen, text="Email * ").place(x=20, y=120)

    # email textbox
    Entry(reg_screen, textvariable=email).place(x=90, y=122)

    # gender Label
    Label(reg_screen, text="Gender * ").place(x=20, y=160)

    # gender radiobutton
    Radiobutton(reg_screen, text="Male", variable=gender, value=1).place(x=90, y=162)
    Radiobutton(reg_screen, text="Female", variable=gender, value=2).place(x=150, y=162)

    Label(reg_screen, text="Vaccine * ").place(x=20, y=202)

    Radiobutton(reg_screen, text="Covaccine", variable=vaccine, value=1).place(x=90, y=202)
    Radiobutton(reg_screen, text="Covishield", variable=vaccine, value=2).place(x=170, y=202)

    # city Label
    Label(reg_screen, text="City * ").place(x=20, y=242)
    # city combobox
    citychoosen = ttk.Combobox(reg_screen, width=27, textvariable=city)
    citychoosen['values'] = ('NONE', 'Chennai', 'Mumbai', 'Bangalore', 'Kochi', 'Kolkata',)
    citychoosen.current(0)
    citychoosen.place(x=90, y=242)
    citychoosen.bind('<<ComboboxSelected>>', alter_tree)

    # hosp Label
    Label(reg_screen, text="Hospital * ").place(x=20, y=282)
    # hosp combobox
    hospchoosen = ttk.Combobox(reg_screen, width=27, textvariable=hospital)
    hospchoosen['values'] = []
    hospchoosen.set('SELECT HOSPITAL')
    hospchoosen.place(x=90, y=282)
    hospchoosen.bind('<<ComboboxSelected>>', alter_tree_1)

    # date Label
    Label(reg_screen, text="Date * ").place(x=20, y=322)
    # date combobox
    datechoosen = ttk.Combobox(reg_screen, width=27, textvariable=date)
    datechoosen['values'] = []
    datechoosen.set('SELECT DATE')
    datechoosen.place(x=90, y=322)
    datechoosen.bind('<<ComboboxSelected>>', alter_tree_2)

    # slot Label
    Label(reg_screen, text="Slot * ").place(x=20, y=362)
    # slot combobox
    slotchoosen = ttk.Combobox(reg_screen, width=27, textvariable=slot)
    slotchoosen['values'] = []
    slotchoosen.set('SELECT SLOT')
    slotchoosen.place(x=90, y=362)
    slotchoosen.bind('<<ComboboxSelected>>')

    # Label for displaying login status[success/failed]

    Label(reg_screen, text="", textvariable=message).place(x=95, y=442)
    # Login button
    Button(reg_screen, text="Register", width=10, height=1, bg="gold", command=register).place(x=105, y=402)

    reg_screen.mainloop()



def vacancy():
    # city Label
    Label(reg_screen, text="City * ").place(x=20, y=242)
    # city combobox
    citychoosen = ttk.Combobox(reg_screen, width=27, textvariable=city)
    citychoosen['values'] = ('NONE', 'Chennai', 'Mumbai', 'Bangalore', 'Kochi', 'Kolkata',)
    citychoosen.current(0)
    citychoosen.place(x=90, y=242)
    citychoosen.bind('<<ComboboxSelected>>', alter_tree)

    # hosp Label
    Label(reg_screen, text="Hospital * ").place(x=20, y=282)
    # hosp combobox
    hospchoosen = ttk.Combobox(reg_screen, width=27, textvariable=hospital)
    hospchoosen['values'] = []
    hospchoosen.set('SELECT CITY')
    hospchoosen.place(x=90, y=282)
    hospchoosen.bind('<<ComboboxSelected>>', alter_tree_1)

            

def form():
    patient_list.destroy()

    cursor = conn.cursor()
    cursor.execute('select Name, Contact, Email, Gender, City, Vaccine, Dov, Slot_no, Hospital_Name from patient_list where user_id = "%s"' % user_id)
    result = cursor.fetchall()

    if not result:
        result = [('', '', '', 'NO', 'RECORDS', 'FOUND', '', '', '')]

    def back_function():
        display_screen.destroy()

    display_screen = Tk()
    display_screen.title('PATIENT LIST')

    user_label = Label(display_screen, text='USER_ID : '+user_id, font=('Times New roman', 12))
    user_label.grid(row=0, column=0)

    patient_frame = Frame(display_screen)
    patient_frame.grid(row=1, column=0)

    back = Button(display_screen, text='BACK', command=back_function)
    back.grid(row=2, column=0, sticky=N + S + W + E, pady=4)

    scroll = Scrollbar(patient_frame, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill='y')

    high_score = ttk.Treeview(patient_frame, height=7, yscrollcommand=scroll.set)
    high_score.pack()

    scroll.config(command=high_score.yview)

    high_score['columns'] = ("Name", "Contact", "Email", "Gender", "City", "Vaccine", "Date", "Slot", "Hospital")

    high_score.column("#0", width=0, stretch=NO)
    high_score.column("Name", anchor=CENTER, width=150)
    high_score.column("Contact", anchor=CENTER, width=100)
    high_score.column("Email", anchor=CENTER, width=150)
    high_score.column("Gender", anchor=CENTER, width=70)
    high_score.column("City", anchor=CENTER, width=100)
    high_score.column("Vaccine", anchor=CENTER, width=80)
    high_score.column("Date", anchor=CENTER, width=80)
    high_score.column("Slot", anchor=CENTER, width=80)
    high_score.column("Hospital", anchor=CENTER, width=150)

    high_score.heading('Name', text='Name', anchor=CENTER)
    high_score.heading('Contact', text='Contact', anchor=CENTER)
    high_score.heading('Email', text='Email', anchor=CENTER)
    high_score.heading('Gender', text='Gender', anchor=CENTER)
    high_score.heading('City', text='City', anchor=CENTER)
    high_score.heading('Vaccine', text='Vaccine', anchor=CENTER)
    high_score.heading('Date', text='Date', anchor=CENTER)
    high_score.heading('Slot', text='Slot', anchor=CENTER)
    high_score.heading('Hospital', text='Hospital', anchor=CENTER)

    for position in range(len(result)):
        result[position] = list(result[position])
        high_score.insert(parent='', index=END, iid=position, text='', value=result[position])

    display_screen.mainloop()


import login
user_id, status = login.login_using_user('tharun')

def exit_button():
    patient_list.destroy()

    global status
    status = False
    exit()


while status:

    patient_list = Tk()
    patient_list.geometry('250x250')
    patient_list.title('Main Window')

    userid = Label(patient_list, text='USER_ID : '+user_id, font=('Times New roman', 12))
    userid.pack(anchor=NE, padx=20, pady=8)
    newp = Button(patient_list, text='REGISTER A PATIENT', command=registration_form, font=('Times New roman', 12))
    newp.pack(padx=20, pady=8)
    oldp = Button(patient_list, text='VIEW PATIENTS', command=form, font=('Times New roman', 12))
    oldp.pack(padx=20, pady=8)
    
    exitb = Button(patient_list, text='EXIT', command=exit_button, font=('Times New roman', 12))
    exitb.pack(padx=20, pady=8)

    patient_list.protocol('WM_DELETE_WINDOW', exit_button)

    patient_list.mainloop()
