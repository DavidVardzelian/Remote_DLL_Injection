#include <windows.h>
#include <stdio.h>

void LogMessage(const char* message) {
    FILE* file = fopen("dll_log.txt", "a");
    if (file) {
        fprintf(file, "%s\n", message);
        fclose(file);
    }
}

BOOL WINAPI DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH:
            LogMessage("DLL loaded successfully");
            MessageBox(NULL, "malware CRb64", "DLL Injected", MB_OK);
            break;
        case DLL_PROCESS_DETACH:
            LogMessage("DLL unloaded");
            break;
    }
    return TRUE;
}
