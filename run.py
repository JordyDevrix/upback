import logging
import subprocess as sp
import sys
import argparse
from logging import Logger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the application.")
    parser.add_argument('-p', '--port', type=int, help='Port to use (1-65535)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    return parser.parse_args()

def logger_setup(debug: bool) -> logging.Logger:
    logger = logging.getLogger('runner')

    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger

def get_system() -> str:
    sys_os = sys.platform

    if sys_os.startswith('linux'):
        return 'linux'
    elif sys_os == 'darwin':
        return 'macos'
    elif sys_os == 'win32':
        return 'windows'
    elif sys_os == 'cygwin':
        return 'windows'

    raise OSError('Unsupported operating system')

def shell_cmd(cmd: str, cwd: str = None) -> str:
    process = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, cwd=cwd)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"Command '{cmd}' failed with error: {stderr.decode().strip()}")

    return stdout.decode().strip()

def main() -> None:
    args: argparse.Namespace = parse_args()
    port: int = args.port
    debug: bool = args.debug

    if port is not None:
        if not (1 <= port <= 65535):
            raise ValueError("Port must be between 1 and 65535")
    else:
        port = 8080

    logger: Logger = logger_setup(debug=debug)
    logger.info(f"Running setup. Debug {debug}")

    sys_os = get_system()
    logger.info(f"Operating System: {sys_os}")

    logger.info("Building frontend")
    frontend_dir: str = 'src/frontend/upback-frontend'

    npm_install: str = shell_cmd('npm install', cwd=frontend_dir)
    logger.debug(f"\n{npm_install}")

    npm_build: str = shell_cmd('npm run build', cwd=frontend_dir)
    logger.debug(f"\n{npm_build}")

    logger.info(f"Frontend build complete")

    logger.info(f"Building backend")
    uv_sync: str = shell_cmd('uv sync')
    logger.debug(f"\n{uv_sync}")

    logger.info(f"Starting backend server on port {port}")

    try:
        shell_cmd(f"uv run upback --port {port}")
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        return
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        return


if __name__ == '__main__':
    main()