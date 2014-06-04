import sublime_plugin


class LastViewCommand(sublime_plugin.WindowCommand):
    def run(self):
        active_group = self.window.active_group()
        view = self.window.views_in_group(active_group)[-1]
        self.window.focus_view(view)
