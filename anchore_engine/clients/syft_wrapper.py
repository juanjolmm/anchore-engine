import os
import json
import shlex

from anchore_engine.utils import run_command, run_command_list, manifest_to_digest, AnchoreException
from anchore_engine.subsys import logger

def catalog_image(image):
    proc_env = os.environ.copy()
    cmd = "syft -vv -o json {image}".format(image=image)

    logger.debug("running syft: cmd={}".format(repr(cmd)))
    rc, stdout, stderr = run_command_list(shlex.split(cmd), env=proc_env)
    logger.debug("results: rc={} stdout={} stderr={}".format(rc, repr(stdout), repr(stderr)))

    if rc != 0:
        raise SyftError(cmd=cmd, rc=rc, out=stdout, err=stderr)

    return json.loads(stdout)


class SyftError(AnchoreException):

    def __init__(self, cmd=None, rc=None, out=None, err=None, msg='Error encountered in syft operation'):
        from anchore_engine.common.errors import AnchoreError

        self.cmd = ' '.join(cmd) if isinstance(cmd, list) else cmd
        self.exitcode = rc
        self.stderr = str(err).replace('\r', ' ').replace('\n', ' ').strip() if err else None
        self.stdout = str(out).replace('\r', ' ').replace('\n', ' ').strip() if out else None
        self.msg = msg

    def __repr__(self):
        return '{}. cmd={}, rc={}, stdout={}, stderr={}'.format(self.msg, self.cmd, self.exitcode, self.stdout, self.stderr)

    def __str__(self):
        return '{}. cmd={}, rc={}, stdout={}, stderr={}'.format(self.msg, self.cmd, self.exitcode, self.stdout, self.stderr)