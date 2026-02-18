from typing import ClassVar


class AppState:
    tools: ClassVar[list] = []
    tools_loaded: ClassVar[bool] = False


state = AppState()
