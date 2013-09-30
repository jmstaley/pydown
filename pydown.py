#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
import shutil
import optparse

from markdown import markdown
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('pydown', 'templates'))


HERE = os.path.abspath(os.path.dirname(__file__))
markdown_options = ['extra', 'codehilite']


def copy(dst, theme):
    if os.path.exists(os.path.join(dst)):
        shutil.rmtree(os.path.join(dst))
    shutil.copytree(os.path.join(HERE, 'templates', 'css'),
                    os.path.join(dst, "css"))
    shutil.copy(os.path.join(HERE, 'templates', 'themes', '%s.css' % theme),
                os.path.join(dst, 'css', '%s.css' % theme))
    shutil.copytree(os.path.join(HERE, 'templates', 'js'),
                    os.path.join(dst, 'js'))


def slides_split(slides):
    data = ''
    css = ''
    for item in slides.split('\n'):
        if item.startswith('!SLIDE'):
            yield css, data
            css = ' '.join(item.split(' ')[1:])
            data = ''
        else:
            data += item+'\n'
    yield css, data


def handle(md, dst, theme='web-2.0', status=False):
    copy(dst, theme)
    slides = codecs.open(md, 'r', 'utf-8').read()
    data = ''
    for css, item in slides_split(slides):
        if not item:
            continue
        data += '<section class="slide %s">' % css\
                + '<div class="content">'\
                + markdown(item, markdown_options)\
                + '</div>'\
                + '</section>\n'
    template = env.get_template('index.html')
    html = template.render(slide=data, theme=theme, status=status)
    f = codecs.open(os.path.join(dst, 'index.html'), 'w', 'utf-8')
    f.write(html)
    f.close()

def main():
    '''Main entry point for the pydown CLI.'''
    usage = "usage: %prog [options] mdfile directory"
    parser = optparse.OptionParser(usage=usage)
    # add in the theme option
    parser.add_option("-t", "--theme", 
                      dest="theme", 
                      default='web-2.0', 
                      help="theme to copy")
    # deck.js status option
    parser.add_option("-s", "--status",
                      action="store_true",
                      default=False,
                      dest="status",
                      help="turn on deck.js status")
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.print_help()
    else:
        handle(*args, theme=options.theme, status=options.status)

if __name__ == '__main__':
    main()
