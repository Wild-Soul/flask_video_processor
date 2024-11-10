from typing import TypeVar, Generic, Type, Optional, List
from app.extensions import db

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.model.query.get(id)

    def get_all(self) -> List[T]:
        return self.model.query.all()

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        db.session.add(instance)
        return instance

    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    def delete(self, instance: T) -> None:
        db.session.delete(instance)

    def commit(self) -> None:
        db.session.commit()

    def rollback(self) -> None:
        db.session.rollback()
