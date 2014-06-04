import sublime
import sublime_plugin


class DefaultFontSizeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("font_size", 16)
        sublime.save_settings("Preferences.sublime-settings")
