#!/usr/bin/env python3
import argparse
import collections
import configparser
import hashlib
import os
import re
import sys
import zlib

argparser = argparse.ArgumentParser(
    description='simple git')


argsubparsers = argparser.add_subparsers(
                    title='commands', 
                    dest='command')

argsubparsers.required = True



def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if   args.command == 'add'          : cmd_add(args)
    elif args.command == 'cat-file'     : cmd_cat_file(args)
    elif args.command == 'checkout'     : cmd_checkout(args)
    elif args.command == 'commit'       : cmd_commit(args)
    elif args.command == 'hash-object'  : cmd_hash_object(args)
    elif args.command == 'init'         : cmd_init(argv)
    elif args.command == 'log'          : cmd_log(argv)
    elif args.command == 'ls-tree'      : cmd_ls_tree(argv)
    elif args.command == 'merge'        : cmd_merge(argv)
    elif args.command == 'rebase'       : cmd_rebase(args)
    elif args.command == 'rev-parse'    : cmd_rev_parse(args)
    elif args.command == 'rm'           : cmd_rm(args)
    elif args.command == 'show-ref'     : cmd_show_ref(args)
    elif args.command == 'tag'          : cmd_tag(args)

argsp = argsubparsers.add_parser('init', 
                    help='Initialize a new, empty repository.')

argsp.add_argument( 'path',
                    metavar='directory',
                    nargs='?',
                    default='.',
                    help='path to create the git repository.')

def cmd_init(args):
    '''
    bridge function: read values from the object & 
    call the actual fuction
    '''
    repo_create(args.path)

def repo_path(repo, *path):
    '''
    compute path under repo's gitdir
    '''
    return os.path.join(repo.gitdir, *path)

def repo_file(repo, *path, mkdir=False):
    '''
    create dirname if absent
    '''
    path = repo_path(repo, *path[:-1])

    if os.path.exists(path):
        if (os.path.isdir(path)):
            return path
        else:
            raise Exception('{0:s} is not a Git repository'.format(path))

    if mkdir:
        os.makedirs(path)
        return path

    return None

def repo_default_config():
    '''
    create configuration file: 
    repositoryformatversion = 0: the version of the gitdir format.
    filemode = false: disable tracking of file mode changes in the work tree.
    bare = false: indicates that this repository has a worktree.
    '''
    ret = configparser.ConfigParser()

    ret.add_section('core')
    ret.set('core', 'repositoryformatversion', '0')
    ret.set('core', 'filemode', 'false')
    ret.set('core', 'bare', 'false')

    return ret


class GitRepo(object):
    '''
    a git repo
    '''

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        '''
        init worktree and git dir
        read Configuration file:
        a INI-like file with a single section ([core]) + three fields.
        '''
        self.worktree = path
        self.gitdir = os.path.join(path, '.git')

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception('{0:s} is not a Git repository'.format(self.worktree))

        self.conf = configparser.configparser()
        # wait?
        cf = repo_file(self, 'config')
        if cf and os.path.exists(cf):
            self.config.Read([cf])
        elif not force:
            raise Exception('Configuration file missing.')

        if not force:
            vers = int(self.conf.get('core', 'repositoryformatversion'))
        if vers != 0:
            raise Exception('Unsupported repositoryformatversion: {0:s}'.format(vers))


def repo_create(path):
    '''
    create a new git repo at path
    init description, HEAD and config
    '''
    repo = GitRepository(path, True)


    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception ('{0:s} is not a directory!'.format(path))
        if os.listdir(repo.worktree):
            raise Exception('{0:s} is not empty!'.format(path))
    else:
        os.makedirs(repo.worktree)

    assert(repo_dir(repo, 'branches', mkdir=True))
    assert(repo_dir(repo, 'objects', mkdir=True))
    assert(repo_dir(repo, 'refs', 'tags', mkdir=True))
    assert(repo_dir(repo, 'refs', 'heads', mkdir=True))

    with open(repo_file(repo, 'description'), 'w') as f:
        f.write('Unnamed repository; edit the file \'description\' to name the repository.\n')

    with open(repo_file(repo, 'HEAD'), 'w') as f:
        f.write('ref: refs/heads/master\n')

    with open(repo_file(repo, 'config'), 'w') as f:
        config = repo_default_config()
        config.write(f)

    return repo




        