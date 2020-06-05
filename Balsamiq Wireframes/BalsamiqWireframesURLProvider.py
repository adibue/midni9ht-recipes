#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import json

from autopkglib import Processor, ProcessorError, URLGetter

__all__ = ["BalsamiqWireframesURLProvider"]


BASE_URL = "https://builds.balsamiq.com/bwd/mac.jsonp"


class BalsamiqWireframesURLProvider(URLGetter):
    # class BalsamiqWireframesURLProvider():
    """Provides a download URL for the latest Balsamiq Wireframes release."""
    input_variables = {
        "base_url": {"required": False, "description": "Default is %s" % BASE_URL,},
    }
    output_variables = {
        "url": {"description": "URL to the latest Balsamiq Wireframes release.",},
        "date": {
            "description": "Release date of the latest Balsamiq Wireframes release.",
        },
        "version": {"description": "Version of the latest Balsamiq Wireframes release.",},
    }
    description = __doc__

    def get_balsamiq_url(self, base_url):
        try:
            url = self.download(base_url)
            return json.loads(url[len("jsoncallback(") : -2])

        except Exception as err:
            raise Exception("Can't read %s: %s" % (base_url, err))

    def main(self):
        """Find and return a download URL"""
        base_url = self.env.get("base_url", BASE_URL)
        self.env["object"] = self.get_balsamiq_url(base_url)
        self.env["url"] = (
            "https://builds.balsamiq.com/bwd/"
            "Balsamiq%20Wireframes%20%s.dmg" % self.env["object"]["version"]
        )
        self.env["version"] = self.env["object"]["version"]
        self.env["date"] = self.env["object"]["date"]
        self.output("Found URL %s" % self.env["url"])


if __name__ == "__main__":
    processor = BalsamiqWireframesURLProvider()
    processor.execute_shell()
