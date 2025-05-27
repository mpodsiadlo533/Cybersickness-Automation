import pyautogui
import time
import threading
import pygetwindow as gw
from flask import Flask, request, jsonify

app = Flask(__name__)

def focus_acqknowledge():
    try:
        windows = gw.getWindowsWithTitle("AcqKnowledge")
        if not windows:
            print("[MarkerListener] AcqKnowledge window not found.")
            return False
        win = windows[0]
        win.activate()
        print("[MarkerListener] AcqKnowledge window focused.")
        time.sleep(0.3)
        return True
    except Exception as e:
        print(f"[MarkerListener] Error focusing AcqKnowledge: {e}")
        return False

def send_marker(marker_type):
    if focus_acqknowledge():
        pyautogui.press('esc')
        print(f"[MarkerListener] ESC sent for: {marker_type}")
    else:
        print(f"[MarkerListener] Cannot send marker, AcqKnowledge not focused.")

def handle_scenario(scenario, duration):
    print(f"[MarkerListener] SCENARIO {scenario} START, duration {duration}s")
    send_marker(f"START {scenario}")
    time.sleep(duration)
    send_marker(f"STOP {scenario}")
    print(f"[MarkerListener] SCENARIO {scenario} END")

@app.route('/scenario', methods=['POST'])
def scenario():
    data = request.json
    scenario_number = data.get("scenario")
    duration = data.get("duration")

    if scenario_number is None or duration is None:
        return jsonify({"error": "Missing scenario or duration"}), 400

    # uruchamiamy w tle, żeby Flask nie był zablokowany
    threading.Thread(target=handle_scenario, args=(scenario_number, int(duration))).start()
    return jsonify({"status": "Scenario started", "scenario": scenario_number, "duration": duration})


@app.route('/hardstop', methods=['POST'])
def hardstop():
    if focus_acqknowledge():
        pyautogui.hotkey('ctrl','space')
        print(f"[MarkerListener] ctrl space sent for: {marker_type}")
    else:
        print(f"[MarkerListener] Cannot send marker, AcqKnowledge not focused.")

if __name__ == "__main__":
    print("Marker listener running on http://0.0.0.0:5050")
    print("Waiting for POST /scenario {scenario, duration}...")
    app.run(host='0.0.0.0', port=5050)
