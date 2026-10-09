from PySide6.QtWidgets import QDialog, QDialogButtonBox, QTextBrowser, QVBoxLayout, QWidget

NOTES_HTML = """
<h2>How to use</h2>
<ol>
<li>Type or paste your message in <b>Enter Your Message</b>.</li>
<li>Pick a conversion mode and press <b>Generate Code</b> (Ctrl+Enter).</li>
<li>Use <b>Copy Code</b> to copy the result, or <b>Clear</b> to start over.</li>
</ol>
<h3>Conversion modes</h3>
<ul>
<li><b>Character</b> &ndash; each character is converted individually; words are separated by two spaces.</li>
<li><b>Word</b> &ndash; each word is listed with its codes.</li>
<li><b>Sentence</b> &ndash; text is split at sentence boundaries and each sentence is converted.</li>
<li><b>Text &rarr; Morse / Morse &rarr; Text</b> &ndash; encode or decode Morse. When decoding, separate
letters with one space and words with two spaces, <code>/</code> or a new line.</li>
<li><b>Text &rarr; ROT13 / ROT13 &rarr; Text</b> &ndash; rotate letters by 13; case, numbers,
punctuation and whitespace are preserved.</li>
<li><b>Text &rarr; ROT13 &rarr; Morse</b> and its reverse chain both steps.</li>
</ul>
<h3>Notes</h3>
<ul>
<li>Uppercase and lowercase letters map to the same code.</li>
<li>Unsupported characters are reported as warnings instead of being silently removed.</li>
<li>Reversing an output generated in this session restores the exact original text, including case.</li>
</ul>
"""


class NotesDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Help & Notes")
        self.resize(560, 520)
        browser = QTextBrowser()
        browser.setHtml(NOTES_HTML)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout = QVBoxLayout(self)
        layout.addWidget(browser)
        layout.addWidget(buttons)
