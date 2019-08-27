from urllib.request import urlopen
import json
import subprocess, shlex
import time
import os


def download1(gitlabAddr, gitlabToken):
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
                # http下载
                thisProjectURL = thisProject['http_url_to_repo']
                thisProjectPath = thisProject['path_with_namespace']
                print(thisProjectURL + ' ' + thisProjectPath)
                if os.path.exists(thisProjectPath):
                    command = shlex.split('git clone' % (thisProjectPath))
                else:
                    command = 'git clone %s %s' % (thisProjectURL, thisProjectPath)

                # ssh 下载
                # thisProjectURL = thisProject['ssh_url_to_repo']
                # if os.path.exists(thisProjectPath):
                #     command = shlex.split('git -C "%s" pull' % (thisProjectPath))
                # else:
                #     command = shlex.split('git clone %s %s' % (thisProjectURL, thisProjectPath))

                # resultCode = os.subprocess.Popen(command)
                resultCode = os.system(command)
                print(resultCode)
                time.sleep(1)
            except Exception as e:
                print("Error on %s: %s" % (thisProjectURL, e.strerror))


if __name__ == '__main__':
    gitlabAddr = 'https://git.sensin-tech.cn'
    gitlabToken = 'yNJQufxun5iCbzmjxmNW'
    download1(gitlabAddr, gitlabToken)
