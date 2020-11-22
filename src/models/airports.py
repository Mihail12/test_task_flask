from src.models.base import db
from src.models.utils import get_object_or_404


__all__ = (
    'Airport',
)


# In future the part of the model such city and country, could be another Models
# The same with type and source
class Airport(db.Model):
    """Model class to represent Airport"""

    __tablename__ = "airport"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    iata = db.Column(db.String(255))
    icao = db.Column(db.String(255))
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    altitude = db.Column(db.String(255))

    timezone = db.Column(db.String(50))
    dst = db.Column(db.String(50))
    tz = db.Column(db.String(50))
    type = db.Column(db.String(50))
    source = db.Column(db.String(50))

    is_deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def from_upload(cls, data):
        return cls(**data)

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.name})>"
        )

    def update_current_object(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    @classmethod
    def update(cls, data, sid):
        airport = get_object_or_404(cls.query.only_not_deleted().with_for_update(), sid)
        airport.update_current_object(data)
        return airport

    @classmethod
    def delete(cls, sid):
        airport = get_object_or_404(cls.query.only_not_deleted().with_for_update(), sid)
        airport.is_deleted = True
        db.session.commit()

    @classmethod
    def create(cls, data):
        airport = Airport(**data)
        db.session.add(airport)
        db.session.commit()
        return airport
