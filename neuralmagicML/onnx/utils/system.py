"""
Utilities for ONNX based ML system info and validation
"""

from typing import List, Any, Dict
import socket
import psutil

try:
    import neuralmagic

    nm_import_err = None
except Exception as nm_err:
    neuralmagic = None
    nm_import_err = nm_err

try:
    import onnxruntime

    ort_import_err = None
except Exception as ort_err:
    onnxruntime = None
    ort_import_err = ort_err


__all__ = [
    "available_ml_engines",
    "ml_engines_errors",
    "get_ml_sys_info",
]


def available_ml_engines() -> List[str]:
    """
    :return: List of available inference providers on current system. Potential values
        include ['neural_magic', 'ort_cpu', 'ort_gpu']
    """
    # ORT availability
    engines = []

    if neuralmagic is not None:
        engines.append("neural_magic")

    ort_providers = onnxruntime.get_available_providers()
    if "CPUExecutionProvider" in ort_providers:
        engines.append("ort_cpu")
    if "CUDAExecutionProvider" in ort_providers:
        engines.append("ort_gpu")

    return engines


def ml_engines_errors() -> Dict[str, Exception]:
    """
    :return: a dictionary containing any errors encountered when importing ML engines
        on the current system
    """
    return {
        "neuralmagic": nm_import_err,
        "onnxruntime": ort_import_err,
    }


def get_ml_sys_info() -> Dict[str, Any]:
    """
    :return: a dictionary containing info for the system and ML engines on the system.
        Such as number of cores, instruction sets, available engines, etc
    """
    sys_info = {
        "available_engines": available_ml_engines(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
    }

    # get sys info from neuralmagic.cpu
    if neuralmagic is not None:
        nm_info = neuralmagic.cpu.cpu_architecture()
        nm_info = {k.lower(): v for k, v in nm_info.items()}  # standardize case
        sys_info.update(nm_info)  # add to main dict

        available_instructions = neuralmagic.cpu.VALID_VECTOR_EXTENSIONS
        available_instructions = [ins.upper() for ins in available_instructions]
        sys_info["available_instructions"] = available_instructions
    else:
        sys_info["cores_per_socket"] = psutil.cpu_count(logical=False)

    return sys_info
