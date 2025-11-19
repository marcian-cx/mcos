# **Mission Command OS (MCOS)**

## **Quick Start Commands**

### **Development Setup**
```bash
# Clone and setup
git clone <repository-url>
cd mcos

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
./launch.sh

### **Build & Package**
```bash
# Create app icon (one-time setup)
python create_icon.py
iconutil -c icns mcos.iconset

# Build standalone app
source .venv/bin/activate
pyinstaller mcos.spec --clean

# Quick rebuild during development
./rebuild_app.sh
```

### **Daily Use Setup**
```bash
# Setup for daily use (creates vault, installs app, desktop launcher)
./setup_daily_use.sh

# Manual vault creation
mkdir -p ~/mcos_vault/{Inbox,Projects,Goals,Reviews,Calendar,Notes}
cp -r demo_vault/* ~/mcos_vault/

# Install to Applications folder
cp -r dist/MCOS.app /Applications/
```

### **Launch Commands**
```bash
# Development mode
python -m mcos.app --vault ~/mcos_vault

# Standalone app (after building)
open dist/MCOS.app

# From Applications (after install)
open /Applications/MCOS.app

# Desktop launcher (after setup)
~/Desktop/Launch\ MCOS.command
```

### **Export & Distribution**
```bash
# Create distributable zip
zip -r MCOS-$(date +%Y%m%d).zip dist/MCOS.app

# Create vault backup
zip -r vault-backup-$(date +%Y%m%d).zip ~/mcos_vault

# Clean build artifacts
rm -rf build/ dist/

# Full clean rebuild
rm -rf build/ dist/ && pyinstaller mcos.spec --clean
```

### **Development Workflow**
```bash
# Quick development cycle
./rebuild_app.sh                    # Rebuild and optionally install
python -m pytest mcos/tests/        # Run tests
python -m mcos.app --vault ./demo_vault  # Test run

# Check dependencies
pip list
pip check

# Update requirements
pip freeze > requirements.txt
```

### **Troubleshooting & Maintenance**
```bash
# Clean everything and start fresh
rm -rf .venv build/ dist/ mcos.iconset/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Fix icon issues
python create_icon.py
iconutil -c icns mcos.iconset

# Check PyInstaller issues
pyinstaller mcos.spec --clean --debug all

# Test vault structure
ls -la ~/mcos_vault/
ls -la demo_vault/

# Remove and reinstall app
rm -rf /Applications/MCOS.app
cp -r dist/MCOS.app /Applications/

# Check app permissions (macOS)
xattr -d com.apple.quarantine /Applications/MCOS.app
```

### **System Requirements**
- **macOS**: 10.14+ (for PyQt6 compatibility)
- **Python**: 3.9+ (tested with 3.9)
- **Dependencies**: See `requirements.txt`
- **Disk Space**: ~200MB for built app bundle

### **Keyboard Shortcuts**

#### **File Operations (Sidebar)**
| Shortcut | Action |
|----------|--------|
| `Enter` | Open selected file/folder |
| `Ctrl+N` | Create new markdown file |
| `Ctrl+Shift+N` | Create new CSV file |
| `Ctrl+D` | Delete selected file |
| `Ctrl+R` | Rename selected file |

#### **Editor**
| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save current file |
| `Ctrl+T` | Toggle task checkbox (- [ ] ↔ - [x]) |
| `Enter` | Auto-continue checkboxes and lists |
| `Tab` | Indent line or selection |
| `Shift+Tab` | Dedent line or selection |

#### **CSV Tables**
| Navigation | Action |
|----------|--------|
| Click cell | Edit cell content |
| Double-click header | Edit column name |
| `↑` from first row | Edit column header |
| `→` from last column | Auto-creates new column |
| `↓` from last row | Auto-creates new row |
| `←` from empty column | Auto-deletes empty column |
| `↑` from empty row | Auto-deletes empty row |
| Arrow keys | Navigate between cells |
| `Ctrl+Shift+V` | Toggle between table and raw CSV view |

#### **Navigation**
| Shortcut | Action |
|----------|--------|
| `↑/↓` | Navigate sidebar tree |
| `←/→` | Collapse/expand folders |
| `Ctrl+Left` | Focus sidebar |
| `Ctrl+Right` | Focus editor |
| `Enter` | Open file (from sidebar) |

#### **System**
| Shortcut | Action | Status |
|----------|--------|--------|
| `Ctrl+K` | Show keyboard shortcuts |
| `Ctrl+F` | Find in file | 🚧 Planned |
| `Ctrl+H` | Find & replace | 🚧 Planned |
| `Alt+Left` | Navigate back | 🚧 Planned |
| `Ctrl+D` | Dashboard mode | 🚧 Planned |
| `F9` | AI hook (selected text) | 🚧 Planned |

#### **Task Management**
| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | Toggle task: `- [ ]` ↔ `- [x]` |
| `Space` | Toggle task on current line |

**Note**: All shortcuts use `Ctrl` on macOS (maps to `Cmd` key automatically via PyQt6).

### **Plain Text Markdown Editing**

MCOS features a **clean, distraction-free markdown editor**:

#### **Features:**
- **Pure plain text editing** with monospace font
- **Smart task management**: 
  - `Ctrl+T` toggles checkboxes `- [ ]` ↔ `- [x]`
  - `Enter` on checkbox creates new checkbox
  - `Tab` indents for nested checkboxes
- **Intelligent indentation**: Tab/Shift+Tab works on single lines or selections
- **Clean navigation**: `Ctrl+Left/Right` to switch between sidebar and editor
- **Auto-continuation**: Enter continues lists and tasks automatically
- **Keyboard-driven**: All operations via shortcuts
- **E-ink optimized**: Pure black/white, crisp text
- **Crash-safe saves**: Temporary files with timestamps
- **Clean architecture**: Services handle logic, UI handles presentation

**Smart, reliable markdown editing with proper task management and nested structures.**

---

# **Project Summary**

  

## **Vision**

  

Mission Command OS (MCOS) is a **local-first, distraction-free life management system**.

It combines the durability of plain text with the clarity of a **monospace, hacker-aesthetic interface**, giving you a personal command center for tasks, goals, reviews, and calendars—without cloud lock-in, bloat, or digital noise.

**Design Philosophy**: Pure black/white, monospace everything, e-ink optimized, keyboard-driven, no fluff.

  

MCOS is designed to be **agnostic software**: it runs on laptops, Raspberry Pis, or any small computer. Hardware like the **MCDeck** (dedicated e-ink device) will later enforce strict usage modes, but MCOS itself stays mode-neutral.

---

## **Core Principles**

- **Plain Text Backbone**: All data stored as Markdown + CSV, Obsidian-compatible.
    
- **Offline-First**: Works without internet; Proton Drive handles encrypted sync.
    
- **Minimal UI**: One focused app (sidebar + editor + dashboards).
    
- **Secure & Ownable**: You own the files, no vendor lock-in.
    
- **Extendable**: Built light, with room for dashboards, reviews, calendars, and AI hooks.
    

---

## **Features (MVP → Future)**

  

### **MVP**

- Markdown editor with sidebar vault tree.
    
- GTD tasks (- [ ], !due(...), @tags) + inbox count.
    
- CSV-based goal tracker with ASCII progress bars.
    
- Weekly/quarterly review templates.
    
- Dashboard: inbox, goal progress, upcoming calendar items, overdue tasks.
    
- File-based calendar import (.ics) → ASCII agenda.
    
- Proton Drive sync via local folder.
    

  

### **Future**

- Proton Calendar API integration.
    
- Taskwarrior bridge (recurrence, scheduling).
    
- ASCII charts and richer dashboards.
    
- TUI mode (ncurses).
    
- AI hook: summon analysis/summaries, responses saved to .ai.md.
    

---

## **Development Roadmap**

1. **Core editor + vault access** (sidebar + markdown editor).
    
2. **Task parsing + inbox logic**.
    
3. **Goal tracking via CSV**.
    
4. **Weekly/quarterly review support**.
    
5. **Dashboards (inbox, goals, calendar)**.
    
6. **Calendar import (.ics)**.
    
7. **Search & quick navigation**.
    
8. **Sync discipline (Proton, Git, exports)**.
    
9. **Optional AI hook (stub only)**.
    
10. **Packaging for Linux/macOS** (portable binaries).
    

---

## **Hardware Context**

- **MCOS = Software layer**.
    
- **MCDeck = Dedicated e-ink hardware** that runs MCOS in enforced “WRITE” or “PLAN” boot modes (strict separation by reboot).
    
- **PocketDeck = Future PDA form factor** for ultra-portable capture.
    

---

## **Why It Matters**

  

Modern tools scatter attention. MCOS is built from the ground up to resist that:

- It’s **deep, slow, deliberate**—aligned with _The Shallows_ (Nicholas Carr).
    
- It’s **modular**—a software core that can live in different hardware shells.
    
- It’s **legacy-proof**—files readable in 50 years, outside any app.
    

  

This is not “yet another productivity app.” It’s a **Warrior King’s command system**: local, sovereign, distraction-free.

---

### TODO


# **MCOS Development Order**

1. **Laptop Prototype** — build the baseline app: sidebar, editor, dashboard.
    
2. Add **indexer + SQLite** — structured queries instead of regex.
    
3. Add **calendar import (read-only)** + **Taskwarrior bridge**.
    
4. Port to **Pi + e-ink** (refresh control, performance tuning).
    
5. Add **sync discipline** + optional **AI hook**.
    
6. Only then: **battery + enclosure**.
    

---

# **1. Laptop Prototype**

  

## ~~**Phase 0 — Foundations**~~ ✅

- ~~Repo setup:~~
    
    - ~~Root folder: mcos/ package, requirements.txt, README.md.~~
        
    - ~~Keep .venv/ outside sync (e.g., ~/dev/mcos).~~
        
    
- ~~Dependencies:~~
    
    - ~~PyQt6, pyyaml, pandas, python-dateutil, icalendar, pytest.~~
        
    
- ~~Vault layout (Obsidian-compatible, Proton-syncable):~~
    

```
/Vault
  /Inbox
  /Projects
  /Goals
  /Reviews
  /Calendar
  /Notes
```

-   
    
- ~~Config file (~/.mcos.toml):~~ (deferred)
    
    - vault_path = "~/ProtonSync/mcos_vault"
        
    - dashboard_defaults = ["inbox", "goals"]
        
    - keymap = "default"
        
    

  

✅ **QA:**

- ~~python -m mcos.app --vault ./demo_vault opens, sidebar + editor appear.~~
    
- ~~Able to edit and save inbox.md without errors.~~
    

---

## ~~**Phase 1 — Core Editor + Vault Access**~~ ✅

- ~~Sidebar:~~
    
    - ~~Tree view of vault (dirs + .md files) - monospace, e-ink optimized.~~
        
    - ~~Expand/collapse with ASCII arrows.~~
        
    - ~~Enter key opens files (keyboard-only navigation).~~
        
    
- ~~Editor:~~
    
    - ~~Monospace font (Monaco/Menlo/Consolas) - HACKER AESTHETIC.~~
        
    - ~~Save (Ctrl+S).~~
        
    - ~~Crash-safe temp saves (.tmp with timestamp).~~
        
    - ~~Markdown preview toggle (Ctrl+Shift+V) with ASCII-style formatting.~~
        
    - ~~E-ink optimized: pure black/white, no borders, crisp lines.~~
        
    
- ~~Status bar:~~
    
    - ~~Show file path, *modified marker in monospace.~~
        
    

  

✅ **QA:**

- ~~Open demo_vault/inbox.md with Enter key, edit text, save.~~
    
- ~~Close + reopen app, changes persist.~~
    
- ~~Ctrl+Shift+V toggles between edit/preview with ASCII task formatting.~~
    
- ~~Pure monospace hacker aesthetic: [ ] → [X], [DUE:3d], @tags.~~
    

---

## **Phase 2 — Task & GTD Conventions** 🚧

- ~~Task parsing:~~
    
    - ~~- [ ] unchecked~~
        
    - ~~- [x] checked~~
        
    - ~~!due(YYYY-MM-DD) → parse with dateutil.~~
        
    - ~~@tags.~~
        
    
- ~~Editor behavior:~~
    
    - ~~Press space on - [ ] line toggles → - [x].~~
        
    
- Dashboard-lite:
    
    - Count unchecked tasks in /Inbox/*.md. (pending)
        
    

  

✅ **QA:**

- Create 3 tasks in inbox.md, dashboard shows "Inbox: 3".
    
- Toggle one with spacebar → count drops to 2.
    
- Due date tasks show correctly parsed in log/console.
    

---

## **Phase 3 — Goal Tracking (CSV)**

- /Goals/goals.csv schema:
    

```
goal_id,category,target,progress,due_date,status
G1,Fitness,Deadlift 600,550,2025-12-31,active
```

-   
    
- Load into Pandas DataFrame.
    
- Dashboard: ASCII progress bar [#####-----] 55%.
    
- Update inline:
    
    - Editor changes value → save back to CSV.
        
    

  

✅ **QA:**

- Add new goal row → appears in dashboard.
    
- Change progress → ASCII bar updates.
    
- Save → confirm CSV updated on disk.
    

---

## **Phase 4 — Weekly & Quarterly Reviews**

- Templates auto-generated:
    
    - /Reviews/weekly-2025-W39.md
        
    - /Reviews/quarterly-2025-Q4.md
        
    
- Weekly view:
    
    - Pull unfinished tasks from last week (- [ ]).
        
    - Insert checklist into new weekly file.
        
    

  

✅ **QA:**

- Run on Sunday → new weekly review file appears.
    
- Tasks from previous week copied forward.
    
- Quarterly review pulls linked goals.
    

---

## **Phase 5 — Dashboards**

- Press Ctrl+D → Dashboard mode.
    
- Show:
    
    - 📥 Inbox count (open tasks).
        
    - 🎯 Goals (from CSV).
        
    - 📅 Upcoming tasks (!due < 7 days).
        
    - ⏳ Overdue (!due < today).
        
    
- Rendered in editor as read-only Markdown.
    

  

✅ **QA:**

- Press toggle key → dashboard appears.
    
- Values match manual counts in files.
    
- Links in dashboard jump to source notes.
    

---

## **Phase 6 — Calendar Integration**

- Drop .ics into /Calendar.
    
- Parse with icalendar.
    
- Render agenda as ASCII in dashboard:
    

```
09:00  Team Call
11:30  Gym
14:00  Poetry Block
```

-   
    
- Manual .md events exportable to .ics.
    

  

✅ **QA:**

- Add test.ics → events appear.
    
- Add .md event → exported .ics valid (can import to Apple/Google Calendar).
    

---

## **Phase 7 — Search & Navigation**

- Quick switcher (Ctrl+K) → fuzzy filename search.
    
- Find/replace in editor (Ctrl+F, Ctrl+H).
    
- Back nav (Alt+Left).
    

  

✅ **QA:**

- Search “goal” → opens goals.csv.
    
- Replace “2025” → works across note.
    
- Navigate back returns to prior file/position.
    

---

## **Phase 8 — Sync Discipline**

- Vault lives in ~/ProtonSync/mcos/.
    
- Proton handles encrypted sync.
    
- Export command:
    
    - zip vault-YYYYMMDD.zip.
        
    
- Optional auto-commit Git.
    

  

✅ **QA:**

- Modify file locally → change syncs via Proton client.
    
- Run export → zip appears with correct content.
    
- Git auto-commit shows in log.
    

---

## **Phase 9 — AI Hook (Optional Stub)**

- Press F9 → selected text POSTs to stub endpoint.
    
- Save reply as note.ai.md.
    

  

✅ **QA:**

- Select text → response lands in vault.
    
- Offline mode: pressing F9 does nothing, no crash.
    

---

## ~~**Phase 10 — Packaging & Portability**~~ ✅

- ~~CLI flags:~~
    
    - ~~--vault /path/to/vault (auto-detects ~/mcos_vault)~~
        
    - ~~Smart vault discovery and selection~~
        
    
- ~~Package with PyInstaller → MCOS.app bundle.~~
    
- ~~Run binary on clean Mac → works OOTB.~~
    
- ~~Desktop launcher for daily use testing.~~
    

  

✅ **QA:**

- ~~Install with ./setup_daily_use.sh script.~~
    
- ~~Run MCOS.app → sidebar, editor, markdown preview functional.~~
    
- ~~Double-click desktop launcher → opens instantly.~~
    

---

# **Milestones**

- **M1 (2w):** ✅ Sidebar + editor + hacker aesthetic (COMPLETE: monospace, e-ink optimized).
    
- **M2 (4w):** 🚧 Tasks + inbox parsing (CURRENT: spacebar toggle works, need dashboard).
    
- **M3 (6w):** Goals + weekly review.
    
- **M4 (8w):** Dashboards + calendar import.
    
- **M5 (10w):** ✅ Packaging + sync (DONE: .app bundle ready for daily use).
    

---

# **Daily Use Deployment**

See the **Quick Start Commands** section above for all build, setup, and launch commands.

## **What Setup Creates**

- **MCOS.app** → Full macOS application bundle at `dist/MCOS.app`
- **~/mcos_vault** → Your personal vault directory with folder structure
- **Desktop launcher** → `~/Desktop/Launch MCOS.command` for quick access
- **Applications install** → Launch via Spotlight (Cmd+Space "MCOS")

## **Key Features for Daily Use**

- **Vault Persistence**: Remembers your last vault location (stored in `~/.mcos_config.json`)
- **Custom Icon**: Terminal-style MCOS icon with monospace aesthetic  
- **Quick Launch**: Desktop launcher, Spotlight search, or Applications folder
- **Instant Rebuild**: `./rebuild_app.sh` for development iterations

## **File Locations**

- **App Bundle**: `dist/MCOS.app`
- **Your Vault**: `~/mcos_vault` (or your chosen location)
- **Config**: `~/.mcos_config.json` (vault location memory)
- **Desktop Launcher**: `~/Desktop/Launch MCOS.command`

**Perfect for daily test driving to find real-world issues!**
