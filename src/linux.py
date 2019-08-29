from urllib.request import urlopen
import json
import subprocess, shlex
import time
import os


def download(gitlabAddr, gitlabToken, ssh_or_http):
    for index in range(10):
        url = "%s/api/v4/projects?private_token=%s&per_page=100&page=%d&order_by=name" % (
            gitlabAddr, gitlabToken, index)
        print(url)
        allProjects = urlopen(url)
        allProjectsDict = json.loads(allProjects.read().decode())
        if len(allProjectsDict) == 0:
            break
        for thisProject in allProjectsDict:
            try:
                if ssh_or_http == "http":
                    # http下载
                    thisProjectURL = thisProject['http_url_to_repo']
                    thisProjectPath = thisProject['path_with_namespace']
                    print(thisProjectURL + ' ' + thisProjectPath)
                    if os.path.exists(thisProjectPath):
                        command = shlex.split('git clone' % (thisProjectURL))
                    else:
                        command = shlex.split('git clone %s %s' % (thisProjectURL, thisProjectPath))
                    os.subprocess.Popen(command)
                else:
                    # ssh 下载
                    thisProjectURL = thisProject['ssh_url_to_repo']
                    thisProjectPath = thisProject['path_with_namespace']
                    print(thisProjectURL + ' ' + thisProjectPath)
                    if os.path.exists(thisProjectPath):
                        command = shlex.split('git -C "%s" pull' % (thisProjectPath))
                    else:
                        command = shlex.split('git clone %s %s' % (thisProjectURL, thisProjectPath))

                    os.subprocess.Popen(command)
                time.sleep(1)
            except Exception as e:
                print("Error on %s: %s" % (thisProjectURL, e.strerror))


if __name__ == '__main__':
    gitlabAddr = 'https://git.sensin-tech.cn'
    gitlabToken = 'yNJQufxun5iCbzmjxmNW'
    ssh_or_http = "http"
    download(gitlabAddr, gitlabToken, ssh_or_http)
