from PyQt6.QtWidgets import QTextBrowser
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import markdown
import re
from datetime import datetime

class MarkdownViewer(QTextBrowser):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setOpenExternalLinks(True)
        
        # Monospace font for hacker aesthetic
        font = QFont("Monaco", 12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        # E-ink optimized styling
        self.setStyleSheet("""
        QTextBrowser {
            background-color: #000000;
            color: #ffffff;
            border: none;
            padding: 8px;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
            selection-background-color: #333333;
            selection-color: #ffffff;
        }
        """)
        
        self.md = markdown.Markdown(extensions=['extra'])
        
    def preprocess_text(self, text: str) -> str:
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            # Convert task list items to ASCII style
            if re.match(r'^\s*- \[ \]', line):
                line = re.sub(r'- \[ \]', '[ ]', line)
            elif re.match(r'^\s*- \[x\]', line):
                line = re.sub(r'- \[x\]', '[X]', line)
            
            # Process due dates in task lines
            if re.match(r'^\s*\[[X ]\]', line):
                # Find due dates
                due_match = re.search(r'!due\(([^)]+)\)', line)
                if due_match:
                    due_str = due_match.group(1)
                    try:
                        due_date = datetime.strptime(due_str, '%Y-%m-%d')
                        today = datetime.now()
                        days_until = (due_date - today).days
                        
                        if days_until < 0:
                            due_text = f"[OVERDUE:{abs(days_until)}d]"
                        elif days_until == 0:
                            due_text = "[DUE:TODAY]"
                        elif days_until <= 3:
                            due_text = f"[DUE:{days_until}d]"
                        else:
                            due_text = f"[{due_date.strftime('%m-%d')}]"
                        
                        line = re.sub(r'!due\([^)]+\)', due_text, line)
                    except:
                        pass
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
        
    def set_markdown(self, text: str):
        processed_text = self.preprocess_text(text)
        html = self.md.convert(processed_text)
        
        # E-ink optimized monospace CSS
        css = """
        <style>
        body {
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 12px;
            line-height: 1.4;
            color: #ffffff;
            background-color: #000000;
            margin: 0;
            padding: 0;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-weight: normal;
            margin: 8px 0 4px 0;
            padding: 0;
        }
        
        h1 { border-bottom: 1px solid #ffffff; }
        h2 { border-bottom: 1px solid #333333; }
        
        p { 
            margin: 4px 0; 
            padding: 0;
        }
        
        ul, ol {
            margin: 4px 0;
            padding-left: 16px;
        }
        
        li {
            margin: 2px 0;
            padding: 0;
        }
        
        li[data-task] {
            list-style: none;
            margin-left: -16px;
        }
        
        code {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            padding: 0;
        }
        
        pre {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            margin: 4px 0;
            padding: 4px;
            border: 1px solid #333333;
        }
        
        blockquote {
            margin: 4px 0;
            padding-left: 8px;
            border-left: 1px solid #333333;
            color: #cccccc;
        }
        
        strong, b { color: #ffffff; }
        em, i { color: #cccccc; }
        
        a { color: #ffffff; text-decoration: underline; }
        </style>
        """
        
        full_html = f"{css}{html}"
        self.setHtml(full_html)
