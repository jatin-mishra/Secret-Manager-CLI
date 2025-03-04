# Secret Manager CLI

### **Introducing Secret Manager CLI – A Secure, Local, and Lightweight Password Management Solution**  

In today's digital landscape, password security is a major concern. Many users either rely on third-party password managers, which raise trust issues, store passwords in plaintext files, making them vulnerable, or use simple passwords just to remember them—each posing significant security risks. Secret Manager CLI is here to change that.

## 🚀 What is Secret Manager CLI?  
Secret Manager CLI is a lightweight, **AI-generated** command-line tool that allows you to securely store and manage sensitive information **locally**, using encryption. No cloud, no third-party services—**just you and your encrypted secrets**.  

## 🔒 Why Should You Use It?  
- **No Third-Party Trust Issues** – Your secrets stay on your machine, fully encrypted.  
- **Instant Access** – Retrieve passwords directly into the clipboard without ever displaying them on the screen.  
- **Bulk Operations** – Easily add and verify multiple secrets at once.  
- **Advanced Encryption** – Even if someone gains access to your machine, they cannot read your secrets without your encryption key.  
- **Simple & Fast** – No complicated UI, just a powerful CLI tool that gets the job done.  

## 🔍 How It Stands Out  
Unlike browser password managers or third-party tools like LastPass and Bitwarden, **Secret Manager gives you full control** over your data while maintaining convenience. It's as easy as running:  
```sh
secret_manager
```
and handling your secrets securely.  

## 💡 Ideal For:  
- Developers & engineers who need to manage API keys and sensitive credentials.  
- Security-conscious users who don’t trust third-party password managers.  
- Anyone who wants an **offline, encrypted, and simple** way to store passwords.  

🛠 **Try it now and take control of your digital security.**  

---

## Installation
Follow these steps to set up Secret Manager on macOS, Linux, and Windows.

### 1. Set Up a Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```sh
pip install pyperclip cryptography
```

### 3. Configure Environment Variables
Define the location for storing encrypted secrets:

For **zsh users**:
```sh
nano ~/.zshrc
```
For **bash users**:
```sh
nano ~/.bashrc
```
For **Linux users**:
```sh
nano ~/.bash_profile
```
For **Windows users** (PowerShell):
```powershell
[System.Environment]::SetEnvironmentVariable("SECRETS_FILE", "$env:USERPROFILE\secrets.enc", [System.EnvironmentVariableTarget]::User)
```
Add the following line:
```sh
export SECRETS_FILE=~/Desktop/secrets.enc  # macOS/Linux
setx SECRETS_FILE "%USERPROFILE%\secrets.enc"  # Windows (CMD)
```
Save and exit, then apply the changes:
```sh
source ~/.zshrc   # For zsh users
source ~/.bashrc  # For bash users
source ~/.bash_profile  # For Linux users
```

### 4. Download and Install Secret Manager CLI
#### macOS/Linux
```sh
wget https://your-download-link.com/secret_manager.py -O secret_manager.py  # Replace with actual link
sudo mv secret_manager.py /usr/local/bin/secret_manager
sudo chmod +x /usr/local/bin/secret_manager
```

#### Windows
```powershell
Invoke-WebRequest -Uri "https://your-download-link.com/secret_manager.py" -OutFile "$env:USERPROFILE\secret_manager.py"
```
Then, add the Python script directory to your system PATH:
```powershell
[System.Environment]::SetEnvironmentVariable("Path", "$env:Path;$env:USERPROFILE", [System.EnvironmentVariableTarget]::User)
```
Now, you can run it using:
```sh
python %USERPROFILE%\secret_manager.py  # CMD
python $env:USERPROFILE\secret_manager.py  # PowerShell
```
To make it a command, create a batch file:
1. Open Notepad and paste:
   ```sh
   @echo off
   python %USERPROFILE%\secret_manager.py %*
   ```
2. Save it as `secret_manager.bat` in `C:\Windows`.
3. Now, run it from any terminal:
   ```sh
   secret_manager
   ```

### 5. Run Secret Manager
```sh
secret_manager  # macOS/Linux
secret_manager.bat  # Windows
```

---

## Usage

### Secret Manager (`secret_manager`)
Perform secure operations with encrypted secrets:
- **Add key-value pairs** – Store secrets securely; it can also generate strong passwords on your behalf.
- **Retrieve values** – Copy secret values directly to the clipboard without displaying them.
- **Change encryption key** – Update the encryption key if needed.
- **Search keys** – Find stored secrets using prefix-based search.
- **Clear stored data** – Remove all saved secrets if necessary.
- **Batch insert key-value pairs** – Efficiently store multiple secrets at once.
- **Verify stored values** – Compare key-value pairs from a file against stored secrets and identify mismatches.

---

## Comparison with Other Solutions

| Solution                      | Local Storage | Encryption | Third-Party Dependence | Bulk Operations | Clipboard Retrieval |
|--------------------------------|--------------|------------|------------------------|----------------|--------------------|
| **Secret Manager**            | ✅           | ✅         | ❌                     | ✅              | ✅                 |
| Bitwarden / LastPass / 1Password | ❌        | ✅         | ✅                     | ❌              | ✅                 |
| KeePass / Pass                | ✅           | ✅         | ❌                     | ❌              | ❌                 |
| Encrypted Text Files (GPG, VeraCrypt) | ✅      | ✅         | ❌                     | ❌              | ❌                 |
| Browser Password Managers     | ❌           | ✅         | ✅                     | ❌              | ✅                 |

---

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to enhance this tool.

