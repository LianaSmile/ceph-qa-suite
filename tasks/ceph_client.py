"""
Set up client keyring
"""
import logging

from teuthology import misc as teuthology
from teuthology.orchestra import run
from ceph_manager import write_conf

log = logging.getLogger(__name__)

def create_keyring(ctx, cluster_name):
    """
    Create key ring on remote client
    """
    log.info('Create client keyring...')
    #clients = ctx.cluster.only(teuthology.is_type('client', cluster_name))
    #testdir = teuthology.get_testdir(ctx)
    for role in ctx.config.get('roles'):
        for remote in teuthology.get_clients(ctx,role):
            client_keyring = "/etc/ceph/xtao-client.{id}.keyring".format(id=remote[0])
            remote[1].run(
                args=[        
                    'ceph',
                    'auth',
                    'get-or-create',
                    'client.{id}'.format(id=remote[0]),
                    'mon',
                    'allow rwx',
                    'mds',
                    'allow *',
                    'osd',
                    'allow *',
                    '-o',
                    client_keyring,
                    '--cluster',
                    cluster_name,
               ]
            )
            write_conf(ctx,'client.{id}'.format(id=remote[0]),'keyring',write_value=client_keyring,write_add=True)

# Liyan add this function
def clear_keyring(ctx,cluster_name):
    """
    Clear key ring on remote client
    """
    log.info('Clear client keyring...')
    for role in ctx.config.get('roles'):
        for remote in teuthology.get_clients(ctx,role):
            client_keyring = "/etc/ceph/xtao-client.{id}.keyring".format(id=remote[0])
            remote[1].run(
                'ceph',
                'auth',
                'del',
                'client.{id}'.format(id=remote[0]),
                '--cluster',
                cluster_name,
            )
            write_conf(ctx,'client.{id}'.format(id=remote[0]),'keyring',write_add=False)
            remote[1].run(
                args=[
                    'rm',
                    '-rf',
                    client_keyring,
                ]
            )
