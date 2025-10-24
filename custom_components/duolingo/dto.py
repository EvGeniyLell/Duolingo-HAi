from dataclasses import dataclass


@dataclass
class UserIdentifiersDto:
    id: int
    name: str
    username: str

    ID_KEY = "id"
    NAME_KEY = "name"
    USERNAME_KEY = "username"

    @classmethod
    def from_dict(cls, data: dict) -> "UserIdentifiersDto":
        """Create UserIdentifiersDto from dictionary."""
        return cls(
            id=data.get(UserIdentifiersDto.ID_KEY, 0),
            name=data.get(UserIdentifiersDto.NAME_KEY, ""),
            username=data.get(UserIdentifiersDto.USERNAME_KEY, ""),
        )

    @property
    def to_dict(self) -> dict:
        """Convert UserIdentifiersDto to dictionary."""
        return {
            UserIdentifiersDto.ID_KEY: self.id,
            UserIdentifiersDto.NAME_KEY: self.name,
            UserIdentifiersDto.USERNAME_KEY: self.username,
        }

    @property
    def as_entry_title(self) -> str:
        """Convert UserIdentifiersDto to dictionary."""
        return f"{self.id} ({self.name})"


@dataclass
class UserDto:
    id: int
    name: str
    username: str
    total_xp: int
    courses_xp: dict[str, int]
    streak_today: bool
    streak_length: int

    ID_KEY = "id"
    NAME_KEY = "name"
    USERNAME_KEY = "username"
    TOTAL_XP_KEY = "total_xp"
    COURSES_XP_KEY = "courses_xp"
    STREAK_TODAY_KEY = "streak_today"
    STREAK_LENGTH_KEY = "streak_length"

    @classmethod
    def from_dict(cls, data: dict) -> "UserDto":
        """Create UserDto from dictionary."""
        return cls(
            id=data.get(UserDto.ID_KEY, 0),
            name=data.get(UserDto.NAME_KEY, ""),
            username=data.get(UserDto.USERNAME_KEY, ""),
            total_xp=data.get(UserDto.TOTAL_XP_KEY, 0),
            courses_xp=data.get(UserDto.COURSES_XP_KEY, {}),
            streak_today=data.get(UserDto.STREAK_TODAY_KEY, False),
            streak_length=data.get(UserDto.STREAK_LENGTH_KEY, 0),
        )

    @property
    def to_dict(self) -> dict:
        """Convert UserDto to a dictionary."""
        return {
            UserDto.ID_KEY: self.id,
            UserDto.NAME_KEY: self.name,
            UserDto.USERNAME_KEY: self.username,
            UserDto.TOTAL_XP_KEY: self.total_xp,
            UserDto.COURSES_XP_KEY: self.courses_xp,
            UserDto.STREAK_TODAY_KEY: self.streak_today,
            UserDto.STREAK_LENGTH_KEY: self.streak_length,
        }
