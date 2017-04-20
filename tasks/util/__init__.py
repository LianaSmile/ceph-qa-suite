from teuthology import misc

def get_remote(ctx, cluster, service_type, service_id):
    """
    Get the Remote for the host where a particular role runs.

    :param cluster: name of the cluster the service is part of
    :param service_type: e.g. 'mds', 'osd', 'client'
    :param service_id: The third part of a role, e.g. '0' for
                       the role 'ceph.client.0'
    :return: a Remote instance for the host where the
             requested role is placed
    """
    # Liyan debug
    #def _is_instance(role):
    #    role_tuple = misc.split_role(role)
    #    return role_tuple == (cluster, service_type, str(service_id))
    try:
        # Liyan debug
        #(remote,) = ctx.cluster.only(_is_instance).remotes.keys()
        role = get_role(cluster,service_type,service_id)
        for key,value in ctx.cluster.only(role).remotes.items():
            if role in value:
                remote = key
                return remote
                break
            else:
                log,info('Liyan no matched service_type {type} service_id {id} , Please check your roles config'.format(type=service_type,id=service_id))
    except ValueError:
        raise KeyError("Service {0}.{1}.{2} not found".format(cluster,
                                                              service_type,
                                                              service_id))
    #return remote

# Liyan add this function
def get_role(cluster,service_type,service_id):
    return '{ceph_cluster}.{ceph_service_type}.{ceph_service_id}'.format(ceph_cluster=cluster,ceph_service_type=service_type,ceph_service_id=service_id)

def get_remote_for_role(ctx, role):
    return get_remote(ctx, *misc.split_role(role))
