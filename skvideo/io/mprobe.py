import subprocess as sp

from .._utils import *

def mprobe(filename):
    """get metadata by using mediainfo

    Checks the output of mediainfo on the desired video
    file. Data is then parsed into a dictionary and
    checked for video data. If no such video data exists,
    an empty dictionary is returned.

    Parameters
    ----------
    filename : string
        Path to the video file

    Returns
    -------
    mediaDict : dict
       Dictionary containing all header-based information 
       about the passed-in source video.

    """
    # '-f' gets full output, and --Output=XML is xml formatted output
    command = ["mediainfo", "-f", "--Output=XML", filename]

    # simply get std output
    xml = check_output(command)

    d = xmltodictparser(xml)

    assert "Mediainfo" in d
    d = d["Mediainfo"]

    assert "File" in d
    d = d["File"]

    assert "track" in d
    unorderedtracks = d["track"]

    # tracksbytype normalizes the input by key
    tracksbytype = {}
    if type(unorderedtracks) is list:
        for d in unorderedtracks:
            assert "@type" in d
            # can't have more than 1 key. If this case arises
            # an issue should be made in the tracker for a fix.
            assert d["@type"] not in tracksbytype 
            tracksbytype[d["@type"]] = d
    else: # not list
        assert "@type" in unorderedtracks
        tracksbytype[unorderedtracks["@type"]] = unorderedtracks

    return tracksbytype
