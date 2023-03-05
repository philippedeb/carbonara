import subprocess as sp
import platform
import wmi
import psutil

# conda install pywin32

def print_system_details() -> None:
    print("\n\t>>> System details")
    
    # Get platform information
    print(f"\tOperating System: {platform.system()} {platform.release()} {platform.version()}")
    print(f"\tProcessor: {platform.processor()}")

    # Print CPU information
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    print(f"\tCPU Count: {cpu_count}")
    print(f"\tCPU Frequency: {cpu_freq.current/1000:.2f} GHz")

    # Print memory information
    mem = psutil.virtual_memory()
    total_memory = round(mem.total / (1024 ** 3), 2)
    used_memory = round(mem.used / (1024 ** 3), 2)
    available_memory = round(mem.available / (1024 ** 3), 2)
    memory_percent = mem.percent
    print(f"\n\tRAM:\n\tTotal Memory: {total_memory} GB")
    print(f"\tUsed Memory: {used_memory} GB")
    print(f"\tAvailable Memory: {available_memory} GB")
    print(f"\tMemory Usage: {memory_percent}%")

    # Print storage information
    c_drive = psutil.disk_usage('C:')
    total_storage = round(c_drive.total / (1024 ** 3), 2)
    used_storage = round(c_drive.used / (1024 ** 3), 2)
    available_storage = round(c_drive.free / (1024 ** 3), 2)
    storage_percent = c_drive.percent
    print(f"\n\tSTORAGE:\n\tTotal Storage: {total_storage} GB")
    print(f"\tUsed Storage: {used_storage} GB")
    print(f"\tAvailable Storage: {available_storage} GB")
    print(f"\tStorage Usage: {storage_percent}%")

    # Get display information
    wmi_obj = wmi.WMI(namespace='wmi')
    brightness = None
    for monitor in wmi_obj.WmiMonitorBrightness():
        if monitor.Active:
            brightness = monitor.CurrentBrightness
    print(f"\n\tBrightness: {brightness}%")
    
    # Print GPU information
    wmi_obj = wmi.WMI(namespace="root\\cimv2")
    gpu_info = wmi_obj.query("SELECT * FROM Win32_VideoController")
    gpu_count = 0
    for gpu in gpu_info:
        gpu_count += 1
        gpu_name = gpu.Name
        gpu_driver_version = gpu.DriverVersion
        gpu_memory = gpu.AdapterRAM
        gpu_memory_gb = min(0, round(gpu_memory / (1024 ** 3), 2))
        
        print(f"\n\tGPU {gpu_count}: {gpu_name}")
        print(f"\tGPU Driver Version: {gpu_driver_version}")
        print(f"\tGPU Memory: {gpu_memory_gb} GB")
