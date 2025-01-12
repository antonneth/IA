import subprocess

def run_scripts():
    scripts = ["NSDcache.py", "script2.py"]
    for script in scripts:
        print(f"Ejecutando {script}...")
        result = subprocess.run(["python", script], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error executant {script}: {result.stderr}")
            break

if __name__ == "__main__":
    run_scripts()