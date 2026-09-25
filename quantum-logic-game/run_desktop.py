"""
Desktop Native Window Launcher for Quantum Logic Circuit Hacker
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
    
    # Custom Silent HTTP Request Handler
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=base_dir)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    port = server.server_address[1]
    
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    
    url = f"http://127.0.0.1:{port}/index.html"
    window = webview.create_window(
        title="LogicCore :: Quantum Circuit Hacker",
        url=url,
        width=1100,
        height=800,
        min_size=(850, 600),
        background_color="#0a0f1e"
    )
    webview.start()
    server.shutdown()

if __name__ == "__main__":
    main()
