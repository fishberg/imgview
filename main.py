import base64
from pathlib import Path
from nicegui import ui
import os

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg'}
MIME = {'png': 'png', 'jpg': 'jpeg', 'jpeg': 'jpeg', 'gif': 'gif', 'webp': 'webp', 'bmp': 'bmp', 'svg': 'svg+xml'}

POLL_OPTIONS = {
    '0.1s': 0.1,
    '0.5s': 0.5,
    '1s': 1.0,
    '2s': 2.0,
    '5s': 5.0,
    '10s': 10.0,
}


def find_last_image(folder: str) -> str | None:
    p = Path(folder)
    if not p.is_dir():
        return None
    images = sorted(
        f for f in p.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    )
    return str(images[-1]) if images else None


def refresh_image():
    path = find_last_image(folder_input.value)
    if path:
        ext = Path(path).suffix.lower().lstrip('.')
        mime = MIME.get(ext, 'jpeg')
        data = base64.b64encode(Path(path).read_bytes()).decode()
        img_html.content = (
            f'<img src="data:image/{mime};base64,{data}" '
            f'style="max-width:100%; max-height:100%; object-fit:contain; display:block;">'
        )
        status.set_text(f'Showing: {Path(path).name}')
    else:
        img_html.content = ''
        status.set_text('No images found in folder.')


def on_poll_change(e):
    timer.interval = POLL_OPTIONS[e.value]


ui.add_head_html('<style>html, body { height: 100%; margin: 0; padding: 0; overflow: hidden; }</style>')

with ui.column().classes('w-full items-center gap-4 p-6').style('height: 100%; box-sizing: border-box; overflow: hidden;'):
    ui.label('Image Viewer').classes('text-2xl font-bold')

    with ui.row().classes('w-full max-w-2xl items-center gap-2'):
        folder_input = ui.input(
            label='Folder path',
            placeholder='/path/to/folder',
            value=os.path.expanduser('imgs'),
        ).classes('flex-1')
        ui.select(
            list(POLL_OPTIONS.keys()),
            value='1s',
            label='Poll interval',
            on_change=on_poll_change,
        ).classes('w-24')

    status = ui.label('').classes('text-sm text-gray-500')

    img_html = ui.html('').style(
        'flex: 1; min-height: 0; width: 100%; '
        'display: flex; align-items: center; justify-content: center; overflow: hidden;'
    )

timer = ui.timer(interval=1.0, callback=refresh_image)

ui.run(title='Image Viewer', show=False)
