# -*- coding: UTF-8 -*-

from ninja_ide.core import plugin
from PyQt4.Qt import Qt, QTextCursor


class AutoIndent(plugin.Plugin):
    """
    An attempt to make a NINJA-IDE plugin that makes the tab key act
    more like emacs' semi-automatic indenter.
    """

    """
    Stores whether or not the previous command was an indent.
    """
    indent_mode = False

    def initialize(self):
        """
        Sets up the environment for the auto indenter.
        """
        self.editor_service = self.locator.get_service('editor')
        #self.editor_service.editorKeyPressEvent.connect(self.check_indent)
        self.editor = self.editor_service.get_editor()
        self.editor.preKeyPress[Qt.Key_Tab] = self.indent

    def check_indent(self, event):
        """
        Reads in a key press event and, on pressing the tab key,
        interrupts the insertion of four spaces and tries to
        cycle through possible indentation levels.
        """
        if event.key() == Qt.Key_Tab:
            self.indent()
        elif self.indent_mode:
            self.indent_mode = False

    def current_indent(self, block):
        """
        Reads the current indentation level of a block.
        """
        cursor = self.editor.textCursor()
        cursor.setPosition(block.position())
        indent = 0
        while cursor.selectedText() == ((' ' * self.editor.indent) * indent):
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor,
                                self.editor.indent)
            indent += 1

        return indent - 1

    def find_default_indent(self, cursor, block):
        """
        Finds the default (i.e. most likely) indentation level
        for a given block of text.
        """
        block = block.previous()
        while (not block.text().strip() or
               block.text().strip().startswith('#')):
            block = block.previous()

        indent = self.current_indent(block)
        if block.text().strip().endswith(':'):
            indent += 1

        return indent

    def indent(self, event):
        """
        Attempts to automatically indent to a correct level.
        """
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            pass
            #start_position = cursor.selectionStart()
            #end_position = cursor.selectionEnd()
            #block = self.editor.document().findBlock(start_position)
            # Indent the selection
        else:
            position = self.editor.get_cursor_position()
            block = self.editor.document().findBlock(position)
            default_indent = self.find_default_indent(cursor, block)
            cursor.setPosition(block.position())
            while cursor.selectedText().strip() == '':
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)

            cursor.removeSelectedText()
            cursor.insertText((' ' * self.editor.indent) * default_indent)

        self.indent_mode = True
        return True

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
