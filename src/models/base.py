"""Base classes and utilities for models to inherit or use"""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import MetaData


class CustomBaseQuery(BaseQuery):
    def only_not_deleted(self):
        return self.filter_by(is_deleted=False)


metadata = MetaData()
db = SQLAlchemy(metadata=metadata, query_class=CustomBaseQuery)
migrate = Migrate()
