import re

import sublime_plugin


class RstInlineLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in reversed(self.view.sel()):
            text = self.view.substr(region)

            match = re.match(r"`(?P<text>[^<]*)<(?P<link>.*)>`__", text)
            if not match:
                continue

            reference = match["text"].replace("`", "").rstrip()

            endline = self.view.find(r"^$", max((region.a, region.b)))

            self.view.replace(
                edit,
                endline,
                "\n"
                + ".. |"
                + reference
                + "| replace:: "
                + match["text"]
                + "\n"
                + "__ "
                + match["link"]
                + "\n",
            )

            self.view.replace(edit, region, "|" + reference + "|__")

        self.view.end_edit(edit)
