#!/usr/bin/env python
import optparse
import os
import urllib2
import json

def main():
    p = optparse.OptionParser()
    p.add_option('-l', '--list', action="store_false", help="return list of plugins installed")
    p.add_option('-s','--search',action='store_true', help='will search in plugins for string', dest='query')
    options, arguments = p.parse_args()
    if options.list is not None:
        list_installed()
        pass
    if options.query is not None:
        if len(arguments)>0:
            api_request(arguments[0])
        else:
            api_request('')
        pass

def list_installed():
    vim_bundle_path = os.environ['HOME']+'/.vim/bundle/'
    plugins = [name for name in os.listdir(vim_bundle_path)
            if os.path.join(vim_bundle_path, name)]
    index=0
    for plugin in plugins:
        print str(index)+"\t\033[38;5;172m"+plugin+"\033[0m"
        os.system('cd '+os.path.join(vim_bundle_path,plugin)+';git config --local remote.origin.url')
        print "\n"
        index+=1
    action = raw_input("Possible actions\n(r)emove\t(o)pen\t(c)ancel\n")
    if action in ['r','remove']:
        toRm = raw_input("Index to remove: \n")
        toRm = plugins[int(toRm)]
        confirm = raw_input("Sure?\t y\N \n")
        if confirm in ['y','Yes','Y','yes']:
            os.system(os.path.dirname(os.path.realpath(__file__))+'/./uninstall.sh '+toRm)
            pass
        pass
    if action in ['o','open']:
        toOp = raw_input('Index?\n')
        os.system('open $(cd "'+os.path.join(vim_bundle_path,plugins[int(toOp)])+'"; git config --local remote.origin.url)')

def api_request(query):
    url = 'http://vimawesome.com/api/plugins'
    if query:
        url += '?query='+query
        pass
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    index=0
    for plugin in response['plugins'][:8]:
        print str(index)+'\t\033[38;5;172m'+plugin['normalized_name'].title()+'\033\n\033[38;5;226m'+str(plugin['github_stars'])+'\033[0m\t\033[38;5;36m'+str(plugin['plugin_manager_users'])+'\033[0m\n\033[38;5;248m'+plugin['github_url']+'\033[0m\n'+plugin['vimorg_short_desc']+'\n'
        index+=1
        pass
    action = raw_input('Possible actions\n(i)nstall\t(o)pen\t(c)ancel\n')
    if action in ['i','install']:
        toIn = raw_input('Index to install:\n')
        os.system(os.path.dirname(os.path.realpath(__file__))+'/./install.sh '+response['plugins'][int(toIn)]['github_url'])
        pass
    if action in ['o','open']:
        toOp = raw_input('Index?\n')
        os.system('open '+response['plugins'][int(toOp)]['github_url'])

if __name__ == '__main__':
      main()
