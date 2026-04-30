from modules.database import engine, Base
import modules.models

print("Checking and updating database tables...")
Base.metadata.create_all(bind=engine, checkfirst=True)
print("Done! All tables are up to date.")