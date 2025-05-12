from keep_alive import keep_alive
import threading
from macha import main as run_bot

keep_alive()
threading.Thread(target=run_bot).start()
