"""
京剧数据可视分析系统 - 本地开发服务器
Usage: python serve.py
然后浏览器打开 http://localhost:8080
"""
import http.server
import socketserver
import os

PORT = 8888

os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.json': 'application/json',
    '.csv': 'text/csv',
})

print(f"""
╔═══════════════════════════════════════╗
║   京剧数据可视分析系统               ║
║   Peking Opera Analytics System      ║
╠═══════════════════════════════════════╣
║   服务已启动: http://localhost:{PORT}    ║
║   按 Ctrl+C 停止服务                  ║
╚═══════════════════════════════════════╝
""")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止。")
