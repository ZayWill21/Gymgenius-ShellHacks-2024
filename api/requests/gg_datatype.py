from enum import Enum
from ..presets import Presets

class gg_Datatype(Enum):
    conversation = 3
    text = 2
    table = 1
    null = 0

    @staticmethod
    def get_preset(inp):
        if inp == gg_Datatype.conversation:
            return Presets.get_conv_exaple()
        elif inp == gg_Datatype.text:
            return Presets.get_text_example()
        elif inp == gg_Datatype.table:
            return Presets.get_table_example()