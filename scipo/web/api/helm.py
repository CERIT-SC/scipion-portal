
import os
import logging
import subprocess


logger = logging.getLogger('django')

class Helmctl:
    def __init__(self) -> None:
        self.ns_name = f"{os.environ['KUBERNETES_NS_NAME']}"

    def _execute_command(self, cmd):
        cmd_full = f'helm --output json -n {self.ns_name} {cmd}'

        # convert str to List[str]
        cmd_list = list()
        cmd_tmp = cmd_full.split(' ')
        for word in cmd_tmp:
            if word:
                cmd_list.append(word)

        try:
            result = subprocess.run(cmd_full, shell=True, capture_output=True)
        except subprocess.CalledProcessError as ex:
            logger.error(ex)
            return None
        except Exception as ex:
            logger.error(ex)
            return None

        if result.returncode != 0:
            logger.error(f'Command returned non-zero code. Code: {result.returncode}, stderr: \"{result.stderr}\".')
            return None

        return str(result.stdout)

    def list(self):
        cmd_result = self._execute_command('list')

        data = ''
        error = ''

        if not cmd_result:
            error = 'Getting list of your running instances failed'
            return (data, error)

        data = cmd_result
        return (data, error)

    def install(self):
        logger.error("not implemented")

    def uninstall(self):
        logger.error("not implemented")
