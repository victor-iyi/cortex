"""Events for the Cortex API."""

from enum import StrEnum


class Event(StrEnum):
    """Base event class."""

    @classmethod
    def get_events(cls) -> list[str]:
        """Get all events.

        Returns:
            list[str]: All events.

        """
        return [str(value) for value in cls.__members__.values()]

    @classmethod
    def get_event(cls, event: str) -> 'Event' | None:
        """Get an event.

        Args:
            event (str): The event to get.

        Returns:
            Event | None: The event.

        """
        return cls.__members__.get(event)

    @classmethod
    def has_event(cls, event: str) -> bool:
        """Check if an event exists.

        Args:
            event (str): The event to check.

        Returns:
            bool: True if the event exists, False otherwise.

        """
        return event in cls.get_events()

    @classmethod
    def is_event(cls, event: str) -> bool:
        """Check if an event is valid.

        Args:
            event (str): The event to check.

        Returns:
            bool: True if the event is valid, False otherwise.

        """
        return event in cls.__members__


class MarkerEvent(Event):
    """Marker events."""

    INJECTED = 'inject_marker_done'
    UPDATED = 'update_marker_done'


class MentalCommandEvent(Event):
    """Mental command events."""

    ACTION_SENSITIVITY = 'action_sensitivity_done'
    BRAIN_MAP = 'brain_map_done'
    GET_ACTIVE_ACTION = 'get_active_action_done'
    SET_ACTIVE_ACTION = 'set_active_action_done'
    TRAINING_THRESHOLD = 'training_threshold_done'


class NewDataEvent(Event):
    """New data events."""

    COM_DATA = 'new_com_data'
    DATA_LABELS = 'new_data_labels'
    DEV_DATA = 'new_dev_data'
    EEG_DATA = 'new_eeg_data'
    FE_DATA = 'new_fe_data'
    MET_DATA = 'new_met_data'
    MOT_DATA = 'new_mot_data'
    POW_DATA = 'new_pow_data'
    SYS_DATA = 'new_sys_data'


class ProfileEvent(Event):
    """Profile events."""

    CREATED = 'create_profile_done'
    SAVED = 'save_profile_done'
    QUERIED = 'query_profile_done'
    LOADED_UNLOADED = 'load_unload_profile_done'


class RecordEvent(Event):
    """Record events."""

    CREATED = 'create_record_done'
    STOPPED = 'stop_record_done'
    EXPORTED = 'export_record_done'


class SessionEvent(Event):
    """Session events."""

    CREATED = 'create_session_done'
    SAVED = 'save_session_done'


class WarningEvent(Event):
    """Warning events."""

    CORTEX_STOP_ALL_SUB = 'warn_cortex_stop_all_sub'


class ErrorEvent(Event):
    """Error events."""

    INFORM_ERROR = 'inform_error'
