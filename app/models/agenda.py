from app.database.connection import Base
from sqlalchemy import Column, Integer, String, Enum
import enum


class PubliclyExposedPersons(str, enum.Enum):
    PRESIDENT = "presidente-da-republica"
    VICE_PRESIDENT = "vice-presidente"
    FIRST_LADY = "primeira-dama"
    


class Event(Base):
    __tablename__ = "events"

    _id = Column(Integer, primary_key=True, index=True)
    datetime = Column(String, index=True)
    href = Column(String, index=True)
    location = Column(String, index=True)
    start = Column(String, index=True)
    title = Column(String, index=True)
    
    
# Preciso criar uma tabela para os Parlamentares separado dos eventos, assim
# Eu consigo ter controle de qual evento pertence a qual parlamentar,
# e consigo fazer consultas mais eficientes ADICIONANDO O ENUM LÁ EM CIMA
