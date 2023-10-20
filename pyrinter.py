import socket

from flask import Flask, request, jsonify
import cups
from zeroconf import ServiceInfo, Zeroconf
import os
from loguru import logger
import requests
from threading import Thread
import time
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize CUPS connection
conn = cups.Connection()

# Discord webhook URLs
webhook_urls = os.getenv("DISCORD_WEBHOOK_URLS").split(',')

# Printer stub name for selecting the correct printer
PRINTER_STUB_NAME = os.getenv("PRINTER_STUB_NAME")

# Initialize logger
logger.add("all_logs.log", rotation="10 MB")
logger.add("error_logs.log", rotation="1 MB", level="ERROR")


def send_discord_webhook(content, embeds):
    for url in webhook_urls:
        requests.post(url, json={"content": content, "embeds": embeds})


def find_local_printer():
    printers = conn.getPrinters()
    valid_printers = [printer for printer in printers if printers[printer]["printer-state"] == 3]

    if PRINTER_STUB_NAME:
        for printer in valid_printers:
            if PRINTER_STUB_NAME in printer:
                return printer

    return valid_printers[0] if valid_printers else None


printer_name = find_local_printer()

if printer_name is None:
    logger.critical("No local printer found.")
    send_discord_webhook("FATAL: No local printer found.", [])
    exit(1)


@app.route('/print', methods=['POST'])
def print_file():
    try:
        file = request.files['file']
        if file:
            # Save the file temporarily
            file_path = "/tmp/" + file.filename
            file.save(file_path)

            # Print the file
            job_id = conn.printFile(printer_name, file_path, "Print Job", {})

            # Remove the temporary file
            os.remove(file_path)

            logger.info(f"Print job {job_id} started for file {file.filename}")

            # Send Discord webhook for job started
            send_discord_webhook("", [
                {
                    "title": "New Print Job",
                    "description": f"Job ID: {job_id}\nFile: {file.filename}\nTimestamp: {time.ctime()}",
                    "color": 3447003  # Blue color
                }
            ])

            return jsonify({"status": "success", "job_id": job_id})
        else:
            logger.error("No file provided for printing.")
            return jsonify({"status": "failure", "message": "No file provided"}), 400
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"status": "failure", "message": str(e)}), 500


def register_zeroconf_service():
    zeroconf = Zeroconf()
    service_info = ServiceInfo(
        "_ipp._tcp.local.",
        "My WiFi Printer._ipp._tcp.local.",
        addresses=[socket.inet_aton("192.168.1.2")],
        port=5000,
        properties={"path": "/"},
    )
    zeroconf.register_service(service_info)


if __name__ == '__main__':
    # Run Zeroconf service registration in a separate thread
    zeroconf_thread = Thread(target=register_zeroconf_service)
    zeroconf_thread.daemon = True
    zeroconf_thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=9669)
