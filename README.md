
# **DLL Injection: Code in the Shadows 💉**  

### 🕶️ **Some codes are meant to be written in silence...**  

This project demonstrates **DLL injection**—a technique that allows external code to be executed inside a running process. By manipulating memory and creating remote threads, we can make a process load a custom DLL, altering its behavior from the inside.  

### 🔥 **How It Works**  
- **Finds the target process** by name  
- **Allocates memory** inside the process  
- **Writes the DLL path** to the allocated memory  
- **Remotely executes LoadLibraryA** to load the DLL into the process  

### 🚀 **Usage**  
```sh
python Remote_DLL_injection.py <process_name> <dll_path>
```
Example:  
```sh
python Remote_DLL_injection.py notepad.exe mydll.dll
```

### ⚠️ **Disclaimer**  
This project is for **educational and research purposes only.** Unauthorized use on systems you do not own **may violate laws and policies.** Always act responsibly.  

---
