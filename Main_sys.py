###MYSQL-Python-User_Interface###
import PySimpleGUI as sg
import MYSQL_Connection
import Loggin_sys
import SQL_Statements as SQLS

##Main file##
#Refer to events section for more help about input types / media


##Set up the mysql_connection object:
"""
user = 'root'
password = 'Joshua100x'
host = '127.0.0.1'
database = 'sql_store'
connection = 'connection1'

connection_obj = MYSQL_Connection.mysql_connection(user, password, host, database)
connection_obj.setUp_connection(connection)
"""
"""
#The one-shot window:

#Change the theme of the windows loaded with sg
#sg.theme('DarkAmber')

layout = [[sg.Text("My first window")],
          [sg.InputText(key='-IN-')],
          [sg.Submit(), sg.Cancel()]
    ]

window = sg.Window('Home', layout)

event, values = window.read()

window.close()

sg.popup("You entered", values['-IN-'])


#Interactive Window:
layout = [[sg.Text("What is your name")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('OK'), sg.Button('Quit')]                     
    ]

window = sg.Window('Home', layout)

#Display the window using an Event loop:
while True:
    #event describes any action take by the user:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    window['-OUTPUT-'].update(value='Hello ' + values['-INPUT-'] + "! Thanks for trying PySimple GUI", text_color = 'yellow')

window.close()


#Layouts:
layout = [  [sg.Text('Row 1'), sg.Text("What's your name?")],
            [sg.Text('Row 2'), sg.Input()],
            [sg.Text('Row 3'), sg.Button('Ok')] ]

window = sg.Window('Home', layout)

event, values = window.read()








#List comprehensions for layouts:
#Try to put all the table names for a database in one row as buttons:
#Result: success

tables = ['Table1', 'Table2', 'Table3', 'Table4', 'Table5', 'Table6', 'Table7', 'Table8', 'Table9']

layout = [[[sg.Button(tables[j]) for i in range(1)] for j in range(len(tables))],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('OK'), sg.Button('Quit')]
          ]

window = sg.Window('Home', layout)

while True:
    #event describes any action take by the user:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    window['-OUTPUT-'].update(value='Hello ' + values['-INPUT-'] + "! Thanks for trying PySimple GUI", text_color = 'yellow')

window.close()



"""


#Create a window with a frame element inside of it:
connection = 'connection1'

#Create the process to update the table names based on the database:
def load_main_page(session_user, log_in_window):

    #load session users mysql_connection:
    #session_user.connect()
    
        
    def change_databases(window, values):
        tables = get_tables(values["Databases"][0])
        session_user.database = values["Databases"][0]
        session_user.connection_obj.database = values["Databases"][0]
        window["Tables"].update(tables)


    def get_databases():
        databases = session_user.connection_obj.get_database_names(connection)
        return databases


    def get_tables(database):
        tables = session_user.connection_obj.get_table_names(database, connection)
        return tables


    def show_table(window, values, current_table):
        window["create_database_page"].update(visible=False)
        window["create_table_page"].update(visible=False)
        window[current_table].update(visible=False)
        window[values["Tables"][0]].update(visible=True)
        current_table = values["Tables"][0]
        return current_table


    def delete_table(window, values, current_table):
        is_dropped = session_user.connection_obj.delete_table(values["Tables"][0], connection)
        print(is_dropped)
        tables = get_tables(session_user.database)
        window["Tables"].update(tables)
        #Change from current table to the first one in the database
        if len(list(session_user.connection_obj.connection_details[session_user.database].keys())) < 1:
            window[values["Tables"][0]].update(visible=False)
        else:
            window[values["Tables"][0]].update(visible=False)
            window[list(session_user.connection_obj.connection_details[session_user.database].keys())[0]].update(visible=True)
            current_table = list(session_user.connection_obj.connection_details[session_user.database].keys())[0]
        return current_table


    def create_new_table(values, current_table):
        print(values)
        table_name = values["INPUT_TABLE_name"].lower()
        attribute_names = [values["INPUT_Attribute1"], values["INPUT_Attribute2"], values["INPUT_Attribute3"]]
        attribute_types = ["VARCHAR(30)", "VARCHAR(30)", "VARCHAR(30)"]
        worked = session_user.connection_obj.create_new_table(table_name, attribute_names, attribute_types, connection)
        print("Has is worked?:",worked)
        return table_name


    def create_new_database(window, values):
        database_name = values["INPUT_DATABASE_name"].lower()
        worked = session_user.connection_obj.create_new_database(database_name, connection)
        session_user.database = database_name
        session_user.connection_obj.database = database_name


    def delete_database(window, values):
        is_dropped = session_user.connection_obj.delete_database(values["Databases"][0], connection)
        databases = get_databases()
        session_user.database = databases[0]
        session_user.connection_obj.database = databases[0]
        print("2 Has it worked?:",is_dropped)


    def create_select_layout(session_user, values):
        print(values)
        table = values["Tables"][0]
        attributes = session_user.connection_obj.get_table_attributes(table, connection)
        attributes_listboxes = [[sg.Checkbox(attributes[i], size=(50, 20), key=attributes[i])] for i in range(len(attributes))]
        print(attributes_listboxes)
        where_conjunctions = ["AND", "OR"]
        where_signs = ["=", "NOT =", "NOT", ">=", "<=", ">", "<", "IN"]
        selection_layout = [
            [sg.Text("SELECT")],
            *attributes_listboxes,
            [sg.Text("FROM"), sg.Text(table)],
            [sg.Text("WHERE"), sg.Combo(attributes, default_value=None, size=(8,2), key="WHERE_attribues_list_box1"),
             sg.Combo(where_signs, default_value=None, size=(8,2), key="WHERE_signs_list_box1"),
             sg.Input(key="WHERE_INPUT_value1")]   ,
            [sg.Button("SELECT", size=(8,2), key="INPUT_CREATE_SELECT_STATEMENT")]
            ]
        return selection_layout




    def create_selection_statement(window, session_user, values, current_table):
        print(values)
        table = session_user.database + "." + current_table
        is_all = False
        is_where = True
        attributes = session_user.connection_obj.get_table_attributes(table, connection)
        print(attributes)
        listbox_attributes = [attribute for attribute in attributes if values[attribute] == True]
        where_attributes = ""
        where_condition = ""
        where_values = ""
        where_and_or = ""
        if len(attributes) == len(listbox_attributes):
            is_all = True
        if values["WHERE_attribues_list_box1"] == None and values["WHERE_signs_list_box1"] == None and values["WHERE_INPUT_value1"] == None:
            is_where = False
        else:
            where_attributes = values["WHERE_attribues_list_box1"]
            where_condition = values["WHERE_signs_list_box1"]
            where_values = values["WHERE_INPUT_value1"]
            
        SELECT_statement = SQLS.create_SELECT_statement(is_all, listbox_attributes, table, is_where, [where_attributes], [where_condition], [where_values], [where_and_or])
        print(SELECT_statement)

        #Run select statement and return query result:
        SELECT_data = session_user.connection_obj.run_select_statement(connection, SELECT_statement)
        SELECT_data2 = [str(data) for data in SELECT_data]
        print(SELECT_data)

        #Update the output box with the result and the query:
        output_text1 = "SELECT STATEMENT RETURNED:\n" + "\n" + "\n".join(SELECT_data2) + "\n" + "\nThis was generated from query:\n" + "\n" + "'" + SELECT_statement + "'"
        window["SQL_OUTPUT"].update(output_text1)

    def create_layout(session_user, current_table, manipulate_table_layout):
        connection = 'connection1'
        current_Database = session_user.database
        databases = get_databases()
        
        tables = get_tables(session_user.database)

        #Defualt to the first table in the entire connection if there isn't one:
        if len(tables) < 1:
            try:
                current_table = session_user.connection_obj.connection_details[session_user.connection_obj.connection_details.keys()[0]].keys()[0]
            except:
                #Create new table in the event there isn't one to connect too:
                values = {'Databases': ['world'],
                          'Tables': [],
                          'current_table1': [], 'current_table10': [], 'current_table11': [],
                          'INPUT_TABLE_name': 'Table1', 'INPUT_Attribute1': 'ID', 'INPUT_Attribute2': 'Name', 'INPUT_Attribute3': 'Address', 'INPUT_DATABASE_name': ''}
                current_table = create_new_table(values, current_table)
        else:
            current_table = tables[0].lower()

            
        #Create table popup
        create_table_popup = [
            [sg.Text("Create Table:", size=(40,1))],
            [sg.Text("Table Name:", size=(10, 1)), sg.Input(key="INPUT_TABLE_name", size=(10, 20))],
            [sg.Text("Attribute1:", size=(10, 1)), sg.Input(key="INPUT_Attribute1", size=(10, 20))],
            [sg.Text("Attribute2:", size=(10, 1)), sg.Input(key="INPUT_Attribute2", size=(10, 20))],
            [sg.Text("Attribute3:", size=(10, 1)), sg.Input(key="INPUT_Attribute3", size=(10, 20))],
            [sg.Button("Create Table", size=(9, 1), key="INPUT_create_table_popUp_button"), sg.Button("Cancel", size=(9, 1), key="INPUT_create_table_cancel")]
            ]


        #Create Database popup
        create_database_popup = [
            [sg.Text("Create Database", size=(40, 1))],
            [sg.Text("Database Name: ", size=(10, 1)), sg.Input(key="INPUT_DATABASE_name", size=(10, 20))],
            [sg.Button("Create Database", size=(9, 1), key="INPUT_create_database_popUp_button"), sg.Button("Cancel", size=(9, 1), key="INPUT_create_database_cancel")]
            ]
        

        #Add buttons to the table list frame
        frame_layout_tables = [
            [sg.LB(tables, enable_events=True, size=(20, 27), key="Tables")],
            [sg.Button("Create Table", key="INPUT_CREATE_TABLE", size=(8, 2)), sg.Button("Delete Table", key="INPUT_DELETE_TABLE", size=(8, 2))]
            ]

        #Manipulate tables section:
        select_query_layout = [
            [sg.Text("Manipulate Table", size=(40, 1))],
            ]

        if manipulate_table_layout:
            for layout in manipulate_table_layout:
                select_query_layout.append(layout)

        #Create a table object for each table in the database and hide all bar 1:
        frame_all_tables_data = []
        for database in databases:
            session_user.connection_obj.database = database
            tables = get_tables(database)
            for table in tables:
                table_attributes = session_user.connection_obj.get_table_attributes(table, connection)
                table_data = session_user.connection_obj.get_table_data(table, connection)
                frame_table_data = [
                    [sg.Table(values=table_data, headings = table_attributes, auto_size_columns=False, col_widths=list(map(lambda x: len(x) + 1, table_attributes)), size=(900, 900), key="current_table1")]
                ]
                frame_all_tables_data.append(sg.Frame(table, layout=frame_table_data, font="Any 12", title_color="black", size=(1000, 900), key=table, visible=False))
                
        frame_all_tables_data.append(sg.Frame("Create Table", layout=create_table_popup, font="Any 12", title_color="black", size=(450, 900), key="create_table_page", visible=False))
        frame_all_tables_data.append(sg.Frame("Create Database", layout=create_database_popup, font="Any 12", title_color="black", size=(900, 900), key="create_database_page", visible=False))

        frame_all_tables_data.append(sg.Frame("Manipulate Tables", layout=select_query_layout, font="Any 12", title_color="black", size=(450, 900), key="manipulate_tables_page"))
        

        #Add buttons to the database frame:
        frame_layout_databases = [
            [sg.LB(databases, enable_events=True, size=(20, 35), key="Databases"), sg.Frame("Tables", frame_layout_tables, font="Any 12", title_color="black")],
            [sg.Button("Create Database", key="INPUT_CREATE_DATABASE", size=(9, 2)), sg.Button("Delete Database", key="INPUT_DELETE_DATABASE", size=(9, 2))]
            ]

        operations = [
            [sg.Button("SELECT", key="INPUT_SELECT", size=(15, 4))],
            [sg.Button("DELETE", key="INPUT_DELETE", size=(15, 4))],
            [sg.Button("INSERT", key="INPUT_INSERT", size=(15, 4))],
            [sg.Button("UPDATE", key="INPUT_UPDATE", size=(15, 4))]
            ]

        sql_query_output_layoyt = [
            [sg.Multiline(key="SQL_OUTPUT", size=(200, 200))]
            ]

        layout = [
            [sg.Frame("Databases", frame_layout_databases, font="Any 12", title_color="black", size=(400, 750)),
             sg.Frame("Current Table", [frame_all_tables_data], font="Any 12", title_color="black", size=(1150, 750), key="curent_table2"),
             sg.Frame("Operations", operations, font="Any 12", title_color="black", size=(220, 750), key="operations")],
            [sg.Frame("SQL Statement Output", layout=sql_query_output_layoyt, font="Any 12", title_color="black", size=(1750, 200))]
            ]

        return layout, current_table

    current_table = ""
    layout_return = create_layout(session_user, current_table, None)
    layout = layout_return[0]
    current_table = layout_return[1].lower()
    
    window = sg.Window('Home', layout, font=("Helvetica", 12), size=(1750, 980))

    #Delay the closing of the log-in window till the main page has loaded:
    log_in_window.close()

    new_table_counter = 1

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        elif event == "Databases":
            change_databases(window, values)
        elif event == "Tables":
            current_table = show_table(window, values, current_table)
        elif event == "INPUT_DELETE_TABLE":
            current_table = delete_table(window, values, current_table)

            #Display Delete statement:
            output_text = "TABLE WAS DELETED:\n" + "\nThis was perfromed by this query:\n" + "\n" + session_user.connection_obj.last_statement
            window["SQL_OUTPUT"].update(output_text)
            
        elif event == "INPUT_CREATE_TABLE":
            window[current_table].update(visible=False)
            window["create_database_page"].update(visible=False)
            window["create_table_page"].update(visible=True)
        elif event == "INPUT_create_table_cancel":
            window["create_table_page"].update(visible=False)
            window[current_table].update(visible=True)
        elif event == "INPUT_create_table_popUp_button":
            current_table = create_new_table(values, current_table)
            current_table.lower()
            #Make new window with the changes:
            layout = create_layout(session_user, current_table, None)[0]
            window.close()
            window = sg.Window('Home', layout, font=("Helvetica", 12), size=(1750, 950))
            #Return to normal:
            event, values = window.read()
            window["create_table_page"].update(visible=False)
            window[current_table].update(visible=True)
            
            #Display create statement:
            output_text = "TABLE WAS CREATED:\n" + "\nThis was perfromed by this query:\n" + "\n" + session_user.connection_obj.last_statement
            window["SQL_OUTPUT"].update(output_text)
            
        elif event == "INPUT_CREATE_DATABASE":
            window[current_table].update(visible=False)
            window["create_table_page"].update(visible=False)
            window["create_database_page"].update(visible=True)           
        elif event == "INPUT_create_database_popUp_button":
            create_new_database(window, values)
            #Make new window with the changes:
            layout = create_layout(session_user, current_table, None)[0]
            window.close()
            window = sg.Window('Home', layout, font=("Helvetica", 12), size=(1750, 950))
            event, values = window.read()
            window["create_database_page"].update(visible=True)
            window[current_table].update(visible=False)
            
            #Display create statement:
            output_text = "DATABASE WAS CREATED:\n" + "\nThis was perfromed by this query:\n" + "\n" + session_user.connection_obj.last_statement
            window["SQL_OUTPUT"].update(output_text)
            
        elif event == "INPUT_create_database_cancel":
            window["create_table_page"].update(visible=False)
            window["create_database_page"].update(visible=False)
            window[current_table].update(visible=True)
        elif event == "INPUT_DELETE_DATABASE":
            delete_database(window, values)
            layout_return = create_layout(session_user, current_table, None)
            layout = layout_return[0]
            current_table = layout_return[1]
            window.close()
            window = sg.Window('Home', layout, font=("Helvetica", 12), size=(1750, 950))
            event, values = window.read()
            window["create_database_page"].update(visible=False)
            window[current_table].update(visible=True)
            
            #Display drop statement:
            output_text = "DATABASE WAS DELETED:\n" + "\nThis was perfromed by this query:\n" + "\n" + session_user.connection_obj.last_statement
            window["SQL_OUTPUT"].update(output_text)
            
        elif event == "INPUT_SELECT":
            manipulate_table_layout = create_select_layout(session_user, values)
            layout_return = create_layout(session_user, current_table, manipulate_table_layout)
            layout = layout_return[0]
            window.close()
            window = sg.Window('Home', layout, font=("Helvetica", 12), size=(1750, 950))
            event, values = window.read()
        elif event =="INPUT_CREATE_SELECT_STATEMENT":
            create_selection_statement(window, session_user, values, current_table)
        else:
            continue
        window.Refresh()



#Log-in screen:

#create log-in object:
log_in_obj = Loggin_sys.login_handler()

def change_menu_create_user():
    window["log-in"].update(visible=False)
    window["create_user"].update(visible=True)

def change_menu_log_in_user():
    window["create_user"].update(visible=False)
    window["log-in"].update(visible=True)

log_in_box =[
    [sg.Text("", size=(40,1))],
    [sg.Text("Log-in Screen:", size=(40,1))],
    [sg.Text("           ______________________________", size=(40,1))],
    [sg.Text("Username:", size=(10, 1)), sg.Input(key="INPUT_username", size=(10, 20))],
    [sg.Text("Password:", size=(10, 1)), sg.Input(key="INPUT_password", size=(10, 20))],
    [sg.Text("           ______________________________", size=(40,1))],
    [sg.Button("log-in", size=(7, 1), key="INPUT_log_in_btn"), sg.Button("Create User", size=(9, 1), key="INPUT_goTo_create_user_btn")]
    ]

create_user_screen = [
    [sg.Text("", size=(40,1))],   
    [sg.Text("Create User Screen", size=(40,1))],
    [sg.Text("                _______________________", size=(40,1))],
    [sg.Text("New - Username", size=(15, 1))],
    [sg.Input(key="INPUT_new_username", size=(15, 25))],
    [sg.Text("New - Password", size=(15, 1))],
    [sg.Input(key="INPUT_new_password", size=(15, 25))],
    [sg.Text("New - host", size=(15, 1))],
    [sg.Input(key="INPUT_new_host", size=(15, 25))],
    [sg.Text("New - database", size=(15, 1))],
    [sg.Input(key="INPUT_new_database", size=(15, 25))],
    [sg.Text("                _______________________", size=(40,1))],
    [sg.Button("Create_user", size=(9, 1), key="INPUT_create_user_btn"), sg.Button("Cancel", size=(7, 1), key="INPUT_cancel_user_btn")]
    ]


shift_down = [
    [sg.Text("", size=(40,1))],
    [sg.Text("", size=(40,1))]
    ]


log_in_screen = []
log_in_screen.append(sg.Frame("Log-In", layout=log_in_box, font="Any 12", title_color="black", size=(400, 350), key="log-in", visible=True, vertical_alignment='center', element_justification='c'))
log_in_screen.append(sg.Frame("Create User", layout=create_user_screen, font="Any 12", title_color="black", size=(400, 500), key="create_user", visible=False, vertical_alignment='center', element_justification='c'))

window = sg.Window('Home', [log_in_screen], font=("Helvetica", 12), size=(1200, 750), element_justification='c')       

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "INPUT_goTo_create_user_btn":
        change_menu_create_user()
    elif event == "INPUT_cancel_user_btn":
        change_menu_log_in_user()
    elif event == "INPUT_log_in_btn":
        if values["INPUT_username"].strip() == "" or values["INPUT_password"].strip() == "":
            sg.popup("You need to enter a username and a password to Log in to you account")
        else:
            log_in_obj.take_username_and_password(values["INPUT_username"].strip(), values["INPUT_password"].strip())
            log_in_obj.check_username_password()
            if log_in_obj.valid_user == False:
                sg.popup("Incorrect username or password")
            elif log_in_obj.valid_user == True:
                session_user = log_in_obj.create_session_user()
                load_main_page(session_user, window)
            else:
                continue
    elif event == "INPUT_create_user_btn":
        if values["INPUT_new_username"].strip() == "" or values["INPUT_new_password"].strip() == ""  or values["INPUT_new_host"].strip() == "" or values["INPUT_new_database"].strip() == "":
            sg.popup("You need to enter all you details to create an account")
        else:
            create_user_obj = Loggin_sys.create_new_user_handler(values["INPUT_new_username"], values["INPUT_new_password"], values["INPUT_new_host"], values["INPUT_new_database"])
            create_user_obj.check_username()
            if create_user_obj.valid_user == False:
                sg.popup("Either usename or password do not match specifications or there is no connection / database under these details")
            else:
                session_user = create_user_obj.create_session_user()
                load_main_page(session_user, window)
    else:
        continue
    window.Refresh()
     

#Example Frame:
"""
def blank_frame():
    return sg.Frame("", [[]], pad=(5, 3), expand_x=True, expand_y=True, background_color='#404040', border_width=0)

sg.theme('DarkGrey4')

layout_frame1 = [
    [blank_frame(), blank_frame()],
    [sg.Frame("Frame 3", [[blank_frame()]], pad=(5, 3), expand_x=True, expand_y=True, title_location=sg.TITLE_LOCATION_TOP)],
]

layout_frame2 = [[blank_frame()]]

layout = [
    [sg.Frame("Frame 1", layout_frame1, size=(280, 250)),
     sg.Frame("Frame 2", layout_frame2, size=(200, 250), title_location=sg.TITLE_LOCATION_TOP)],]

window = sg.Window("Title", layout, margins=(2, 2), finalize=True)

while True:

    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

window.close()
""" 
