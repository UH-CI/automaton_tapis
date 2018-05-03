template = {'vc': '10.0.0.0/16', 'instanceAvailabilityZone': '<<INSTANCE_AVAILABILITY_ZONE>>', 'VolumeType': 'SSD', 'clusterError': 'none', 'workingGroups': [{'omfs': 4, 'enableEBSEncryption': 'true', 'ofit': 't2.small', 'fid': '84569551', 'VolumeType': 'SSD', 'ofs': 4, 'iops': 0, 'accessInstances': ['Login'], 'ebsNumber': 1, 'ebs': 25, 'fo': 1, 'fn': 'orangefs', 'op': 3334}], 'clusterNumber': 1, 'RecType': 'Cluster', 'schedulers': [{'schedType': 'Torque', 'scalingType': 'autoscaling', 'sit': 't2.small', 'VolumeType': 'SSD', 'schedName': 'myTorque', 'schedGroups': []}], 's3': [{'clusterName': '<<CLUSTER_NAME>>', 's3Name': 'ccautomatonbucket', 's3NameDisplay': 'ccautomatonbucket', 'type': 'common', 's3Encryption': 'false'}], 'efs': [{'filesystemId': 'pending', 'type': 'common', 'efsName': 'efsdata'}, {'filesystemId': 'pending', 'type': 'ssw', 'efsName': 'efsapps'}, {'filesystemId': 'pending', 'type': 'sharedHome', 'efsName': 'home'}], 'clusterSpunUp': 'false', 'clusterAction': {'status': 'none'}, 'rollback': {'status': 'none'}, 'sswName': 'efsapps', 'clusterName': '<<CLUSTER_NAME>>', 'completed': 'true', 'hasNAT': 'true', 'computeGroups': [], 'ccVersion': 'Current Version', 'efsName': 'efsdata', 'hash_key': '<<CLUSTER_UUID>>', 'webDavs': [{'accessName': 'Login', 'VolumeType': 'SSD', 'fn': ['orangefs'], 'wdit': 't2.small'}], 'nit': 't2.micro', 'ofa': '0.0.0.0/0', 'name': '<<CLUSTER_UUID>>', 'cid': '<<CLUSTER_UUID>>', 'k': '<<KEY_NAME>>', 'pagesViewed': {'welcome': 'true', 'advanced': 'true', 'finalReview': 'true'}, 'Region': '<<REGION>>', 'sharedHomeDirEnabled': 'true', 'naf': '0.0.0.0/0', 'roadTraveled': ['welcome', 'advanced', 'finalReview']}

description = "Creates a CloudyCluster Environment that contains a single t2.small CCQ enabled Slurm Scheduler, a t2.small Login instance, EFS backed shared home directories, EFS backed shared software mount, an EFS backed shared filesystem, a 100GB encrypted EBS based OrangeFS Filesystem running on 4 EC2 instances, an S3 bucket named ccautomatonbucket, and a t2.micro NAT instance."
