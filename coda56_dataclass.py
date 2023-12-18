from dataclasses import dataclass


@dataclass
class DownstreamOfdmInfo:
    """
    DataClass structure - DownstreamOfdmInfo
    """

    receive: int
    ffttype: str
    Subcarr0freqFreq: int
    plclock: str
    ncplock: str
    mdc1lock: str
    plcpower: float
    SNR: int
    dsoctets: int
    correcteds: int
    uncorrect: int


@dataclass
class DownstreamInfo:
    """
    DataClass structure - DownstreamOfdmInfo
    """

    portId: int
    frequency: int
    modulation: str
    signalStrength: float
    snr: float
    dsoctets: int
    correcteds: int
    uncorrect: int
    channelId: int


@dataclass
class UpstreamOfdmInfo:
    """
    DataClass structure - UpstreamOfdmInfo
    """

    uschindex: int
    state: str
    frequency: int
    digAtten: float
    digAttenBo: float
    channelBw: float
    repPower: float
    repPower1_6: float
    fftVal: str


@dataclass
class UpstreamInfo:
    """
    DataClass structure - UpstreamInfo
    """

    portId: int
    frequency: int
    bandwidth: int
    modtype: str
    scdmaMode: str
    signalStrength: float
    channelId: int
