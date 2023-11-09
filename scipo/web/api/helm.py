
import os
import logging
import subprocess


logger = logging.getLogger('django')

helm_chart_path = '/opt/scipion-docker-chart'

class Helmctl:
    class CommandBuilder:
        def __init__(self, instance_name):
            self.command = list()
            self.command.append(f'install {instance_name}')

        def add_variable(self, name, value):
            self.command.append(f'--set {name}={value}')
            return self

        def build(self):
            final_cmd = list(self.command)
            final_cmd.append(helm_chart_path)
            logger.debug(str(f'final cmd {final_cmd}'))
            return ' '.join(final_cmd)


    def __init__(self) -> None:
        self.ns_name = f"{os.environ['KUBERNETES_NS_NAME']}"

    def _execute_command(self, cmd, json_output = False):
        cmd_output_part = "--output json" if json_output else ""
        cmd_full = f'helm {cmd_output_part} -n {self.ns_name} {cmd}'

        # convert str to List[str]
        cmd_list = list()
        cmd_tmp = cmd_full.split(' ')
        for word in cmd_tmp:
            if word:
                cmd_list.append(word)

        try:
            result = subprocess.run(cmd_full, shell=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as ex:
            logger.error(ex)
            return None
        except Exception as ex:
            logger.error(ex)
            return None

        if result.returncode != 0:
            logger.error(f'Command returned non-zero code. Code: {result.returncode}, stderr: \"{result.stderr}\".')
            return None

        return result.stdout.strip()

    def list(self):
        result = self._execute_command('list --all', json_output=True)
        if not result:
            logger.error("Getting list of your running instances failed.")
            return None

        return result

    def install(self, command_builder: CommandBuilder):
        result = self._execute_command(command_builder.build(), json_output=True)
        if not result:
            logger.error("Starting new Scipion instance failed.")
            return False

        return True

    def uninstall(self, instance_name):
        result = self._execute_command(f'uninstall {instance_name}')
        if not result:
            logger.error("Deletion of the Scipion instance failed.")
            return False

        return True
