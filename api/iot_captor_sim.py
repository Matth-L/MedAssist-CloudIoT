from db_connector import *
import random


def create_age_groupe():
    start = random.randint(0, 9) * 10
    end = start + 10
    return f"{start}-{end}"

def create_personal_data():
    return NULL 

def create_patient_mysql():
    db = get_db()
    cursor = db.cursor()
    
    # inserting into patients table
    insert_query = """
        INSERT INTO patients (age_group,encrypted_info) VALUES (%s, %s)
    """
    values = (create_age_groupe(), create_personal_data())    
    cursor.execute(insert_query, values)
    db.commit()
    cursor.close()
    db.close()
