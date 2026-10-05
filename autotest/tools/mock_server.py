"""Mock 服务器 —— 模拟外部设备/第三方依赖，解耦测试"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/mock/device/status":
            self._json(200, {"device_id": "MOCK_DEV", "status": "online", "battery": 85})
        elif self.path == "/mock/thirdparty/report":
            self._json(200, {"report_url": "https://mock.example.com/r/123.pdf"})
        else:
            self._json(404, {"error": "not found"})

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # 静默日志

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9999), MockHandler)
    print("Mock server running on http://localhost:9999")
    server.serve_forever()
