import sublime
import sublime_plugin


class DeleteLineAboveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view

        if len(view.sel()) > 1:
            return

        cursor = view.sel()[0].begin()
        line = view.line(cursor)
        if line.begin() == 0:
            return

        above = view.line(line.begin() - 1)
        above_plus_nl = sublime.Region(above.begin(), above.end() + 1)
        view.replace(edit, above_plus_nl, '')


class DeleteLineBelowCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view

        if len(view.sel()) > 1:
            return

        cursor = view.sel()[0].begin()
        line = view.line(cursor)

        below = view.line(line.end() + 1)
        below_plus_nl = sublime.Region(below.begin(), below.end() + 1)

        view.replace(edit, below_plus_nl, '')
