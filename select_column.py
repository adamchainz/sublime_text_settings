import sublime
import sublime_plugin


class SelectColumnCommand(sublime_plugin.TextCommand):
    def run(self, edit, column_num):
        view = self.view
        sel = view.sel()

        regex = (
            '^'  # start of line
            '([^\\t]+\\t){%i}'  # not a tab +, then tab, n - 1 times
            '([^\\t\\n]+){1}'  # not a tab or newline +, once
        ) % (column_num - 1)

        found = view.find_all(regex, sublime.IGNORECASE)

        if len(found) > 0:
            sel.clear()
            for region in found:
                substr = view.substr(region)
                if column_num > 1:
                    last_tab = substr.rfind("\t") + 1
                else:
                    last_tab = 0
                sel.add(sublime.Region(region.a + last_tab, region.b))


class SelectColumnPromptCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel(
            "Column Number (1 = first):", "", self.on_done, None, None)

    def on_done(self, text):
        try:
            column_num = int(text)
        except ValueError:
            return

        if column_num < 1:
            column_num = 0

        self.window.run_command("select_column", {"column_num": column_num})
