"""Doc."""
import toml
import subprocess
import os
from os.path import expanduser
from pylxd import Client
from pylxd.exceptions import LXDAPIException

OPERATION_CREATED = 100
STARTED = 101
STOPPED = 102
RUNNING = 103
CANCELLING = 104
PENDING = 105
STARTING = 106
STOPPING = 106
ABORTING = 108
FREEZING = 109
FROZEN = 110
THAWED = 111
SUCCESS = 200
FAILURE = 400
CANCELLED = 401

STATUSES = {
    OPERATION_CREATED: 'Operation created',
    STARTED: 'Started',
    STOPPED: 'Stopped',
    RUNNING: 'Running',
    CANCELLING: 'Cancelling',
    PENDING: 'Pending',
    STARTING: 'Starting',
    STOPPING: 'Stopping',
    ABORTING: 'Aborting',
    FREEZING: 'Freezing',
    FROZEN: 'Frozen',
    THAWED: 'Thawed',
    SUCCESS: 'Success',
    FAILURE: 'Failure',
    CANCELLED: 'Cancelled'
}


DEBIAN_JESSIE_AMD64 = '40d81d3f5808'
CENTOS6_AMD64 = 'fb4f93e86126'
FEDORA22_AMD64 = 'aca23c3193bb'
UBUNTU_TRUSTY_AMD64 = '93a72d8e0f92'


FINGERPRINTS_NAMES = {
    DEBIAN_JESSIE_AMD64: 'Debian jessie (amd64)',
    CENTOS6_AMD64: 'Centos 6 (amd64)',
    FEDORA22_AMD64: 'Fedora 22 (amd64)',
    UBUNTU_TRUSTY_AMD64: 'Ubuntu trusty (amd64)'
}

BASE_IMAGES_FINGERPRINTS = {
    "Debian": DEBIAN_JESSIE_AMD64,
    "Centos": CENTOS6_AMD64,
    "Fedora": FEDORA22_AMD64,
    "Ubuntu": UBUNTU_TRUSTY_AMD64
}


class LaimEnvAlreadyExists(Exception):
    """LaimEnv already exists."""

    pass


class LaimEnvDoesNotExist(Exception):
    """Doc."""

    pass


class LaimEnvNotStopped(Exception):
    """Doc."""

    pass


# Example ~/.laim
# ---------------

# [base]
# endpoint=""
# cert_path=""
# cert_key=""


class LaimLaim(object):
    """Doc."""

    def __init__(self, conf_file=None):
        """Doc."""
        self.conf = self.__load_conf(conf_file)
        endpoint = self.conf.get('base', {}).get('endpoint', None)
        if endpoint:
            self.lxd = Client(
                endpoint=endpoint,
                cert=(self.conf.get('base', {}).get('cert_path', None),
                      self.conf.get('base', {}).get('cert_key', None)))
        else:
            self.lxd = Client()

    def __load_conf(self, conf_file):
        """doc."""
        if conf_file is None:
            conf_file = os.path.join(expanduser('~'), '.laim')
            conf = toml.loads(open(conf_file, 'r').read())
            return conf
        return {}

    def envs(self):
        """List all available work environments."""
        # containers = self.lxd.containers_list()
        conts = [cobj.name
                 for cobj in self.lxd.containers.all()
                 if cobj.status_code == RUNNING]
        # import pdb; pdb.set_trace()
        return conts

    def startenv(self, name, wait=True):
        """Start a new Laim work env."""
        try:
            container = self.lxd.containers.get(name)
            raise LaimEnvAlreadyExists()
        except LXDAPIException:
            fingerprint = BASE_IMAGES_FINGERPRINTS.get(
                self.conf.get('env', {}).get('base_image')
            ) or UBUNTU_TRUSTY_AMD64

            print FINGERPRINTS_NAMES.get(fingerprint)

            conf = {'name': name,
                    'source': {
                        'mode': 'pull',
                        'type': 'image',
                        'fingerprint':
                            fingerprint,
                        'server': 'http://images.linuxcontainers.org',
                        'ephemral': False
                    }}
            container = self.lxd.containers.create(conf, wait=wait)

            if self.conf.get('env', {}).get('auto_start'):
                container.start()

        return (container.status_code, container)

    def delete(self, name, wait=True):
        """Delete a work environment."""
        try:
            container = self.lxd.containers.get(name)
            if container.status_code == STOPPED:
                return container.delete(wait=wait)
            else:
                raise LaimEnvNotStopped
        except LXDAPIException:
            raise LaimEnvDoesNotExist()

    def stop(self, name, wait=True):
        """Stop a work environment."""
        container = self.lxd.containers.get(name)
        return container.stop(wait=wait)

    def bash(self, name):
        """Activate a work env."""
        try:
            cont = self.lxd.containers.get(name)
            cmds = [
                'lxc',
                'exec',
                cont.name,
                '--',
                self.conf.get('env', {}).get('activate_script') or 'bash'
            ]
            print "Calling: ", ' '.join(cmds)
            subprocess.call(cmds, shell=False)
        except LXDAPIException:
            raise LaimEnvDoesNotExist()
