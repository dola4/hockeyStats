from database.mongoDB import connection
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from .Team import Team
from .StatsGoaler import StatsGoaler
from .StatsPlayer import StatsPlayer


db = connection()

class Player:
    def __init__(self, team_id, email, password, first_name, last_name, age, number, phone, position, photo_url, _id=None):
        self.team_id = team_id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.number = number
        self.phone = phone
        self.position = position
        self.photo_url = photo_url
        self.stats_player = StatsPlayer()
        self.stats_goaler = StatsGoaler()
        self._id = _id
    
    def to_dict(self):
        return {
            "team_id": ObjectId(self.team_id),
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "number": self.number,
            "phone": self.phone,
            "position": self.position,
            "photo_url": self.photo_url,
            "stats_player": self.stats_player.__dict__ if self.stats_player else None,
            "stats_goaler": self.stats_goaler.__dict__ if self.stats_goaler else None
        }
    
    def from_dict(self, player_dict):
        self.team_id = player_dict["team_id"]
        self.email = player_dict["email"]
        self.password = player_dict["password"]
        self.first_name = player_dict["first_name"]
        self.last_name = player_dict["last_name"]
        self.age = player_dict["age"]
        self.number = player_dict["number"]
        self.phone = player_dict["phone"]
        self.position = player_dict["position"]
        self.photo_url = player_dict["photo_url"]
        self.stats_player = StatsPlayer().from_dict(player_dict["stats_player"])
        self.stats_goaler = StatsGoaler().from_dict(player_dict["stats_goaler"])
        return self
    
    def create(self):
        try:
            #if Player.find_one_by_email(self.email) != None:
             #   return "Player already exists"
            #else:
            self.password = generate_password_hash(self.password)
            inserted = db.players.insert_one(self.to_dict())
            self._id = str(inserted.inserted_id)
            print(inserted)
            return True
        
        except Exception as e:
            print(e)
            return False

    
    @classmethod
    def find_one(cls, player_id):
        try:
            player_data = db.players.find_one({"_id": ObjectId(player_id)})
            if player_data:
                player = cls(_id=str(player_data['_id']), team_id=player_data['team_id'], email=player_data['email'], password=player_data['password'], first_name=player_data['first_name'], last_name=player_data['last_name'], age=player_data['age'], number=player_data['number'], phone=player_data['phone'], position=player_data['position'], photo_url=player_data['photo_url'])
                player.stats_player.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler.from_dict(player_data.get("stats_goaler", {}))
                return player
            else:
                return "Player not found"
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_one_by_email(cls, email):
        try:
            player_data = db.players.find_one({"email": email})
            print(f"player_data : {player_data}")
            if player_data:
                player = cls(_id=str(player_data['_id']), team_id=player_data['team_id'], email=player_data['email'], password=player_data['password'], first_name=player_data['first_name'], last_name=player_data['last_name'], age=player_data['age'], number=player_data['number'], phone=player_data['phone'], position=player_data['position'], photo_url=player_data['photo_url'])
                player.stats_player.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler.from_dict(player_data.get("stats_goaler", {}))
                return player
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    @classmethod
    def find_one_by_number(cls, number):
        try:
            player_data = db.players.find_one({"number": number})
            if player_data:
                player = cls(_id=str(player_data['_id']), team_id=player_data['team_id'], email=player_data['email'], password=player_data['password'], first_name=player_data['first_name'], last_name=player_data['last_name'], age=player_data['age'], number=player_data['number'], phone=player_data['phone'], position=player_data['position'], photo_url=player_data['photo_url'])
                player.stats_player.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler.from_dict(player_data.get("stats_goaler", {}))
                return player
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    @classmethod
    def find_all(cls):
        try:
            players = []
            cursor = db.players.find()
            print(cursor)
            for player_data in cursor:
                player = cls(_id=str(player_data['_id']), team_id=player_data['team_id'], email=player_data['email'], password=player_data['password'], first_name=player_data['first_name'], last_name=player_data['last_name'], age=player_data['age'], number=player_data['number'], phone=player_data['phone'], position=player_data['position'], photo_url=player_data['photo_url'])
                player.stats_player.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler.from_dict(player_data.get("stats_goaler", {}))
                players.append(player)
            
            if len(players) == 0:
                return "No players found"
            
            return players
        except Exception as e:
            print(e)
            return None
        
    def update(self, player_id):
        try:
            existing_player = db.players.find_one({"_id": ObjectId(player_id)})
            print(f'existing_player : {existing_player}')
            if existing_player:
                if not check_password_hash(existing_player["password"], self.password):
                    self.password = generate_password_hash(self.password)
            db.players.update_one({"_id": ObjectId(player_id)}, {"$set": {"team_id": self.team_id, "email": self.email, "password": self.password, "first_name": self.first_name, "last_name": self.last_name, "age": self.age, "number": self.number, "phone": self.phone, "position": self.position, "photo_url": self.photo_url}})
            return True
        except Exception as e:
            print(e)
            return False
        
    @classmethod
    def delete(cls, player_id):
        try:
            db.players.delete_one({"_id": ObjectId(player_id)})
            return True
        except Exception as e:
            print(e)
            return False
    
    def increment_player_stat(self, stat_type):
        self.stats_player.increment_stat(stat_type)
    
    def decrement_player_stat(self, stat_type):
        self.stats_player.decrement_stat(stat_type)

    def increment_goaler_stat(self, stat_type):
        self.stats_goaler.increment_stat(stat_type)
    
    def decrement_goaler_stat(self, stat_type):
        self.stats_goaler.decrement_stat(stat_type)
    
    def update_player_stats(self, operation, stat_type):
        try:
            if operation == "increment_player":
                self.increment_player_stat(stat_type)
            elif operation == "decrement_player":
                self.decrement_player_stat(stat_type)
            elif operation == "increment_goaler":
                self.increment_goaler_stat(stat_type)
            elif operation == "decrement_goaler":
                self.decrement_goaler_stat(stat_type)
            
            if self._id:
                updated_player = db.players.find_one_and_update(
                    {'_id': self._id},
                    {'$inc': {f'stats.{stat_type}': 1}},
                    return_document=ReturnDocument.AFTER
    )
                # db.players.find_one_and_update({"_id": ObjectId(self._id)}, {"$set": {"stats_player": self.stats_player.__dict__, "stats_goaler": self.stats_goaler.__dict__}})
                return True
            else:
                return "Player not found"
        except Exception as e:
            print(e)
            return False
        

    

        

        