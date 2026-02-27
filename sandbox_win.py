"""
MONOLITH SANDBOX (WINDOWS)
Safe execution environment for agents using Windows Job Objects (via ctypes).
Enforces memory limits and strict timeouts.
"""

import subprocess
import time
import sys
import os
import ctypes
from pathlib import Path

# Windows Job Object Constants
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100

class BOOTSTRAP_JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", ctypes.c_void_p), # Placeholder for simpler struct
        ("IoInfo", ctypes.c_void_p),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]

# Basic structure for simple limits
class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", ctypes.c_ulong),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", ctypes.c_ulong),
        ("Affinity", ctypes.c_void_p),
        ("PriorityClass", ctypes.c_ulong),
        ("SchedulingClass", ctypes.c_ulong),
    ]

class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", ctypes.c_ubyte * 48), # Padding
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]

class MonolithSandbox:
    def __init__(self):
        self.job = None
        if os.name == 'nt':
            self._create_job_object()
            
    def _create_job_object(self):
        """Create a Windows Job Object to contain the agent"""
        try:
            self.job = ctypes.windll.kernel32.CreateJobObjectW(None, None)
            
            # Set limits
            info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
            info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            
            # 512MB RAM limit per process (Strict Enforcement)
            info.BasicLimitInformation.LimitFlags |= JOB_OBJECT_LIMIT_PROCESS_MEMORY
            info.ProcessMemoryLimit = 512 * 1024 * 1024 
            
            permission = ctypes.windll.kernel32.SetInformationJobObject(
                self.job,
                9, # JobObjectExtendedLimitInformation
                ctypes.byref(info),
                ctypes.sizeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION)
            )
            
            if not permission:
                print("   [SANDBOX] ⚠️ Failed to set Job Object limits.")
                
        except Exception as e:
            print(f"   [SANDBOX] ⚠️ Sandbox Init Error: {e}")

    def run_agent(self, script_path, args=[], timeout=60, env_vars={}):
        """Run a Python agent in the sandbox"""
        
        # Prepare environment
        env = os.environ.copy()
        env.update(env_vars)
        if "PYTHONUTF8" not in env:
            env["PYTHONUTF8"] = "1"
            
        cmd = [sys.executable, str(script_path)] + args
        
        # Start Process
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(Path(script_path).parent.parent.parent), # Root of repo usually
            env=env,
            creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB if os.name == 'nt' else 0,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # Assign to Job Object
        if self.job and os.name == 'nt':
            try:
                ctypes.windll.kernel32.AssignProcessToJobObject(self.job, ctypes.c_void_p(proc._handle))
            except:
                pass # Fail silently if not supported
                
        # Wait for completion
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            return {
                "success": proc.returncode == 0,
                "exit_code": proc.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "timeout": False
            }
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            return {
                "success": False,
                "exit_code": -1,
                "stdout": stdout,
                "stderr": stderr,
                "timeout": True
            }
