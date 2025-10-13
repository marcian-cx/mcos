"""
Markdown Editor Service

Handles markdown editing operations like task management, indentation, 
and line continuation in a clean, testable way.
"""

import re
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class LineInfo:
    """Information about a line of text"""
    text: str
    indent: str
    is_task: bool
    task_status: Optional[str] = None
    task_content: Optional[str] = None
    is_list: bool = False
    list_content: Optional[str] = None


class MarkdownEditorService:
    """Service for handling markdown editing operations"""
    
    def __init__(self):
        self.tab_size = 4  # Number of spaces for indentation
    
    def parse_line(self, line: str) -> LineInfo:
        """Parse a line and return information about its structure"""
        
        # Extract indentation
        indent_match = re.match(r'^(\s*)', line)
        indent = indent_match.group(1) if indent_match else ""
        
        # Check for task
        task_match = re.match(r'^(\s*)-\s+\[([ x])\]\s+(.*)$', line)
        if task_match:
            return LineInfo(
                text=line,
                indent=indent,
                is_task=True,
                task_status=task_match.group(2),
                task_content=task_match.group(3)
            )
        
        # Check for regular list
        list_match = re.match(r'^(\s*)-\s+(.*)$', line)
        if list_match:
            return LineInfo(
                text=line,
                indent=indent,
                is_task=False,
                is_list=True,
                list_content=list_match.group(2)
            )
        
        # Regular line
        return LineInfo(
            text=line,
            indent=indent,
            is_task=False,
            is_list=False
        )
    
    def toggle_task_status(self, line: str) -> Optional[str]:
        """Toggle a task's completion status. Returns new line or None if not a task."""
        line_info = self.parse_line(line)
        
        if not line_info.is_task:
            return None
        
        new_status = 'x' if line_info.task_status == ' ' else ' '
        return f"{line_info.indent}- [{new_status}] {line_info.task_content}"
    
    def handle_enter_key(self, current_line: str) -> Optional[str]:
        """
        Handle Enter key press on a line. Returns the new line to insert or None.
        """
        line_info = self.parse_line(current_line)
        
        # If it's a task with content, create a new empty task
        if line_info.is_task and line_info.task_content and line_info.task_content.strip():
            return f"{line_info.indent}- [ ] "
        
        # If it's a list item with content, create a new empty list item
        if line_info.is_list and line_info.list_content and line_info.list_content.strip():
            return f"{line_info.indent}- "
        
        # If it's an empty task or list item, don't continue (let user exit the list)
        if (line_info.is_task and not line_info.task_content.strip()) or \
           (line_info.is_list and not line_info.list_content.strip()):
            return None
        
        return None
    
    def handle_tab_key(self, line: str, shift_pressed: bool = False) -> str:
        """
        Handle Tab key press. Indent or dedent the line.
        
        Args:
            line: The current line text
            shift_pressed: True if Shift+Tab (dedent), False for Tab (indent)
        
        Returns:
            The modified line
        """
        if shift_pressed:
            return self._dedent_line(line)
        else:
            return self._indent_line(line)
    
    def _indent_line(self, line: str) -> str:
        """Add indentation to a line"""
        line_info = self.parse_line(line)
        
        # Add tab_size spaces to the beginning
        spaces = " " * self.tab_size
        
        if line_info.is_task:
            # For tasks, add indentation before the dash
            return f"{line_info.indent}{spaces}- [{line_info.task_status}] {line_info.task_content}"
        elif line_info.is_list:
            # For lists, add indentation before the dash
            return f"{line_info.indent}{spaces}- {line_info.list_content}"
        else:
            # For regular lines, just add indentation at the beginning
            return f"{spaces}{line}"
    
    def _dedent_line(self, line: str) -> str:
        """Remove indentation from a line"""
        line_info = self.parse_line(line)
        
        # Remove up to tab_size spaces from the beginning
        if len(line_info.indent) >= self.tab_size:
            new_indent = line_info.indent[self.tab_size:]
        else:
            new_indent = ""
        
        if line_info.is_task:
            return f"{new_indent}- [{line_info.task_status}] {line_info.task_content}"
        elif line_info.is_list:
            return f"{new_indent}- {line_info.list_content}"
        else:
            # For regular lines, remove spaces from the beginning
            if line.startswith(" " * self.tab_size):
                return line[self.tab_size:]
            elif line.startswith(" "):
                # Remove whatever spaces exist
                return line.lstrip(" ")
            else:
                return line
    
    def convert_line_to_task(self, line: str) -> str:
        """Convert a regular line or list item to a task"""
        line_info = self.parse_line(line)
        
        if line_info.is_task:
            return line  # Already a task
        elif line_info.is_list:
            return f"{line_info.indent}- [ ] {line_info.list_content}"
        else:
            # Convert regular line to task
            content = line.strip()
            return f"{line_info.indent}- [ ] {content}"
    
    def convert_line_to_list(self, line: str) -> str:
        """Convert a regular line or task to a list item"""
        line_info = self.parse_line(line)
        
        if line_info.is_list and not line_info.is_task:
            return line  # Already a list
        elif line_info.is_task:
            return f"{line_info.indent}- {line_info.task_content}"
        else:
            # Convert regular line to list
            content = line.strip()
            return f"{line_info.indent}- {content}"
