from .resourcetype import ResourceType
from .utils import urlpathjoin


class JobQ(ResourceType):

    resource_type = 'jobq'

    PRIO_LOWEST = 0
    PRIO_LOW = 1
    PRIO_NORMAL = 2
    PRIO_HIGH = 3
    PRIO_HIGHEST = 4

    def push(self, spider, **jobparams):
        jobparams['spider'] = spider
        for o in self.apipost('push', jl=jobparams):
            return o

    def summary(self, _queuename=None, spiderid=None):
        path = urlpathjoin(spiderid, 'summary', _queuename)
        r = list(self.apiget(path))
        return (r and r[0] or None) if _queuename else r

    def start(self, job=None):
        if job is None:
            for o in self.apipost('startjob'):
                return o
        else:
            return self._set_state(job, 'running')

    def finish(self, job):
        return self._set_state(job, 'finished')

    def delete(self, job):
        return self._set_state(job, 'deleted')

    def _set_state(self, job, state):
        if isinstance(job, dict):
            key = job['key']
        elif hasattr(job, 'key'):
            key = job.key
        else:
            key = job
        r = self.apipost('update', jl={'key': key, 'state': state})
        return r.next()
