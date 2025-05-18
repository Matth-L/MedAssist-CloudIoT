from elastic_connector import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email_to_mailhog(body):
    # Configuration du serveur SMTP MailHog
    smtp_server = "mailhog-service"
    smtp_port = 1025
    sender_email = "sender@example.com"
    receiver_email = "receiver@example.com"

    # Créer un message MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Etat de santé inquiétant "

    try:
        logger.info("attaching message")
        logger.info(len(body))
        message.attach(MIMEText(body, "plain"))
    except Exception as e:
        print(f"Error attaching message: {e}")

    try:
        # Connexion au serveur SMTP MailHog
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            logger.info("tentative de connexion")
            server.sendmail(sender_email, receiver_email, message.as_string())
            logger.info("E-mail envoyé avec succès à MailHog!")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'e-mail: {e}")


def fetch_from_elasticsearch(es_client, index_name="medical_data", size=10):
    """
    Récupère les derniers documents de l'index Elasticsearch.

    :param es_client: Le client Elasticsearch (déjà connecté)
    :param index_name: Le nom de l'index à interroger
    :param size: Le nombre de documents à récupérer
    :return: Liste de documents Elasticsearch
    """
    try:
        response = es_client.search(
            index=index_name,
            size=size,
            sort="timestamp:desc",  # tri décroissant par date
            query={"match_all": {}},
        )
        hits = response.get("hits", {}).get("hits", [])
        results = [hit["_source"] for hit in hits]
        return results
    except NotFoundError:
        logger.error(f"L'index '{index_name}' n'existe pas.")
        return []
    except Exception as e:
        logger.error(f"Erreur lors de la récupération depuis Elasticsearch : {e}")
        return []


def measure_test(val):
    tension = False
    heart_rate = False
    oxygen_saturation = False
    fev1 = False
    fvc = False

    logger.info(val)
    for dict in val:
        if "tension" in dict:
            if dict["tension"] > 1:
                tension = True

        if "heart_rate" in dict:
            if dict["heart_rate"] < 60 or dict["heart_rate"] > 100:
                heart_rate = True

        if "oxygen_saturation" in dict:
            if dict["oxygen_saturation"] < 95.0:
                oxygen_saturation = True

        if "fev1" in dict:
            if dict["fev1"] < 2.0:
                fev1 = True

        if "fvc" in dict:
            if dict["fvc"] < 3.0:
                fvc = True

    return {
        "patient_id": dict["patient_id"],
        "tension": tension,
        "heart_rate": heart_rate,
        "oxygen_saturation": oxygen_saturation,
        "fev1": fev1,
        "fvc": fvc,
    }


def create_body(test_results):
    alert_message = f"Alerte patient {test_results.get('patient_id')} \n\n"
    alert_triggered = False  # Variable pour vérifier si une alerte a été déclenchée

    if test_results["tension"]:
        alert_message += "  - Tension artérielle élevée (supérieure à 110)\n"
        alert_triggered = True
    if test_results["heart_rate"]:
        alert_message += (
            "  - Fréquence cardiaque hors norme (inférieure à 60 ou supérieure à 100)\n"
        )
        alert_triggered = True
    if test_results["oxygen_saturation"]:
        alert_message += "  - Saturation en oxygène inférieure à 95%\n"
        alert_triggered = True
    if test_results["fev1"]:
        alert_message += (
            "  - FEV1 inférieur à 2.0 (Volume expiratoire maximal en 1 seconde)\n"
        )
        alert_triggered = True
    if test_results["fvc"]:
        alert_message += "  - FVC inférieur à 3.0 (Capacité vitale forcée)\n"
        alert_triggered = True

    alert_message += "\n"

    # Vérifier s'il y a des alertes, sinon ajouter un message sans problème
    if not alert_triggered:
        alert_message = "Aucune alerte : Toutes les mesures sont normales.\n"

    return alert_message


if __name__ == "__main__":

    # load the password from the env
    password = os.getenv("PASSWORD")
    es_client = get_elastic_client(password)
    index_name = "medical_data"

    while True:
        latest_data = fetch_from_elasticsearch(es_client, size=5)
        mail_content = create_body(measure_test(latest_data))
        if "Alerte" in mail_content:  # Si l'alerte est déclenchée
            send_email_to_mailhog(mail_content)
            logger.info("Mail envoyé avec alerte")
        else:
            logger.info("Aucune alerte, pas d'envoi de mail")
        sleep(60)
