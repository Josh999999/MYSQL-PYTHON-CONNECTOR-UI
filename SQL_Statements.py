###MYSQL-Python-User_Interface###:


##MYSQL-Connection-SQL-Statement##:


#The WHERE condition will be repeated in every single statement and therefore the complining function for it can be a seperate function:
SELECTION_statement_str_WHERE = "WHERE{}"

def compile_where_statement(where_attributes, where_condition, where_values, where_and_or):
    compiled_conditions = ''
    min_attribute = len(where_attributes)
    for i in range(min_attribute):
        cur_condition = ""
        cur_condition += where_attributes[i]
        if i < min_attribute - 1:
            cur_condition += ' ' + where_condition[i] + " '" + where_values[i] + "' " + where_and_or[i]
        else:
            cur_condition += ' ' + where_condition[i] + " '" + where_values[i] + "'"
        compiled_conditions += cur_condition
        
    WHERE_statement = SELECTION_statement_str_WHERE.format(" " + compiled_conditions)
    return WHERE_statement
    

#SELECTION statement#:
#Notes on writing the WHERE statement and ORDER BY statement#:
#When creaing the WHERE statement of the query, if there are two or more attributes in the form:
#   - (WHERE att1 AND att2 NOT NULL)
#att1 and att2 will be read into 1 slot in the array with a special charatcer '|' between them to denote the need for an
#'AND' or 'OR' statement
#Whereas when you have a statement like this:
#   - (WHERE att1 = 1 AND att2 = NONE)
#they will both be writen into sperate parts of the array
#Conditions and attributes for WHERE and ORDER BY will be written into a string in the order they are in inside of the array

#Attributes for order_by:
"""is_order, order_attributes, order_desc_asc"""


SELECTION_statement_str_SELECT_FROM = """SELECT {} FROM {}"""
SELECTION_statement_str_ORDER_BY = "ORDER BY {} {}"


def create_SELECT_statement(is_all, attributes, table, is_where, where_attributes, where_condition, where_values, where_and_or):
    #Compile SELECT_FROM section:
    print(attributes)
    print(*attributes)
    SELECT_FROM_statement = SELECTION_statement_str_SELECT_FROM.format(','.join(attributes), table)
    print(SELECT_FROM_statement)
    SELECT_statement = SELECT_FROM_statement

    #Compile WHERE section:
    if is_where:
        WHERE_statement = compile_where_statement(where_attributes, where_condition, where_values, where_and_or)
        SELECT_statement += ' ' + WHERE_statement

    """
    #Compile ORDER BY section:
    if is_order:
        ORDER_BY_statement = ''
        ORDER_BY_array = []
        for i in range(len(order_attributes)):
            cur_order = order_desc_asc[i]
            if not cur_order:
                cur_order = 'ASC'
            compiled_order = order_attributes, cur_order
            ORDER_BY_array.append(compiled_order)
        ORDER_BY_statement = SELECTION_statement_str_ORDER_BY.format(*ORDER_BY_array)
        SELECT_statement += ORDER_BY_statement
    """
    return SELECT_statement




#INSERTION statement#:

INSERTION_statement_str_attributes_table = "INSERT INTO {} ({})"
INSERTION_statement_str_values = "VALUES {}"


def create_INSERT_statement(attributes, table, values):
    #Compile attributes and table section:
    TABLES_COLUMNS_statement = INSERTION_statement_str_attributes_tables.format(table, attributes)

    #Compile values section:
    VALUES_statement = INSERTION_statement_str_values.format(values)
    INSERT_statement = TABLE_COLUMNS_statement, VALUES_statement
    return INSERT_statement




#UPDATE statement#:

UPDATE_statement_str_attributes_table = "UPDATE {} SET {}"
UPDATE_statement_str_WHERE = "WHERE {}"


def create_UPDATE_statement(table, attributes, values, is_where, where_attributes, where_condition, where_values, where_and_or):
    UPDATE_statement = ''

    #Compile attributes and table section:
    TABLES_COLUMNS_statement = UPDATE_statement_str_attributes_table.format(table, attributes)
    UPDATE_statement += TABLES_COLUMNS_statement

    #Compile WHERE section:
    if is_where:
        WHERE_statement = compile_where_statement(where_attributes, where_condition, where_values, where_and_or)
        UPDATE_statement += ' ' + WHERE_statement

    return UPDATE_statement




#DELETE statement#:   

DELETE_statement_str_table = "DELETE FROM {}"
DELETE_statement_str_WHERE = "WHERE {}"


def create_DELETE_statement(table, is_where, where_attributes, where_condition, where_values, where_and_or):
    DELETE_statement = ''

    #Compile table section:
    TABLE_statement = DELETE_statement_str_table.format(table)
    DELETE_statement += TABLE_statement

    #Compile WHERE section:
    if is_where:
        WHERE_statement = compile_where_statement(where_attributes, where_condition, where_values, where_and_or)
        DELETE_statement += WHERE_statement

    return DELETE_statement
