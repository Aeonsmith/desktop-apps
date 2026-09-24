"""
Desktop Native Window Launcher for TikTok Tac (Cuffbreaker)
"""

import os
import sys
import threading
import http.server
import functools
import webview

def get_web_dir():
    if getattr(sys, 'frozen', False):
        possible_dirs = [
            os.path.join(getattr(sys, '_MEIPASS', ''), 'web'),
            getattr(sys, '_MEIPASS', None),
            os.path.join(os.path.dirname(sys.executable), 'web'),
            os.path.dirname(sys.executable),
            os.path.join(os.path.dirname(sys.executable), '_internal', 'web'),
            os.path.join(os.path.dirname(sys.executable), '_internal'),
        ]
        for d in possible_dirs:
            if d and os.path.exists(os.path.join(d, 'index.html')):
                return d
        return os.path.dirname(sys.executable)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    web_dir = os.path.join(base_dir, "web")
    if not os.path.exists(web_dir):
        web_dir = base_dir
    return web_dir

def main():
    web_dir = get_web_dir()
        
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=web_dir)
    server = http.server.ThreadingHTTPServer(('*********', 0), handler)
    port = server.server_address[1]
    
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    
    url = f"http://*********:{port}/index.html"
    window = webview.create_window(
        title="TikTok()Tac - Tactical Cuffbreaker Game Engine",
        url=url,
        width=1000,
        height=750,
        min_size=(800, 600),
        background_color="#0d1117"
    )
    webview.start()
    server.shutdown()

if __name__ == "__main__":
    main()
