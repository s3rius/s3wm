# S3WM

🛠️⚙️This is a WIP project. Don't beleive in README ⚙️🛠️


This project is a yet another `Window manager`.

Main Idea behind this project is `modularity` and
window manager `configuration in Python`.

You can even `bind a python function` to some key combination.

## How to Run/test

```bash
# start nested X11 session with Xephyr
Xephyr :1 +xinerama -screen 1280x720 -reset -terminate &
# Run it with proper DISPLAY ENV
DISPLAY=:1.0 s3wm
# To grab or release host keys press `Ctrl` + `Shift`
```
