from dataclasses import dataclass


@dataclass
class UserDto:
    id: int
    name: str
    username: str
    total_xp: int
    courses_xp: dict[str, int]
    streak_today: bool
    streak_length: int

    HA_MAPPING_ID = "name"
    HA_MAPPING_NAME = "name"
    HA_MAPPING_USERNAME = "username"
    HA_MAPPING_TOTAL_XP = "total_xp"
    HA_MAPPING_COURSES_XP = "courses_xp"
    HA_MAPPING_STREAK_TODAY = "streak_today"
    HA_MAPPING_STREAK_LENGTH = "streak_length"

    @classmethod
    def from_ha(cls, data: dict) -> "UserDto":
        """Create a UserDto from a coordinator.data."""
        return cls(
            id=data.get(UserDto.HA_MAPPING_ID, 0),
            name=data.get(UserDto.HA_MAPPING_NAME, ""),
            username=data.get(UserDto.HA_MAPPING_USERNAME, ""),
            total_xp=data.get(UserDto.HA_MAPPING_TOTAL_XP, 0),
            courses_xp=data.get(UserDto.HA_MAPPING_COURSES_XP, {}),
            streak_today=data.get(UserDto.HA_MAPPING_STREAK_TODAY, False),
            streak_length=data.get(UserDto.HA_MAPPING_STREAK_LENGTH, 0),
        )

    @property
    def to_ha(self) -> dict:
        """Convert UserDto to a coordinator.data."""
        return {
            UserDto.HA_MAPPING_ID: self.id,
            UserDto.HA_MAPPING_NAME: self.name,
            UserDto.HA_MAPPING_USERNAME: self.username,
            UserDto.HA_MAPPING_TOTAL_XP: self.total_xp,
            UserDto.HA_MAPPING_COURSES_XP: self.courses_xp,
            UserDto.HA_MAPPING_STREAK_TODAY: self.streak_today,
            UserDto.HA_MAPPING_STREAK_LENGTH: self.streak_length,
        }
