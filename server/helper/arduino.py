def send_signal(arduino = None, text=""):
    if arduino is not None and text != "":
        arduino.write((text + "\n").encode())

def send_checkall_signal(arduino = None):
    if arduino is not None:
        send_signal(arduino, "CheckAll")

def send_offall_signal(arduino = None):
    if arduino is not None:
        send_signal(arduino, "OffAll")

def send_cell_signal(arduino = None, module = "", quantity = 0 , mode = -1):
    if arduino is not None:
        text = f"{module}|{quantity}|{mode}"
        send_signal(arduino, text)