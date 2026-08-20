import logging
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class NotificationService:
    """Firebase & local alert notification abstraction layer."""
    def __init__(self):
        self.firebase_active = False
        if settings.FIREBASE_CREDENTIALS_PATH:
            try:
                # Optional Firebase Admin SDK initialization if credentials path configured
                import firebase_admin
                from firebase_admin import credentials, messaging
                if not firebase_admin._apps:
                    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                    firebase_admin.initialize_app(cred)
                self.firebase_active = True
            except Exception as e:
                logger.warning(f"Firebase Admin SDK not initialized ({e}). Using local notification fallback.")
                self.firebase_active = False

    def send_alert(self, farmer_id: int, title: str, description: str, alert_type: str = "general") -> Dict[str, Any]:
        if self.firebase_active:
            try:
                from firebase_admin import messaging
                message = messaging.Message(
                    notification=messaging.Notification(title=title, body=description),
                    topic=f"farmer_{farmer_id}"
                )
                response = messaging.send(message)
                return {"status": "sent", "message_id": response, "channel": "Firebase FCM"}
            except Exception as e:
                logger.error(f"FCM send failed: {e}")

        # Local fallback event logging
        logger.info(f"[NOTIFICATION FALLBACK] Farmer {farmer_id} ({alert_type}): {title} - {description}")
        return {
            "status": "logged",
            "channel": "Local Development Event Log (Fallback)",
            "title": title,
            "description": description
        }

notification_service = NotificationService()
