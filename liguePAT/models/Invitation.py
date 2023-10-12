from database.mongoDB import connection
from bson.objectid import ObjectId, InvalidId
from twilio.rest import Client

db = connection()


class Invitation:
    def __init__(self, player_id, token, status):
        self.player_id = player_id
        self.token = token
        self.status = status  # Par exemple : "envoyé", "accepté", "expiré"

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "token": self.token,
            "status": self.status
        }
    
    def from_dict(self, invitation_dict):
        return {
            "player_id": invitation_dict["player_id"],
            "token": invitation_dict["token"],
            "status": invitation_dict["status"]
        }
    
    def create(self):
        try:
            db.invitations.insert_one(self.to_dict())
            return True
        except Exception as e:
            print(e)
            return False
        
    def find_one(self, invitation_id):
        try:
            invitation = db.invitations.find_one({"_id": invitation_id})
            if invitation:
                invitation = invitation.from_dict(invitation)
                return invitation
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    def find_all(self):
        try:
            invitations = db.invitations.find()
            if invitations:
                invitations = [invitation.from_dict(invitation) for invitation in invitations]
                return invitations
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    def update(self, invitation_id):
        try:
            db.invitations.update_one({"_id": invitation_id}, {"$set": self.to_dict()})
            return True
        except Exception as e:
            print(e)
            return False
        
    def delete(self, invitation_id):
        try:
            db.invitations.delete_one({"_id": invitation_id})
            return True
        except Exception as e:
            print(e)
            return False
    
    def check_state(self, invitation_id):
        try:
            invitation = db.invitations.find_one({"_id": invitation_id})
            if invitation:
                return invitation["status"]
            else:
                return None
        except Exception as e:
            print(e)
            return None
    
    def send_by_sms(self, phone, mot2pass, token):
        account_sid = 'ACff28aa0dd26c23d51908ee5f61c77076'
        auth_token = '686284b657c87e76380cee9b30d42afe'
        my_twilio_phone = '+16187624352'
        client = Client(account_sid, auth_token)

        body = f"""Bonjour,

        Vous avez été invité à rejoindre le jeu.

        Votre mot de passe est : {mot2pass}

        Votre token est : {token}

        Cordialement,
        L'équipe du jeu"""

        if self:
            twilio_format_phone = "+1" + phone
            try:
                message = client.messages.create(
                    body=body,
                    from_=my_twilio_phone,
                    to=twilio_format_phone
                )

                db.invitations.update_one({"_id": self._id}, {"$set": {"status": "envoyé"}})
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
        
        
            
