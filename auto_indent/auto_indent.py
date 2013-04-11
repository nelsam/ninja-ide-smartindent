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
    currentcontext = None
    currentindent = None

    """
    Characters that cause continuation lines.
    """
    CONTINUATION_CHARACTERS = (
        ('[', ']'),
        ('(', ')'),
        ('{', '}'),
        )

    """
    Characters that cause us to ignore lines.
    """
    MULTILINE_QUOTE_SEQUENCES = (
        '"""',
        "'''",
        )

    def initialize(self):
        """
        Sets up the environment for the auto indenter.
        """
        self.editor_service = self.locator.get_service('editor')
        self.editor_service.editorKeyPressEvent.connect(self.check_mode)
        self.editor_service.currentTabChanged.connect(self.load_context)
        self.editor = self.editor_service.get_editor()
        self.indent_str = ' ' * self.editor.indent
        if self.editor.useTabs:
            self.indent_str = '\t'
        self.currentcontext = None
        self.currentindent = 0
        self.editor.preKeyPress[Qt.Key_Tab] = self.indent

    @property
    def context(self):
        if not hasattr(self, '_context'):
            self.load_context()

        return self._context

    def load_context(self, filename=None):
        doc = self.editor.document()
        block = doc.begin()

        self._context = {}
        while block != doc.end():
            self.parse_line(block)

    def parse_line(self, block):
        context = []
        block_text = block.text()

    def check_indent(self, event):
        """
        Reads in a key press event and, on pressing the tab key,
        interrupts the insertion of four spaces and tries to
        cycle through possible indentation levels.
        """
        if event.key() == Qt.Key_Tab:
            self.indent_mode = True
        elif self.indent_mode:
            self.indent_mode = False

    def find_line_start(self, block):


    def find_previous_indenter(self, block):
        """
        Locates the most recently previous block that affected
        this block's indentation.
        """
        block_indent = self.current_indent(block)
        while True:
            block = block.previous()
            if ':' in block.text():
                start_block = self.find_line_start(block)
                start_indent = self.current_indent(block)
                if start_indent < block_indent:
                    break
        return block

    def find_base_block(self, block):
        """
        Finds the base (unindented) block most recent to this one.
        """
        text = str(block.text())
        while text.startswith(self.indent_str):
            block = self.find_previous_indenter(block)
            text = str(block.text)

        return block

    def load_indent_lines(self, block):
        """
        Loads any lines that change the indentation level into a list,
        each one containing a list of possible indentation levels.
        """
        cursor = self.editor.textCursor()
        scope = []
        while True:
            if str(block.text()).endswith(':'):
                # Increases indent

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

    def find_max_indent(self, cursor, block):
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
