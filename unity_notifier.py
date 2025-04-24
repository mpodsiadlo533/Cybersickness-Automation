import requests

class UnityNotifier:
    '''
    base_url="http://192.168.0.66:5001"
    Tutaj jest adres IP komputera z Unity.
    Domyślnie powinien być `localhost`, bo Unity i GUI działają na tym samym komputerze.
    '''
    def __init__(self, base_url="http://192.168.0.66:5001"):
        self.base_url = base_url

    def start_scenario(self, scenario_number):
        try:
            scenario_number = int(scenario_number)
            if scenario_number == 0:
                print("[Notifier] Scenario 0 (reference) — no START sent to Unity.")
                return

            response = requests.post(
                f"{self.base_url}/start",
                data=str(scenario_number),
                headers={"Content-Type": "text/plain"}
            )
            print(f"[Notifier] START sent: {scenario_number}, Response: {response.status_code}")

        except ValueError:
            print(f"[Notifier] Invalid scenario number: {scenario_number}")
        except requests.exceptions.RequestException as e:
            print(f"[Notifier] Failed to send START: {e}")


    def stop_scenario(self, scenario_number):
        try:
            scenario_number = int(scenario_number)
            if scenario_number == 0:
                print("[Notifier] Scenario 0 (reference) — no STOP sent to Unity.")
                return

            response = requests.post(
                f"{self.base_url}/stop",
                data=str(scenario_number),
                headers={"Content-Type": "text/plain"}
            )
            print(f"[Notifier] STOP sent: {scenario_number}, Response: {response.status_code}")

        except ValueError:
            print(f"[Notifier] Invalid scenario number: {scenario_number}")
        except requests.exceptions.RequestException as e:
            print(f"[Notifier] Failed to send STOP: {e}")


    def hard_stop(self):
        try:
            response = requests.post(f"{self.base_url}/hardstop")
            print(f"[Notifier] HARD STOP sent, Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[Notifier] Failed to send HARD STOP: {e}")
