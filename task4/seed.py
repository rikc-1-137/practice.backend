from database import Base, SessionLocal, engine
import models

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if not db.query(models.Category).first():
    db.add_all([
        models.Category(name="Стрижки и укладки"),
        models.Category(name="Маникюр и педикюр"),
        models.Category(name="Брови и ресницы"),
        models.Category(name="Спа-процедуры"),
    ])

if not db.query(models.Master).first():
    db.add_all([
        models.Master(name="Анна", specialization="Парикмахер"),
        models.Master(name="Мария", specialization="Визажист"),
    ])

db.commit()
db.close()
print("Seed done")