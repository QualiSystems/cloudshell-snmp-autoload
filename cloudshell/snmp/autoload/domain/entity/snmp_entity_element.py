import functools


class Element(object):
    def __init__(self, entity):
        """Initialize Element.

        :type entity: object
        """
        self.entity = entity
        self.id = entity.position_id
        self.child_list = []
        self.parent = None
        self._full_id = ""

    def add_parent(self, parent):
        self.parent = parent
        parent.child_list.append(self)

    @property
    @functools.lru_cache()
    def full_id(self):
        if not self.parent:
            return self.id
        return f"{self.parent.full_id}/{self.id}"


class PortElement(Element):
    def __init__(self, entity, if_entity):
        super(PortElement, self).__init__(entity)
        self.if_entity = if_entity
