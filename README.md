# Local Resume Sharing Website

This is the first project for the Computer Networks course at Isfahan University of Technology, developed by [Hoora](https://github.com/Fotros1383) and [me](https://github.com/afsharz). The project is a resume sharing website that can also serve as a local file-sharing tool for large files over the network.

The main goal was educational: to get hands-on experience with the Application Layer of computer networks. We deliberately worked directly with the HTTP protocol to understand how this layer operates in practice.

## How to Use

### 1. Get the Code

Before cloning this repository, please **fork it** to your own GitHub account.  
This way, you'll have your own copy to experiment with and push changes safely.

Then, you can clone your fork locally:

```bash
git clone https://github.com/YourUsername/jobportal-WebApplication.git

cd <jobportal-WebApplication>
```

### 2. Set Up Your Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
# OR
venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 3. Install the Requirements

```bash
pip install -r requirements.txt
```

### 4. Get the Database Ready

```bash
python manage.py migrate
```

### 5. Start the Server

```bash
python manage.py runserver
```

Then open:

```
http://127.0.0.1:8000/
```



## Making It Work Over Your Local Network

If you want people on the same Wi-Fi or LAN to use it, run:

```bash
python manage.py runserver 0.0.0.0:8000
```

Then they can visit:

```
http://<your_local_ip>:8000/
```
