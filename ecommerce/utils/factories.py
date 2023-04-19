from factory import RelatedFactoryList


class RelatedFactoryVariableList(RelatedFactoryList):
    """
    Allows overriding ``size`` during factory usage,
    e.g. ParentFactory(list_factory__size=4)
    """

    def call(self, instance, step, context):
        size = context.extra.pop("size", self.size)
        assert isinstance(size, int)
        return [
            super(RelatedFactoryList, self).call(instance, step, context)
            for i in range(size)
        ]
