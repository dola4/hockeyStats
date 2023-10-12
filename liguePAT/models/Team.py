from bson.objectid import ObjectId


from database.mongoDB import connection
from .StatsTeam import StatsTeam


db = connection()

class Team:
    def __init__(self, name, _id = None):
        self._id = _id
        self.name = name
        self.stats_team = StatsTeam()


    def to_dict(self):
        return {
            "name": self.name,
            "stats_team": self.stats_team.to_dict()
        }
    

    def from_dict(self, team_dict):
        self.name = team_dict["name"]
        self.stats_team = StatsTeam().from_dict(team_dict["stats_team"])
        self._id = team_dict.get("_id", None)
        return self
    

    def create(self):
        try:
            if Team.find_one_by_name(self.name) != None :
                return "Team already exists"
            else:
                inserted = db.teams.insert_one(self.to_dict())
                self._id = str(inserted.inserted_id)
                print(inserted)
                return True
        except Exception as e:
            print(e)
            return False
    

    @classmethod
    def find_one(cls, team_id):
        try:
            team_data = db.teams.find_one({"_id": ObjectId(team_id)})
            if team_data:
                team = cls(_id=str(team_data['_id']), name=team_data['name'])
                team.stats_team.from_dict(team_data.get("stats_team", {}))
                return team
            else:
                return "Team not found"
        except Exception as e:
            print(e)
            return None
        
    
    @classmethod
    def find_one_by_name(cls, name):
        try:
            team_data = db.teams.find_one({"name": name})
            if team_data:
                team = cls(_id=str(team_data['_id']), name=team_data['name'])
                team.stats_team.from_dict(team_data.get("stats_team", {}))
                return team
            else:
                return None
        except Exception as e:
            print(e)
            return None
    
    
    @classmethod
    def find_all(cls):
        try:
            teams = []
            cursor = db.teams.find()
        
            for team_data in cursor:
                team = cls(_id=str(team_data['_id']), name=team_data['name'])
                team.stats_team.from_dict(team_data.get("stats_team", {}))
                teams.append(team)

            if len(teams) == 0:
                return "No teams found"

            return teams
        except Exception as e:
            print(e)
            return None

    
    def update(self, team_id):
        try:
            existing_team = db.teams.find_one({"_id": ObjectId(team_id)})
            if existing_team:
                db.teams.update_one({"_id": ObjectId(team_id)}, {"$set": {"name": self.name}})
                return True
            else:
                return "Team not found"
        except Exception as e:
            print(e)
            return False
        
    @classmethod
    def delete(cls, team_id):
        try:
            db.teams.delete_one({"_id": ObjectId(team_id)})
            return True
        except Exception as e:
            print(e)
            return False
        
    def increment_stat(self, stat_type):
        self.stats_team.increment_stat(stat_type)

    def decrement_stat(self, stat_type):
        self.stats_team.decrement_stat(stat_type)
    
    def update_stats(self, stat_type, operation):
        try:
            if operation == "increment":
                self.increment_stat(stat_type)
            elif operation == "decrement":
                self.decrement_stat(stat_type)
            else:
                return "Invalid operation"

            # Mettez à jour la base de données avec les nouvelles statistiques
            if self._id:
                updated_stats = {"stats_team": self.stats_team.to_dict()}
                db.teams.update_one({"_id": ObjectId(self._id)}, {"$set": updated_stats})
                return True
            else:
                return "Team ID not found"
        except Exception as e:
            print(e)
            return False
    
