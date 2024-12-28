import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def send_email(name: str, email: str, message: str):
    # Configurer les informations d'authentification
    gmail_user = os.getenv('GMAIL_USER')
    gmail_pass = os.getenv('GMAIL_PASS')

    # Créer le message MIME
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = "alioumbayang99@gmail.com"  # L'adresse de destination
    msg['Subject'] = f"Message from {name}"

    # Corps du message
    body = f"From: {email}\n\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Se connecter au serveur SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_pass)

        # Envoyer le message
        server.sendmail(gmail_user, "alioumbayang99@gmail.com", msg.as_string())
        server.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
