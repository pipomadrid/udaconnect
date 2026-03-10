from __future__ import annotations

from sqlalchemy import Column, Integer, String

from app import db


class Person(db.Model):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Person {self.id}: {self.first_name} {self.last_name}>"
