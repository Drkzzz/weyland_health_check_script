import psutil
import platform
import subprocess
import subprocess


def get_os_info():
    os_name = platform.system()
    return os_name


os_info = get_os_info()


def health_check():
    # Información de CPU
    cpu_usage = psutil.cpu_percent(interval=1)

    # Información de Memoria RAM
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    ram_total_gb = ram.total / 1e9
    ram_available_gb = ram.available / 1e9
    ram_used_gb = ram.used / 1e9

    # Crear un diccionario con la información
    health_info = {
        "cpu": {
            "usage_percentage": cpu_usage,
        },
        "ram": {
            "usage_percentage": ram_usage,
            "total_gb": ram_total_gb,
            "available_gb": ram_available_gb,
            "used_gb": ram_used_gb,
        },
    }

    # Información de Disco
    # Ejecutar disk.py para tomar la información de las particiones correspondientes
    if os_info == "Windows":
        disk = psutil.disk_usage('C:\\')
        disk = {"disk": {"usage_percentage": disk.percent,
                         "total_gb": disk.total / 1e9,
                         "used_gb": disk.used / 1e9,
                         "free_gb": disk.free / 1e9}}
        health_info.update(disk)
    elif os_info == "Darwin":
        disk = psutil.disk_usage('/System/Volumes/Data')
        disk = {"disk": {"usage_percentage": disk.percent,
                         "total_gb": disk.total / 1e9,
                         "used_gb": disk.used / 1e9,
                         "free_gb": disk.free / 1e9}}
        health_info.update(disk)
        health_info.update(disk)
    return health_info


def print_health_info(info):
    print("=== Información del Sistema ===")
    for component, metrics in info.items():
        print(f"\n{component}:")
        for metric, value in metrics.items():
            # Imprimir el valor con dos decimales, excepto para el porcentaje
            if 'percentage' in metric:
                print(f"  {metric}: {value:.2f}%")
            else:
                print(f"  {metric}: {value:.2f} GB")


if __name__ == "__main__":
    health_info_result = health_check()
    print_health_info(health_info_result)
