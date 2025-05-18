from enum import Enum, auto
from escalator_simulator.domain.models.person import Person

class SheetState(Enum):
    EMPTY = auto
    FULL = auto

class Escalator:
    def __init__(
        self,
        length=20,
        lane_count=2,
        velocity=1.0,
        on_person_enter: callable = None,
        on_person_exit: callable = None,
    ):
        self.length: float = length
        self.lane_count: float = lane_count
        self.velocity: float = velocity
        self.sheet = self._make_sheet()
        self.on_person_enter = on_person_enter
        self.on_person_exit = on_person_exit
        assert len(self.sheet) == lane_count

    def _make_sheet(self) -> list[list[Person | None]]:
        sheet = []
        for i in range(self.lane_count):
            sheet.append([None] * self.length)
        return sheet

    def get_enter_state(self) -> dict[int, SheetState]:
        """入り口の情報"""
        state = {}
        for i, lane in enumerate(self.sheet):
            if lane[0] == None:
                state[i] = SheetState.EMPTY
            else:
                state[i] = SheetState.FULL
        return state

    def add_person(self, person: Person, lane_number: int) -> bool:
        if lane_number < 0:
            raise ValueError("lane must be positive")
        if lane_number >= self.lane_count:
            raise ValueError("lane must be less than lane_count")

        if self.sheet[lane_number][0] is not None:
            return False
        self.sheet[lane_number][0] = person
        if self.on_person_enter is not None:
            self.on_person_enter(person)
        return True

    def move(self):
        next = self._make_sheet()
        for lane_number, lane in enumerate(self.sheet):
            for pos, person in enumerate(lane):
                # ステップに誰もいない
                if person is None:
                    continue
                # エスカレータの速さ＋人の速さで動く
                next_step_index = pos + int(self.velocity + person.velocity)
                # エスカレータから出た場合
                if next_step_index >= self.length:
                    if self.on_person_exit is not None:
                        self.on_person_exit(person)
                    continue
                # 人を移動させる
                next[lane_number][next_step_index] = person
        # 状態を更新
        self.sheet = next
