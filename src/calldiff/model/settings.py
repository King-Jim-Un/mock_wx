"""Base class for persistent settings saved/restored between runs"""

from binascii import b2a_base64, a2b_base64
from dataclasses import dataclass
import logging
import pickle
from typing import ClassVar
import wx

from calldiff.constants import CONSTANTS

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class Settings:
    """Base class for persistent settings saved/restored between runs"""

    APP_VERSION: ClassVar[int] = 0
    data_version: int = 0

    @classmethod
    def load(cls, reset: bool = False) -> "Settings":
        """Load settings"""
        if reset:
            return cls()

        try:
            config = wx.Config(CONSTANTS.PERSIST.APP_NAME, CONSTANTS.PERSIST.VENDOR_NAME)
            settings = pickle.loads(a2b_base64(config.Read(CONSTANTS.PERSIST.PATH_NAME)))
        except Exception as error:
            LOG.warning("Unable to load settings: %s", error)
            return cls()

        if settings.data_version > cls.APP_VERSION:
            LOG.warning("Incompatible settings")
            return cls()

        try:
            while settings.data_version < cls.APP_VERSION:
                upgrade = f"upgrade_{settings.data_version}_to_{settings.data_version + 1}"
                LOG.debug("Upgrading settings: %s", upgrade)
                settings = getattr(settings, upgrade)()
        except Exception as error:
            LOG.warning("Unable to update settings: %s", error)
            return cls()

        if sorted(list(cls().__dict__)) != sorted(list(settings.__dict__)):
            LOG.warning("Keys changed")
            return cls()

        return settings

    def save(self) -> None:
        """Save settings"""
        try:
            config = wx.Config(CONSTANTS.PERSIST.APP_NAME, CONSTANTS.PERSIST.VENDOR_NAME)
            config.Write(CONSTANTS.PERSIST.PATH_NAME, b2a_base64(pickle.dumps(self)).decode("ascii"))
            config.Flush()
        except Exception as error:
            LOG.warning("Unable to save settings: %s", error)
