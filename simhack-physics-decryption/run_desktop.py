"""
Desktop Native Window Launcher for SimHack Physics Decryption
"""

import os
import sys
import threading
import http.server
import functools
import webview

def get_base_dir():
    if getattr(sys, 'frozen', False):
        possible_dirs = [
            getattr(sys, '_MEIPASS', None),
            os.path.dirname(sys.executable),
            os.path.join(os.path.dirname(sys.executable), '_internal'),
            os.path.join(getattr(sys, '_MEIPASS', ''), '_internal') if hasattr(sys, '_MEIPASS') else None,
        ]
        for d in possible_dirs:
            if d and os.path.exists(os.path.join(d, 'index.html')):
                return d
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def main():
    base_dir = get_base_dir()
    
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=base_dir)
    server = http.server.ThreadingHTTPServer(('*********', 0), handler)
    port = server.server_address[1]
    
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    
    url = f"http://*********:{port}/index.html"
    window = webview.create_window(
        title="SimHack :: Physics Decryption Terminal (Enhanced Edition)",
        url=url,
        width=1150,
        height=820,
        min_size=(900, 650),
        background_color="#050a0f"
    )
    webview.start()
    server.shutdown()

if __name__ == "__main__":
    main()
