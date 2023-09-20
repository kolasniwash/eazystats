import abc
import model


from sqlalchemy.sql import select

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, game: model.Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, game_id) -> model.Game:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, game):
        self.session.add(game)

    def get(self, game_id):
        return self.session.query(model.Game).filter_by(game_id=game_id).one()

    def list(self):
        return self.session.scalars(select(model.Game)).all()
