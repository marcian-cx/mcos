import re
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from dateutil.parser import parse as parse_date

@dataclass
class Task:
    text: str
    completed: bool
    due_date: Optional[datetime] = None
    tags: List[str] = None
    line_number: int = 0
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

def parse_task_line(line: str, line_number: int = 0) -> Optional[Task]:
    task_pattern = r'^- \[([ x])\] (.+)$'
    match = re.match(task_pattern, line.strip())
    
    if not match:
        return None
    
    completed = match.group(1) == 'x'
    text = match.group(2)
    
    due_date = None
    due_match = re.search(r'!due\(([^)]+)\)', text)
    if due_match:
        try:
            due_date = parse_date(due_match.group(1))
        except:
            pass
    
    tags = re.findall(r'@(\w+)', text)
    
    return Task(
        text=text,
        completed=completed,
        due_date=due_date,
        tags=tags,
        line_number=line_number
    )

def find_tasks_in_text(text: str) -> List[Task]:
    tasks = []
    for i, line in enumerate(text.split('\n'), 1):
        task = parse_task_line(line, i)
        if task:
            tasks.append(task)
    return tasks
