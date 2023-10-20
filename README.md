## 🧰 **Pyrinter** 🖨️

> A simple yet effective way to set up a WiFi printer service on a Linux server. It uses Zeroconf for Bonjour service registration and Discord webhooks for real-time print job notifications.
---

### 🌟 Features

*   🖨️ CUPS-based printing
*   📡 Zeroconf for Bonjour service registration
*   📬 Discord webhook notifications
*   📝 Detailed logging

---

### 🛠️ Setup

<details><summary>The Long Way</summary>

1.  **SSH into your Linux server:**
    
    ```bash
    ssh username@server_ip_address
    ```
    
2.  **Install Required Packages:**
    
    ```bash
    sudo apt update
    sudo apt install libcups2-dev curl
    ```
    
3.  **Install Poetry:**
    
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    
4.  **Clone the Repository:**
    
    ```bash
    git clone https://github.com/zudsniper/pyrinter.git
    cd pyrinter
    ```

5. **Install Dependencies:**
    
    ```bash
    poetry install
    ```

6. **Build the Project:**
    
    ```bash
    poetry build
    ```

7. **Run the Project:**
    
    ```bash
    poetry run pyrinter
    ```
    
    > **Note:** You can also run the project in the background using `nohup`:
    > ```bash
    > nohup poetry run pyrinter &
    > ```

---


</details>

#### ✨ Recommended Way  
Use `build.sh` to install packages / dependencies then build the project. 
```bash
$ ./build.sh
```

