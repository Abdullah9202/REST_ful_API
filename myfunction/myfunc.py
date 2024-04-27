def to_dict(self):
    # Using Dict Comp
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}
