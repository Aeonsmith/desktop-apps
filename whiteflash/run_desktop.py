"""
Desktop Native Window Launcher for Whiteflash Shader Engine
"""

import os
import sys
import threading
import http.server
import functools
import webview

def get_dist_dir():
    if getattr(sys, 'frozen', False):
        possible_dirs = [
            os.path.join(getattr(sys, '_MEIPASS', ''), 'dist_web'),
            getattr(sys, '_MEIPASS', None),
            os.path.join(os.path.dirname(sys.executable), 'dist_web'),
            os.path.dirname(sys.executable),
            os.path.join(os.path.dirname(sys.executable), '_internal', 'dist_web'),
            os.path.join(os.path.dirname(sys.executable), '_internal'),
        ]
        for d in possible_dirs:
            if d and os.path.exists(os.path.join(d, 'index.html')):
                return d
        return os.path.dirname(sys.executable)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    for d in [os.path.join(base_dir, 'dist_web'), os.path.join(base_dir, 'dist'), base_dir]:
        if os.path.exists(os.path.join(d, 'index.html')):
            return d
    return base_dir

def main():
    dist_dir = get_dist_dir()

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=dist_dir)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    port = server.server_address[1]

    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    url = f"http://127.0.0.1:{port}/index.html"
    window = webview.create_window(
        title="Whiteflash :: Real-Time ThreeJS Shader Art Engine",
        url=url,
        width=1100,
        height=800,
        min_size=(850, 600),
        background_color="#000000"
    )
    webview.start()
    server.shutdown()

if __name__ == "__main__":
    main()
