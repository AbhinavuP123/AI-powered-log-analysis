import datetime
import random
import uuid
import os

def generate_log_entry(level, request_id, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    return f"{timestamp} | {level:5} | {request_id} | {message}\n"

def main():
    log_file = "service.log"
    print(f"Generating realistic service logs in {log_file}...")
    
    levels = ["INFO", "INFO", "INFO", "WARN", "ERROR"]
    services = ["AuthService", "PaymentGateway", "InventoryMgr", "EmailService"]
    
    with open(log_file, "w") as f:
        # Start with some startup logs
        f.write(generate_log_entry("INFO", "SYSTEM", "Application starting version 2.4.1-rc3"))
        f.write(generate_log_entry("INFO", "SYSTEM", "Connected to database at cluster-db-primary.internal"))
        
        for _ in range(50):
            req_id = str(uuid.uuid4())[:8]
            service = random.choice(services)
            
            # Successful flow
            f.write(generate_log_entry("INFO", req_id, f"[{service}] Processing request for /api/v1/resource"))
            
            if random.random() > 0.8:
                # Occasional warning
                f.write(generate_log_entry("WARN", req_id, f"[{service}] Response latency higher than P95 (450ms)"))
            
            if random.random() > 0.9:
                # Occasional error
                f.write(generate_log_entry("ERROR", req_id, f"[{service}] Failed to process transaction"))
                if service == "PaymentGateway":
                    f.write("Traceback (most recent call last):\n")
                    f.write("  File \"payment/gateway.py\", line 142, in process_charge\n")
                    f.write("    response = requests.post(GATEWAY_URL, json=payload, timeout=5)\n")
                    f.write("  File \"requests/api.py\", line 115, in post\n")
                    f.write("    return request('post', url, data=data, json=json, **kwargs)\n")
                    f.write("requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='api.stripe.com', port=443): Max retries exceeded with url: /v1/charges\n")
                elif service == "AuthService":
                    f.write(generate_log_entry("ERROR", req_id, "[AuthService] Invalid token signature detected from IP 192.168.1.45"))
            else:
                f.write(generate_log_entry("INFO", req_id, f"[{service}] Request completed successfully (200 OK)"))

    print(f"Successfully generated {log_file}")

if __name__ == "__main__":
    main()
