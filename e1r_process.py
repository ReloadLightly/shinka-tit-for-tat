"""Linux subprocess bounds with parent-death cleanup for nested Headless/Codex."""
import ctypes
import os
import signal
import subprocess


def bounded_run(command, *, timeout, env, stdin=None):
    # Wrappers are single-threaded. The death signal prevents a child in its
    # own process group from outliving a killed outer Headless/guard process.
    libc = ctypes.CDLL(None, use_errno=True)
    parent_pid = os.getpid()

    def child_setup():
        if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
            os._exit(125)
        if os.getppid() != parent_pid:
            os._exit(125)

    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, env=env,
                            start_new_session=True, preexec_fn=child_setup)
    try:
        stdout, stderr = proc.communicate(stdin, timeout=timeout)
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate(timeout=5)
        return 124, stdout, stderr + "\nE1-R subprocess timeout; process group killed.\n"
