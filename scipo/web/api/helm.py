
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

    def _execute_command(self, cmd):
        cmd_full = f'helm --output json -n {self.ns_name} {cmd}'

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
        cmd_result = self._execute_command('list --all')

        data = ''
        error = ''

        if not cmd_result:
            error = 'Getting list of your running instances failed'
            return (data, error)

        data = cmd_result
        return (data, error)

    def install(self, command_builder: CommandBuilder):
        logger.debug(str(command_builder.command))
        cmd_result = self._execute_command(command_builder.build())

        data = ''
        error = ''

        if not cmd_result:
            error = 'Starting new Scipion instance failed'
            return (data, error)

        data = cmd_result
        return (data, error)

    def uninstall(self, instance_name):
        #cmd_result = self._execute_command(f'uninstall {instance_name}')
        logger.error("not implemented")
