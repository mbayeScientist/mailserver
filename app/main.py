from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .email import send_email
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Définir un modèle Pydantic pour valider les données du formulaire
class ContactForm(BaseModel):
    name: str
    email: str
    message: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000" , "https://mailserver-vqz2.onrender.com"],  # Permet toutes les origines (en développement, vous pouvez spécifier 'http://localhost:3000')
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes
)

@app.post("/send-email/")
async def send_contact_email(form: ContactForm):
    try:
        # Appeler la fonction d'envoi d'email
        send_email(form.name, form.email, form.message)
        return {"message": "Email sent successfully!"}
    except HTTPException as e:
        raise e
