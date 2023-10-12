from bson.objectid import ObjectId

from database.mongoDB import connection

from models.Team import Team
from models.Player import Player
from models.StatsTeam import StatsTeam
from models.StatsPlayer import StatsPlayer

db = connection()

def create():
    team_id = Team.find_one_by_name("Canadiens")._id
    print(team_id)
    player1 = Player(team_id=team_id,
                     email="olivier@gmail.com",
                     password="123",
                     first_name="Olivier",
                     last_name="Marandola",
                     age= 7, 
                     number = 11, 
                     phone = "5142148292", 
                     position = "Center",
                     photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player1.create()

    player2 = Player(team_id=team_id,
                        email="gab@gmail.com",
                        password="123",
                        first_name="Gab",
                        last_name="Levesque",
                        age= 7,
                        number = 12,
                        phone = "5142148292",
                        position = "Center",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player2.create()

    player3 = Player(team_id=team_id,
                        email="yaniko@gmail.com",
                        password="123",
                        first_name="Yaniko",
                        last_name="Boucher",
                        age= 7,
                        number = 13,
                        phone = "5142148292",
                        position = "Center",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player3.create()

    player4 = Player(team_id=team_id,
                        email="hazard@gmail.com",
                        password="123",
                        first_name="Hazard",
                        last_name="coudon",
                        age= 7,
                        number = 14,
                        phone = "5142148292",
                        position = "Center",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player4.create()

    player5 = Player(team_id=team_id,
                        email="yan@gmail.com",
                        password="123",
                        first_name="Yan",
                        last_name="cooper",
                        age= 7,
                        number = 15,
                        phone = "5142148292",
                        position = "Left wing",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player5.create()

    player6 = Player(team_id=team_id,
                        email="crosby@gmail.com",
                        password="123",
                        first_name="Sdney",
                        last_name="Crosby",
                        age= 7,
                        number = 16,
                        phone = "5142148292",
                        position = "Left wing",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player6.create()

def find_one():
    player_id = "64f3aaab7b8f47f97ec5935b"
    player_id = ObjectId(player_id)
    player = Player.find_one(player_id).to_dict()
    print(player)

def find_one_by_email():
    player_email = "olivier@gmail.com"
    player = Player.find_one_by_email(player_email)
    print(player)


def find_one_by_number():
    player_number = 11
    player = Player.find_one_by_number(player_number).to_dict()
    print(player)

def find_all():
    players = Player.find_all()
    if players:
        for player in players:
            print(player.to_dict())
    else:
        print("No player found")


def update():
    player_id = "64f3aaab7b8f47f97ec5935b"
    player_id = ObjectId(player_id)
    team_id = Team.find_one_by_name("Canadiens")._id
    team_id = ObjectId(team_id)
    player_updated_try = Player.find_one(player_id)
    player_updated_try.first_name = "Olivier"
    player_updated = Player(team_id=team_id,
                            email="patate@gmail.com",
                            password="123",
                            first_name="Patate",
                            last_name="Giroux",
                            age= 7,
                            number = 11,
                            phone = "5142148292",
                            position = "Center",
                            photo_url = "media/images_joueurs/DVJL3683.JPG",
                            )
    print(player_updated_try.update(player_id))


def delete():
    player_id = "64f3aaac7b8f47f97ec59360"
    player_id = ObjectId(player_id)
    Player.delete(player_id)


def increment_stats():
    player_id = "64f3aaab7b8f47f97ec5935b" 
    player_id = ObjectId(player_id)
    player = Player.find_one(player_id)

    if player is not None:
        result = player.update_player_stats("increment_player", "goals" ) 
        print(f"Update Stats Result: {result}")
    else:
        print("Player not found.")




#create()
#find_one()
#find_one_by_email()
#find_one_by_number()
#find_all()
#update()
#delete()

increment_stats()