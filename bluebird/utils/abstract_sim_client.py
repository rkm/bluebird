"""
Contains the AbstractSimClient class
"""
from abc import ABC
from abc import abstractmethod
from typing import List

from semver import VersionInfo

from bluebird.utils.abstract_aircraft_controls import AbstractAircraftControls
from bluebird.utils.abstract_simulator_controls import AbstractSimulatorControls
from bluebird.utils.timer import Timer


class AbstractSimClient(ABC):
    """
    Adapter class to provide a common interface between BlueBird and the different
    simulator clients
    """

    @property
    @abstractmethod
    def aircraft(self) -> AbstractAircraftControls:
        """
        :return: Returns the client's aircraft controller instance
        :rtype: AbstractAircraftControls
        """

    @property
    @abstractmethod
    def simulation(self) -> AbstractSimulatorControls:
        """
        :return: Returns the client's simulator controller instance
        :rtype: AbstractSimulatorControls
        """

    @property
    @abstractmethod
    def sim_version(self) -> VersionInfo:
        """
        Return the version of the connected simulation server
        :return:
        """

    @abstractmethod
    def connect(self, timeout: int = 1) -> None:
        """
        Connect to the simulation server
        :param timeout:
        :raises TimeoutException: If the connection could not be made before the timeout
        :return:
        """

    @abstractmethod
    def start_timers(self) -> List[Timer]:
        """Start any timed functions, and return all the Timer instances"""

    @abstractmethod
    def shutdown(self, shutdown_sim: bool = False) -> bool:
        """
        Disconnect from the simulation server, and stop the client (including any
        timers)
        :param shutdown_sim: If true, also informs the simulation server to exit
        :return: If shutdown_sim was requested, the return value will indicate whether
        the simulator was shut down successfully. Always returns True if shutdown_sim
        was not requested
        """
