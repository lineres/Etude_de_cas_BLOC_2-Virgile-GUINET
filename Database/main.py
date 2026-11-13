
from database import engine, Base
from table import ObservationMeteo

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

print("Base de données et tables créées avec succès !")
