from db_connector import *
import random
import time


def create_age_groupe():
    start = random.randint(0, 9) * 10
    end = start + 10
    return f"{start}-{end}"


def create_personal_data():
    personal_data = "place_holder"
    return personal_data


def create_patient_mysql():

    # inserting into patients table
    insert_query = """
        INSERT INTO patients (age_group,encrypted_info) VALUES (%s, %s)
    """
    values = (create_age_groupe(), create_personal_data())
    db = get_db()
    cursor = db.cursor()
    cursor.execute(insert_query, values)
    db.commit()
    cursor.close()
    db.close()


def insert_data_for_patient(id: int):

    heart_rate = random.randint(60, 100)  # Battements par minute

    oxygen_saturation = round(random.uniform(95.0, 100.0), 2)  # % de saturation
    fev1 = round(random.uniform(2.0, 4.5), 2)
    fvc = round(random.uniform(fev1, fev1 + 1.0), 2)

    timestamp = ""

    insert_query = """
        INSERT INTO measurements    (patient_id, 
                                    timestamp, 
                                    blood_pressure, 
                                    heart_rate, 
                                    oxygen_saturation, 
                                    fev1, fvc) 
        VALUES (%s, %s, %s, %s, %s, %s,%s)
    """

    values = (id, timestamp, heart_rate, oxygen_saturation, fev1, fvc)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(insert_query, values)
    db.commit()
    cursor.close()
    db.close()


def fetch_latest_measurements():
    db = get_db()
    cursor = db.cursor(dictionary=True)  # Return rows as dictionaries

    query = "SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 10"
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    db.close()
    return results


def index_measurements_to_elasticsearch(es_client, index_name="medical_data"):
    measurements = fetch_latest_measurements()

    for measurement in measurements:
        doc_id = measurement["measurement_id"]  # Optional: use MySQL ID
        es_client.index(index=index_name, id=doc_id, document=measurement)


if __name__ == "__main__":

    # load the password from the env
    password = os.getenv("PASSWORD")
    print("Password is:", password)
    es_client = get_elastic_client(password)
    index_name = "medical_data"

    # insert data in mysql
    create_patient_mysql()
    insert_data_for_patient(1)

    # update data to elastic search
    if not es_client.indices.exists(index="medical_data"):
        es_client.indices.create(index="medical_data")

    index_measurements_to_elasticsearch(es_client)
    print("Synced latest measurements.")
    time.sleep(60)  # Wait 60 seconds
