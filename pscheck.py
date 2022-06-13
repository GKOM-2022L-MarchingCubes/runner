import locale
import subprocess

# based on: https://stackoverflow.com/a/29275361
def process_exists(process_name):
    command = ['tasklist', '/fi', f'imagename eq {process_name}']
    try:
        output = subprocess.check_output(command).decode(locale.getpreferredencoding())
    except subprocess.CalledProcessError:
        return False
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())
