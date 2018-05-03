template = {'vc': '10.0.0.0/16', 'instanceAvailabilityZone': '<<INSTANCE_AVAILABILITY_ZONE>>', 'VolumeType': 'SSD', 'clusterError': 'none', 'workingGroups': [], 'clusterNumber': 1, 'RecType': 'Cluster', 'schedulers': [{'schedType': 'Slurm', 'scalingType': 'autoscaling', 'sit': 't2.small', 'VolumeType': 'SSD', 'schedName': 'mySlurm', 'schedGroups': []}], 's3': [], 'efs': [], 'clusterSpunUp': 'false', 'clusterAction': {'status': 'none'}, 'rollback': {'status': 'none'}, 'clusterName': '<<CLUSTER_NAME>>', 'completed': 'true', 'hasNAT': 'true', 'computeGroups': [], 'ccVersion': 'Current Version', 'hash_key': '<<CLUSTER_UUID>>', 'webDavs': [{'accessName': 'Login', 'VolumeType': 'SSD', 'fn': [], 'wdit': 't2.small'}], 'nit': 't2.micro', 'ofa': '0.0.0.0/0', 'name': '<<CLUSTER_UUID>>', 'cid': '<<CLUSTER_UUID>>', 'k': '<<KEY_NAME>>', 'pagesViewed': {'welcome': 'true', 'advanced': 'true', 'finalReview': 'true'}, 'Region': '<<REGION>>', 'sharedHomeDirEnabled': 'false', 'naf': '0.0.0.0/0', 'roadTraveled': ['welcome', 'advanced', 'finalReview']}

description = "Creates a CloudyCluster Environment that contains a single t2.small CCQ enabled Slurm Scheduler, a t2.small Login instance, and a t2.micro NAT instance. This template contains no shared filesystems as the original workflow was designed to run without one."