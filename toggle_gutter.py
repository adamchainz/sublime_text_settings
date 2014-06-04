import sublime
import sublime_plugin


class ToggleGutterCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        s = sublime.load_settings("Preferences.sublime-settings")
        current = s.get("gutter", True)
        next = not current
        s.set("gutter", next)
        sublime.save_settings("Preferences.sublime-settings")
