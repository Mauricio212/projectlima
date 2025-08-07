import re
with open("web_app_professional.py", "r") as f: content = f.read()
login = "\n@app.route(\"/api/auth/login\", methods=[\"POST\"])\ndef demo_login():\n    data = request.get_json()\n    if data.get(\"email\") == \"demo@projectlima.com\" and data.get(\"password\") == \"demo123\":\n        session[\"user_id\"] = \"demo\"\n        return jsonify({\"status\": \"success\", \"redirect\": \"/dashboard\"})\n    return jsonify({\"status\": \"error\", \"message\": \"Invalid credentials\"}), 401\n"
content = re.sub(r"(if __name__ == \"__main__\":)", login + r"\1", content)
with open("web_app_professional.py", "w") as f: f.write(content)
