#coding=utf8

import sys
import re
import os

BOOK_ARCHIVE_DIR_NAME = 'book_archive_directory'
VDO_ARCHIVE_DIR_NAME = 'vdo_archive_directory'
DUBLIN_CORE_FILE_NAME = 'dublin_core.xml'
CONTENTS_FILE_NAME = 'contents'

if len(sys.argv) < 2:
    print('Please specify a file to be converted as the first argument.')
    exit()

filename = sys.argv[1]

with open(filename, "r") as f:
    content = f.read()
    # Convert RDF Dublin Core to DSpace Dublin Core Simple Archive Format
    content = re.sub(r'\s\s<(\/?)rdf:Description', r'<\1dublin_core', content)
    content = re.sub(r'(\.|\s|\,|\/)*</dc:.+>', r'</dcvalue>', content)
    content = re.sub(r'\s\s<dc:(\w+)>', r'<dcvalue element="\1">', content)
    content = re.sub(r'<(\/)?rdf:RDF.*>', '', content)

    # Convert some elements to supported DSpace elements
    content = re.sub(r'element="creator"', r'element="contributor" qualifier="author"', content)
    content = re.sub(r'element="date"', r'element="date" qualifier="issued"', content)
    content = re.sub(r'element="identifier"', r'element="relation" qualifier="uri"', content)
    content = re.sub(r'element="format"', r'element="format" qualifier="mimetype"', content)
    content = re.sub(r'element="type">.*?</dcvalue>', r'element="type">เอกสารสิ่งพิมพ์</dcvalue>', content)
    content = re.sub(r'element="language">tha</dcvalue>', r'element="language">th</dcvalue>', content)

    # Create Simple Archive Structure to be imported to DSpace
    os.mkdir(BOOK_ARCHIVE_DIR_NAME)
    os.mkdir(VDO_ARCHIVE_DIR_NAME)

    # Extract each item to create its own directory structure
    book_count = 0
    vdo_count = 0
    for idx, item in enumerate(re.findall(r'(<dublin_core>.*?</dublin_core>)', content, flags=re.DOTALL)):
        if 'healthstation.in.th' in item:
            archive_dir = VDO_ARCHIVE_DIR_NAME
            vdo_count += 1
            count = vdo_count
            item = re.sub(r'element="type">.*?</dcvalue>', r'element="type">สื่อมัลติมีเดีย</dcvalue>', item)
            item = re.sub(r'</dublin_core>', r'  <dcvalue element="subject" qualifier="classification">VDO</dcvalue>\n</dublin_core>', item)
            item = re.sub(r'(<dcvalue element="relation" qualifier="uri">.+)</dcvalue>', r'\1/</dcvalue>', item)
        else:
            archive_dir = BOOK_ARCHIVE_DIR_NAME
            book_count += 1
            count = book_count
        item_dir = archive_dir + '/item_' + str(count).zfill(5)
        os.mkdir(item_dir)
        with open(item_dir + '/'+ DUBLIN_CORE_FILE_NAME, 'w') as xml_file:
            xml_file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            xml_file.write(item + '\n')

        # Create empty contents file that is mandatory for importing to DSpace
        # (Actually, this file is used to specify bistream file names)
        open(item_dir + '/' + CONTENTS_FILE_NAME, 'w').close()

