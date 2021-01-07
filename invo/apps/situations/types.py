from ariadne import EnumType, ObjectType

from .models import Situation


situation_state = EnumType("SituationState", Situation.States)
situation_edit = EnumType("SituationExit", Situation.Exit)

situation = ObjectType("Situation")
