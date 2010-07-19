#!/usr/bin/env python

"""
Module for reading Steam user account data

Copyright (c) 2010, Anthony Garcia <lagg@lavabit.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

import json, urllib2, steam, time

_old_profile_url = "http://steamcommunity.com/id/%s?xml=1"
_profile_url = ("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/"
                "v0001/?key=" + steam.api_key + "&steamids=")

class profile:
    # Hopefully Valve will provide a request for doing this so we won't
    # have to use the old API
    def _get_id64_from_sid(self, sid):
        """ This uses the old API, don't use this directly. """
        prof = urllib2.urlopen(_old_profile_url % sid).read()
        if type(sid) == str and prof.find("<steamID64>") != -1:
            prof = (prof[prof.find("<steamID64>")+11:
                             prof.find("</steamID64>")])

            return prof

    def get_summary(self, sid):
        """ Returns the summary object. The wrapper functions should
        normally be used instead."""
        id64 = self._get_id64_from_sid(sid)

        if not id64:
            #Assume it's the 64 bit ID
            id64 = sid

        self.summary_object = (json.load(urllib2.urlopen(_profile_url + str(id64)))
                               ["response"]["players"]["player"][0])

        return self.summary_object

    def get_id64(self):
        """ Returns the 64 bit steam ID (use with other API requests) """
        return self.summary_object["steamid"]

    def get_persona(self):
        """ Returns the user's persona (what you usually see in-game) """
        return self.summary_object["personaname"]

    def get_profile_url(self):
        """ Returns a URL to the user's Community profile page """
        return self.summary_object["profileurl"]

    def get_avatar_url(self, size):
        """ Returns a URL to the user's avatar, see AVATAR_* """
        return self.summary_object[size]

    def get_status(self):
        """ Returns the user's status as a string. (or integer if unrecognized)"""
        status = self.summary_object["personastate"]

        if status == 0:   return "offline"
        elif status == 1: return "online"
        elif status == 2: return "busy"
        elif status == 3: return "away"
        elif status == 4: return "snooze"

        return status

    def get_visibility(self):
        """ Returns the visibility setting of the profile """
        vis = self.summary_object["communityvisibilitystate"]

        if vis == 1: return "private"
        if vis == 2: return "friends"
        if vis == 3: return "public"

        return vis

    # This might be redundant, can we still get an id64 from an unconfigured profile?
    def is_configured(self):
        """ Returns true if the user has created a Community profile """

        if (self.summary_object.has_key("profilestate") and
            self.summary_object["profilestate"]):
            return True
        else:
            return False

    def get_last_online(self):
        """ Returns the last time the user was online as a localtime
        time.struct_time struct """

        return time.localtime(self.summary_object["lastlogoff"])

    def is_comment_enabled(self):
        """ Returns true if the profile allows public comments """
        if (self.summary_object.has_key("commentpermission") and
            self.summary_object["commentpermission"]):
            return True
        else:
            return False

    def get_real_name(self):
        """ Returns the user's real name if it's set and public """
        if (self.get_visibility() == "public" and
            self.summary_object.has_key("realname")):
            return self.summary_object["realname"]

    # This isn't very useful yet since there's no API request
    # for groups yet, and I'm avoiding using the old API
    # as much as possible
    def get_primary_group(self):
        """ Returns the user's primary group ID if set. """
        if (self.get_visibility() == "public" and
            self.summary_object.has_key("primaryclanid")):
            return self.summary_object["primaryclanid"]

    def get_creation_date(self):
        """ Returns the account creation date as a localtime time.struct_time
        struct if public"""
        if (self.get_visibility() == "public" and
            self.summary_object.has_key("timecreated")):
            return time.localtime(self.summary_object["timecreated"])

    def get_current_game(self):
        """ Returns a dict of game info if the user is playing if public and set
        id is an integer
        server is the IP address:port string, will be 0.0.0.0:0 if they're not on a server
        extra is the game name """
        ret = {}
        if self.get_visibility() == "public":
            if self.summary_object.has_key("gameid"):
                ret["id"] = self.summary_object["gameid"]
            if self.summary_object.has_key("gameserverip"):
                ret["server"] = self.summary_object["gameserverip"]
            if self.summary_object.has_key("gameextrainfo"):
                ret["extra"] = self.summary_object["gameextrainfo"]

            return ret

    def get_location(self):
        """ Returns a dict of location data if public and set
        country: A two char ISO country code
        state: A two char ISO state code """
        ret = {}
        if self.get_visibility() == "public":
            if self.summary_object.has_key("loccountrycode"):
                ret["country"] = self.summary_object["loccountrycode"]
            if self.summary_object.has_key("locstatecode"):
                ret["state"] = self.summary_object["locstatecode"]

            return ret

    def __init__(self, sid):
        """ Creates a profile instance for the given user """

        self.get_summary(sid)

    AVATAR_SMALL = "avatar"
    AVATAR_MEDIUM = "avatarmedium"
    AVATAR_LARGE = "avatarfull"