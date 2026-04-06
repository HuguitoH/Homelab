#!/usr/bin/env python3
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

NTFY_URL = "https://ntfy.hugohhm.dev/hugohhm-homelab"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length))
            alerts = body.get("alerts", [])

            for alert in alerts:
    alert_status = alert.get("status", "firing")
    
    # Solo enviar cuando hay alerta, ignorar resolved
    if alert_status != "firing":
        continue
        
    name = alert.get("labels", {}).get("alertname", "Alert")
    summary = alert.get("annotations", {}).get("summary", name)
    description = alert.get("annotations", {}).get("description", "")
    message = f"[ALERT] {summary} - {description}"
    
    print(f"Sending to Ntfy: {message}")
    
    req = urllib.request.Request(
        NTFY_URL,
        data=message.encode("utf-8"),
        headers={
            "Content-Type": "text/plain",
            "User-Agent": "curl/8.5.0"
        }
    )
    urllib.request.urlopen(req)
    print("Sent successfully")

        except Exception as e:
            print(f"Error: {e}")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9095), WebhookHandler)
    print("Bridge running on port 9095")
    server.serve_forever()
