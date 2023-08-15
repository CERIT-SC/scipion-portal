
import logging
import subprocess


logger = logging.getLogger('django')

class Helmctl:
    @staticmethod
    def _execute_command(cmd):
        base = 'helm --output json'
        cmd_full = f'{base} {cmd}'

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

        return result

    @staticmethod
    def list():
        result = Helmctl._execute_command('list')
        return str(result)

    @staticmethod
    def install():
        logger.error("not implemented")

    @staticmethod
    def uninstall():
        logger.error("not implemented")
