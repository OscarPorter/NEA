### Minecraft Maze Generator

A small Pygame project that lets you draw a maze layout, generate a maze, and export it as a Minecraft-compatible structure file.

Watch a demonstration [here.](https://www.youtube.com/watch?v=VPn8d_i7gG8)

### Install

Run:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python main.py
```

### Features

- Draw a maze on a grid
- Generate a procedural maze
- Save generated output as:
  - Litematic file
  - MCFunction file

### Notes

This project uses:
- `pygame` for the interface and drawing
- `litemapy` for exporting Litematic structures
- `tkinter.filedialog` for the file save prompt
