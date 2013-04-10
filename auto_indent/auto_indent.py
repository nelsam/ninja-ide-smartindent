# -*- coding: UTF-8 -*-

from ninja_ide.core import plugin
from PyQt4.Qt import Qt


class AutoIndent(plugin.Plugin):
    """
    An attempt to make a NINJA-IDE plugin that makes the tab key act
    more like emacs' semi-automatic indenter.
    """

    def initialize(self):
        """
        Sets up the environment for the auto indenter.
        """
        self.editor_service = self.locator.get_service('editor')
        self.editor_service.editorKeyPressEvent.connect(self.check_indent)
        self.editor = self.editor_service.get_editor()

    def check_indent(self, event):
        """
        Reads in a key press event and, on pressing the tab key,
        interrupts the insertion of four spaces and tries to
        cycle through possible indentation levels.
        """
        if event.key() == Qt.Key_Tab:
            self.indent()

    def indent(self):
        """
        Attempts to automatically indent to a correct level.
        """
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            block = self.editor.document().findBlock(cursor.selectionStart())
            # Indent the selection
        else:
            position = self.editor.get_cursor_position()
            block = self.editor.document().findBlock(position)

    def finish(self):
        """
        Cleans up and shuts down the auto indenter.
        """
        pass

    def get_preferences_widget(self):
        """
        Returns the widget for setting preferences
        related to the auto indenter.
        """
        pass
