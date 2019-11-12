import logging

import requests

from borgmatic.hooks import monitor

logger = logging.getLogger(__name__)

MONITOR_STATE_TO_CRONITOR = {
    monitor.State.START: 'run',
    monitor.State.FINISH: 'complete',
    monitor.State.FAIL: 'fail',
}


def ping_monitor(ping_url, config_filename, state, dry_run):
    '''
    Ping the given Cronitor URL, modified with the monitor.State. Use the given configuration
    filename in any log entries. If this is a dry run, then don't actually ping anything.
    '''
    dry_run_label = ' (dry run; not actually pinging)' if dry_run else ''
    ping_url = '{}/{}'.format(ping_url, MONITOR_STATE_TO_CRONITOR[state])

    logger.info(
        '{}: Pinging Cronitor {}{}'.format(config_filename, state.name.lower(), dry_run_label)
    )
    logger.debug('{}: Using Cronitor ping URL {}'.format(config_filename, ping_url))

    if not dry_run:
        logging.getLogger('urllib3').setLevel(logging.ERROR)
        requests.get(ping_url)
