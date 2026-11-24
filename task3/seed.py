from database import SessionLocal, Base, engine
import models

Base.metadata.create_all(bind=engine)

db = SessionLocal()
if not db.query(models.Master).first():
    db.add_all([
        models.Master(name="Анна", specialization="Парикмахер"),
        models.Master(name="Мария", specialization="Визажист"),
    ])
    db.commit()
db.close()
print("Seed done")