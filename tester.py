import os
import sys
import termios
import time
import googleapiclient.discovery

def run(args, timeout):
    print("running command %s" % args)
    start = time.time()
    # Use a pty so that commands which call isatty don't change behavior.
    pid, fd = os.forkpty()
    if pid == 0:
        os.execlp(args[0], *args)
    else:
        t = termios.tcgetattr(fd)
        t[1] = t[1] & ~termios.ONLCR
        termios.tcsetattr(fd, termios.TCSANOW, t)
    buffer = b""
    while True:
        # A pty master returns EIO when the slave is closed.
        try:
            new = os.read(fd, 1024)
        except OSError:
            new = b""
        if len(new) == 0:
            break
        sys.stdout.buffer.write(new)
        sys.stdout.flush()
        buffer = buffer + new
    os.close(fd)
    pid, status = os.waitpid(pid, 0)
    if status != 0:
        end = time.time()
        final_time = end - start
        print("It returned a %d exit status. It took %d seconds to end" % (status, final_time))
        sys.exit(1)
    end = time.time()
    final_time = end - start
    print("It took %d seconds to complete" % final_time)
    buffer = buffer.decode()
    return buffer

username = ""
project_name = ""
sourceimage = ""
service_account = ""

job_path = os.getcwd() + "/test.sh"

os.chdir("..")

os.chdir("CloudyCluster/Build")
current_build = run(["git", "describe", "--always"], 0).strip()
compute = googleapiclient.discovery.build("compute", "v1")
images = compute.images().list(project=project_name).execute()
image_id = None
for image in images["items"]:
    if ("%stest" % username) in image["name"] and current_build in image["name"]:
        image_id = image["name"]

if image_id:
    image = image_id
    print("Using image %s" % (image))
else:
    f = open("test.yaml", "w")
    f.write(f"""- start:
  - local: false
  - sshkeyname: builderdash
  - sshkeyuser: builderdash
# ssh-keygen -m pem -f builderdash.pem -C builderdash
  - sshkey: /home/{username}/builderdash.pem
  - pubkeypath: /home/{username}/builderdash.pem.pub
  - spot: no
  - cloudservice: gcp
  - instancetype: n1-standard-32
  - region: us-east1-b
  - ostype: centos
  - instancename: {username}test-hpc
  - sourceimage: {sourceimage}
  - buildtype: dev
  - subnet: ''
  - bucketname: {project_name}.appspot.com
  - projectname: {project_name}
  - projectid: {project_name}
  - customtags:
    - packages
    - save
    - delete

- build:
  - builderdash:
    - build.yaml
""")
    f.close()
    build = run(["python3", "builderdash.py", "-c", "test.yaml"], 900)
    build = build.split("\n")
    image = None
    for line in build:
        if line.startswith("the instance we're going to delete is"):
            image = line.split(":")[1][1:]
    if not image:
        print("There's an error!")
        sys.exit(1)

os.chdir("../..")

ready = False
while not ready:
    compute_client = googleapiclient.discovery.build("compute", "v1")
    request = compute_client.images().get(project=project_name, image=image)
    res = request.execute()
    if res["status"] != "READY":
        time.sleep(30)
    else:
        ready = True

f = open(job_path, "w")
f.write("""#!/bin/sh
#SBATCH -N 1
date
hostname
""")
f.close()

password = os.urandom(16).hex()
print("cluster username", username)
print("cluster password", password)

f = open("automaton/ConfigurationFiles/gcp_tester.conf", "w")
f.write(f"""[UserInfo]
userName: {username}
password: {password}
firstName: {username}
LastName:
pempath: /home/{username}/.ssh/id_rsa

[General]
environmentName: {username}
cloudType: gcp
email:
sender:
sendpw: 
smtp: 

[CloudyClusterGcp]
keyName: {username}
instanceType: g1-small
networkCidr: 0.0.0.0/0
region: us-east1
zone: us-east1-b
pubkeypath: /home/{username}/.ssh/id_rsa.pub
sshkeyuser: {username}
sourceimage: projects/{project_name}/global/images/{image}


projectId: {project_name}
serviceaccountemail: {service_account}

[CloudyClusterEnvironment]
templateName: tester_template
keyName: {username}
region: us-east1
az: us-east1-b

[Computation]
# workflow1: {{"name": "gcpLargeRun", "type": "videoAnalyticsPipeline", "options": {{"instanceType": "c2-standard-4", "numberOfInstances": "2", "submitInstantly": "True", "usePreemptibleInstances": "true", "maintainPreemptibleSize": "true", "trafficVisionDir": "/software/trafficvision/", "bucketListFile": "list-us-east1", "generatedJobScriptDir": "generated_job_scripts", "trafficVisionExecutable": "process_clip.py", "jobGenerationScript": "generateJobScriptsFromBucketListFile.py", "jobPrefixString": "tv_processing_", "clip_to_start_on": "0", "clip_to_end_on": "100", "useCCQ": "true", "schedulerType": "Slurm", "schedulerToUse": "slurm", "skipProvisioning": "true", "timeLimit": "28800", "createPlaceholderInstances": "True"}}}}

#workflow2: {{"name": "gcpLargeRun", "type": "videoAnalyticsPipeline", "options": {{"instanceType": "c2-standard-16", "numberOfInstances": "2", "submitInstantly": "True", "usePreemptibleInstances": "true", "maintainPreemptibleSize": "true", "trafficVisionDir": "/software/trafficvision/", "bucketListFile": "bucket.list", "generatedJobScriptDir": "generated_job_scripts", "trafficVisionExecutable": "process_clip.py", "jobGenerationScript": "generateJobScriptsFromBucketListFile.py", "jobPrefixString": "tv_processing_", "clip_to_start_on": "0", "clip_to_end_on": "1000000", "useCCQ": "true", "schedulerType": "Slurm", "schedulerToUse": "slurm", "skipProvisioning": "true", "timeLimit": "28800", "createPlaceholderInstances": "True"}}}}

jobScript1: {{"name": "testScript1", "options": {{"uploadProtocol": "sftp", "monitorJob": "true", "uploadScript": "true", "localPath": "{job_path}", "remotePath": "/mnt/orangefs/test.sh", "executeDirectory": "/mnt/orangefs"}}}}

jobScript2: {{"name": "testScript2", "options": {{"uploadProtocol": "sftp", "monitorJob": "false", "uploadScript": "true", "localPath": "{job_path}", "remotePath": "/mnt/orangefs/test.sh", "executeDirectory": "/mnt/orangefs"}}}}

jobScript3: {{"name": "testScript3", "options": {{"uploadProtocol": "sftp", "monitorJob": "true", "uploadScript": "true", "localPath": "{job_path}", "remotePath": "/mnt/orangefs/test.sh", "executeDirectory": "/mnt/orangefs"}}}}

jobScript4: {{"name": "testScript4", "options": {{"uploadProtocol": "sftp", "monitorJob": "false", "uploadScript": "true", "localPath": "{job_path}", "remotePath": "/mnt/orangefs/test.sh", "executeDirectory": "/mnt/orangefs"}}}}

[tester_template]
description: Creates a CloudyCluster Environment that contains a single g1-small CCQ enabled Slurm Scheduler, a g1-small Login instance, a 100GB OrangeFS Filesystem, and a g1-small NAT instance.
vpcCidr: 10.0.0.0/16
scheduler1: {{'type': 'Slurm', 'ccq': 'true', 'instanceType': 'g1-small', 'name': 'slurm', 'schedAllocationType': 'cons_res'}}
filesystem1: {{"numberOfInstances": 4, "instanceType": "g1-small", "name": "orangefs", "filesystemSizeGB": "20", "storageVolumeType": "SSD", "orangeFSIops": 0, "instanceIops": 0}}
login1: {{'name': 'login', 'instanceType': 'g1-small'}}
nat1: {{'instanceType': 'g1-small', 'accessFrom': '0.0.0.0/0'}}
""")
f.close()

os.chdir("automaton")

creating_templates = run(["python3", "CreateEnvironmentTemplates.py", "-et", "CloudyCluster", "-cf", "ConfigurationFiles/gcp_tester.conf", "-tn", "tester_template"], 30)
print("created template:", creating_templates)

running_automaton = run(["python3", "Create_Processing_Environment.py", "-et", "CloudyCluster", "-cf", "ConfigurationFiles/gcp_tester.conf", "-all"], None)
print("automaton run:", running_automaton)
