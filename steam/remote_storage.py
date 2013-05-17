"""
Remote storage/UGC
Copyright (c) 2010-2013, Anthony Garcia <anthony@lagg.me>
Distributed under the ISC License (see LICENSE)
"""

import json
import api

class UGCError(api.APIError):
    pass

class ugc_file(object):
    @property
    def size(self):
        """ Size in bytes """
        return self._data["size"]

    @property
    def filename(self):
        """ Local filename is what the user named it, not the URL """
        return self._data["filename"]

    @property
    def url(self):
        """ UGC link """
        return self._data["url"]

    @property
    def _data(self):
        if self._cache:
            return self._cache

        data = None
        status = None
        try:
            data = self._api["data"]
            status = self._api["status"]["code"]
        except KeyError:
            if not data:
                if status != None and status != 9:
                    raise UGCError("Code " + str(status))
                else:
                    raise UGCError("File not found")

        self._cache = data
        return self._cache

    def __init__(self, appid, ugcid64, **kwargs):
        self._cache = {}
        self._api = api.interface("ISteamRemoteStorage").GetUGCFileDetails(ugcid = ugcid64, appid = appid, **kwargs)
