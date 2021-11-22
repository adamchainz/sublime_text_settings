import re
import subprocess

import sublime_plugin


class MarkdownToRstCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for sel in reversed(self.view.sel()):
            # Run pandoc
            text = self.view.substr(sel)

            if re.search(r"</\w+>", text) or text.startswith("<img"):
                source = "html"
            else:
                source = "markdown"

            proc = subprocess.Popen(
                ["pandoc", "-f", source, "-t", "rst", "--wrap", "none"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )
            out, err = proc.communicate(input=text, timeout=1.0)

            # Replace non-breaking spaces after e.g. "e.g."
            out = re.sub(r"\xa0", r" ", out, flags=re.MULTILINE)

            # Replace '.. figure' with '.. image'
            out = re.sub(r"^\.\. figure::", r".. image::", out, flags=re.MULTILINE)

            # Replace '.. code' with '.. code-block'
            out = re.sub(r"^\.\. code::", r".. code-block::", out, flags=re.MULTILINE)

            # Fix up escaping after code
            out = re.sub(r"``\\ ", r"``\\", out, flags=re.MULTILINE)

            # Fix up bullet point style
            out = re.sub(r"^-  ", r"* ", out, flags=re.MULTILINE)

            # Sentence per line
            out = re.sub(r"(\w{2,}|[”’)`])(?<!\be\.g|\bi\.e)([.!?]) ", r"\1\2\n", out)

            if not text.endswith("\n") and out.endswith("\n"):
                out = out[:-1]

            # links with code inside them
            trailer = ""

            def replace_link_with_code(match):
                nonlocal trailer
                text = match["text"]
                reference = text.replace("`", "").rstrip()
                trailer += (
                    "\n"
                    + ".. |"
                    + reference
                    + "| replace:: "
                    + text
                    + "\n"
                    + "__ "
                    + match["link"]
                    + "\n"
                )
                return "|" + reference + "|__"

            out = re.sub(
                r"(?<!`)`(?!__)(?P<text>[^`<]*?``[^<]+?)<(?P<link>.*?)>`__",
                replace_link_with_code,
                out,
            )
            if trailer:
                out += "\n"
                out += trailer

            self.view.replace(edit, sel, out)

        self.view.end_edit(edit)
