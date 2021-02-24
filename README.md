![GitHub Workflow Status](https://img.shields.io/github/workflow/status/s3rius/s3wm/Release%20s3wm?style=for-the-badge)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/s3wm?style=for-the-badge)](https://pypi.org/project/s3wm)
[![PyPI](https://img.shields.io/pypi/v/s3wm?style=for-the-badge)](https://pypi.org/project/s3wm)

# S3WM

🛠️⚙️This is a WIP project. Don't beleive in README ⚙️🛠️


This project is a yet another `Window manager`.

Main Idea behind this project is `modularity` and
window manager `configuration in Python`.

You can even `bind a python function` to some key combination.

## Configuration
Main configuration file must be located in `$HOME/.s3wm_conf.py`.
S3WM configuration examples can be found in examples folder.

## How to Run/test

```bash
# start nested X11 session with Xephyr
Xephyr :1 +xinerama -screen 1280x720 -reset -terminate &
# Run it with proper DISPLAY ENV
DISPLAY=:1.0 s3wm
# To grab or release host keys press `Ctrl` + `Shift`
```
