from crewai.tools import tool
import resend
import os
import json
from dotenv import load_dotenv
load_dotenv(override=True)

@tool("Enviar Email")
def enviar_email_tool(params_str: str) -> str:
    """Envia um email com a ata da reunião. Espera um JSON com 'destinatario' e 'caminho_ficheiro'."""
    try:
        params = json.loads(params_str)
        destinatario = params["destinatario"]
        caminho_ficheiro = params["caminho_ficheiro"]

        resend.api_key = os.getenv('RESEND_API_KEY')

        f: bytes = open(
        os.path.join(os.path.dirname(__file__), caminho_ficheiro), "rb"
        ).read()

        attachment: resend.Attachment = {"content": list(f), "filename": "ata_reuniao.txt"}

        email_params = {
            "from": "MeetDocAI <onboarding@resend.dev>",
            "to": [destinatario],
            "subject": "Ata da Reunião",
            "html": "<p>Segue em anexo a ata da reunião.</p>",
            "attachments": [attachment],
        }

        resend.Emails.send(email_params)
        return f"📬 Email enviado com sucesso para {destinatario}."

    except Exception as e:
        return f"❌ Falha ao enviar email: {str(e)}"
