# import sqlite3

def Add_to_Db(Entity_dict,user_id,cursor,connection):
    #using user id to check if user exists in db
    select_query = '''
        SELECT * FROM users
        WHERE user_id = ?;
    '''
    cursor.execute(select_query, (user_id,))
    existing_user = cursor.fetchone()
    #If the user is an existing user update his null columns with available data without overwriting the previous data
    if existing_user:
      update_query = f'''
          UPDATE users
          SET
              username = CASE WHEN username IS NULL THEN ? ELSE username END,
              email = CASE WHEN email IS NULL THEN ? ELSE email END,
              phone_number = CASE WHEN phone_number IS NULL THEN ? ELSE phone_number END
          WHERE user_id = ?;
      '''
      username = None if len(Entity_dict.get('PERSON', ""))==0 else Entity_dict.get('PERSON', "")[0]
      email = None if len(Entity_dict.get('EMAIL', ""))==0 else Entity_dict.get('EMAIL', "")[0]
      phone_number = None if len(Entity_dict.get('PHONE_NUMBER', ""))==0 else Entity_dict.get('PHONE_NUMBER', "")[0]
      update_data = (username, email,phone_number, user_id)
      cursor.execute(update_query, update_data)
      connection.commit()
      print("UPDATE COMPLETED")
      print(update_data)
    else:
        #if the user is a new user add his available data from Named entities
        username = None if len(Entity_dict.get('PERSON', ""))==0 else Entity_dict.get('PERSON', "")[0]
        email = None if len(Entity_dict.get('EMAIL', ""))==0 else Entity_dict.get('EMAIL', "")[0]
        phone_number = None if len(Entity_dict.get('PHONE_NUMBER', ""))==0 else Entity_dict.get('PHONE_NUMBER', "")[0]
        new_user_data = (user_id, username, email, phone_number)
        print(new_user_data)
        insert_query = '''
            INSERT OR REPLACE INTO users (user_id, username, email, phone_number)
            VALUES (?, ?, ?, ?);
        '''

        cursor.execute(insert_query, new_user_data)
        connection.commit()

        print("User with user_id "+ str(new_user_data[0])+"  been added to the 'users' table.")



def Update_Username_if_Dummy(user_id, new_username,cursor,connection):

    # Update the username in the table if dummy condition satisfies
    update_query = f"UPDATE users SET username = ? WHERE user_id = ?"
    cursor.execute(update_query, (new_username, user_id))

    # Commit the changes
    connection.commit()

    print(f"Username for user ID {user_id} updated successfully.")