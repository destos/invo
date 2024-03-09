from items.models.item_types import Item


class OperationHolderMixin:
    def __and__(self, other):
        return OperandHolder(AND, self, other)

    def __or__(self, other):
        return OperandHolder(OR, self, other)

    def __rand__(self, other):
        return OperandHolder(AND, other, self)

    def __ror__(self, other):
        return OperandHolder(OR, other, self)

    def __invert__(self):
        return SingleOperandHolder(NOT, self)


class SingleOperandHolder(OperationHolderMixin):
    def __init__(self, operator_class, op1_class):
        self.operator_class = operator_class
        self.op1_class = op1_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        return self.operator_class(op1)


class OperandHolder(OperationHolderMixin):
    def __init__(self, operator_class, op1_class, op2_class):
        self.operator_class = operator_class
        self.op1_class = op1_class
        self.op2_class = op2_class

    def __call__(self, *args, **kwargs):
        op1 = self.op1_class(*args, **kwargs)
        op2 = self.op2_class(*args, **kwargs)
        return self.operator_class(op1, op2)


class AND:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_condition(self, situ):
        return self.op1.has_condition(situ) and self.op2.has_condition(situ)

    def has_object_condition(self, situ, obj):
        return self.op1.has_object_condition(situ, obj) and self.op2.has_object_condition(
            situ, obj
        )


class OR:
    def __init__(self, op1, op2):
        self.op1 = op1
        self.op2 = op2

    def has_condition(self, situ):
        return self.op1.has_condition(situ) or self.op2.has_condition(situ)

    def has_object_condition(self, situ, obj):
        return self.op1.has_object_condition(situ, obj) or self.op2.has_object_condition(situ, obj)


class NOT:
    def __init__(self, op1):
        self.op1 = op1

    def has_condition(self, situ):
        return not self.op1.has_condition(situ)

    def has_object_condition(self, situ, obj):
        return not self.op1.has_object_condition(situ, obj)


class BaseConditionMetaclass(OperationHolderMixin, type):
    pass


class BaseCondition(metaclass=BaseConditionMetaclass):
    def has_condition(self, situ):
        """
        Return `True` if condition is granted, `False` otherwise.
        """
        return True

    def has_object_condition(self, situ, obj):
        """
        Return `True` if condition is granted, `False` otherwise.
        """
        return True


class OneSpaceSelected(BaseCondition):
    def has_condition(self, situ):
        "Only one space has been selected"
        return situ.spaces.count() == 1


class TwoSpacesSelected(BaseCondition):
    def has_condition(self, situ):
        "Exactly two spaces have been selected"
        return situ.spaces.count() == 2


class OnlySpacesSelected(BaseCondition):
    def has_condition(self, situ):
        "Spaces have been selected but not items"
        return situ.spaces.exists() and not situ.items.exists()


class OnlyItemsSelected(BaseCondition):
    def has_condition(self, situ):
        "Both spaces and items are present"
        return not situ.spaces.exists() and situ.items.exists()


class SpaceSelected(BaseCondition):
    def has_condition(self, situ):
        "Any amount of spaces exist on situation"
        return situ.spaces.exists()


class SelectedItemInSpace(SpaceSelected):
    def has_object_condition(self, situ, object):
        "The selected item exist in selected spaces"
        if isinstance(object, Item):
            # TODO: do we need to check if we have selected spaces in the object condition?
            return situ.spaces.filter(items__in=[object]).exists()
        return True


class ItemsSelected(BaseCondition):
    def has_condition(self, situ):
        "Any amount of items exist on situation"
        return situ.items.exists()


class ItemsInSameSpace(ItemsSelected):
    def has_condition(self, situ):
        "Items are selected and they are all in the same space"
        return super().has_condition(situ) and situ.items.distinct("space").count() == 1
