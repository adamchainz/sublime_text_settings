import sublime_plugin


class InterpretWithPythonCommand(sublime_plugin.TextCommand):
    always_import = (
        "datetime",
        "html",
        "math",
        "random",
        "statistics",
    )

    def run(self, edit):
        # Import
        glob = globals()
        loc = {}
        for import_me in self.always_import:
            module = __import__(import_me, glob, loc, ["*"])
            for k in dir(module):
                loc[k] = getattr(module, k)

        # Interpret forwards
        replaces = []
        for sel in self.view.sel():
            if sel.size() > 0:
                text = self.view.substr(sel)

                try:
                    evald = str(eval(text, glob, loc))
                except Exception as e:
                    evald = str(e)
                replaces.append((sel, evald))

        for (sel, evald) in reversed(replaces):
            self.view.replace(edit, sel, evald)

        self.view.end_edit(edit)
