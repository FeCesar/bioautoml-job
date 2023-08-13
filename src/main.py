from modules.consumers.processes_consumer import start_consume
import subprocess

subprocess.call("source /etc/environment")
start_consume()
