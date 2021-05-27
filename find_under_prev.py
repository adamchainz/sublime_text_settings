from collections import deque
import sublime
import sublime_plugin


def find_under_prev(view, edit, skip=False):
    sels = view.sel()

    if len(sels) == 1 and sels[0].size() == 0:
        # Just select word if we haven't got one already
        view.window().run_command("find_under_expand")
        print("find_under_expand")
    else:
        # Move to single sel, jump back one, then reselect what we had
        # previously. A hack, for sure, but no easier way to do it.
        wheres = deque([(i.a, i.b) for i in sels])
        view.run_command("single_selection")
        view.window().run_command("find_under_prev")

        if skip:
            wheres.popleft()

        for w in wheres:
            r = sublime.Region(w[0], w[1])
            sels.add(r)


class FindUnderPrevExpandCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        find_under_prev(self.view, edit)


class FindUnderPrevExpandSkipCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        find_under_prev(self.view, edit, skip=True)
