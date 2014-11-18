import shlex, subprocess
from os.path import join
import os

def call_shell(cmd):
    try:
        cmdout = subprocess.call(cmd, shell=True, stdout=None, stderr=subprocess.STDOUT)
        return True
    except Exception, e:
        cmdout = str(e.output)
    return cmdout

def get_files(mypath, path=True):
    if path:
        return sorted([ join(mypath,f) for f in os.listdir(mypath) if os.path.isfile(join(mypath,f)) and 'xiaomi_a' in join(mypath, f) ])
    else:
        return sorted([ f for f in os.listdir(mypath) if os.path.isfile(join(mypath,f)) and not f.endswith('txt')])

def main():
    home = "/home/pogo/xiaorong/tieba_robot/hashcat-0.47"
    hash_files = get_files('/tmp/')
    for f in hash_files:
        print f
        cmd = "%s/hashcat-cli64.bin -m 2611 %s %s/cnpassword.txt -o %s" % (home, f, home, home+"/xiaomi_passwd/"+f.replace("/tmp/", ""))
        call_shell(cmd)

if __name__ == "__main__":
    main()
