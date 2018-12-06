#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     06-12-2018
# Copyright:   (c) User 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# StdLib
import time
import os
import random
import logging
import logging.handlers
import datetime
import json
import cookielib
import re
# Remote libraries
import requests
import requests.exceptions
# local
import common










def find_last_post_date(html):
    return last_post_Date




def load_archive(req_ses, blog_name):
    base_url = 'http://{0}.tumblr.com/archive'.format(blog_name)
    all_history = ''
    # Load first block
    first_response = common.fetch(
        requests_session=req_ses,
        url=base_url,
        method='get',
    )
    common.write_file(
        file_path=os.path.join('debug', 'first_response.html'),
        data=first_response.content
    )
    all_history += first_response.content
    # Find last post date
    last_post_date = find_last_post_date(html = first_response.content)
    # Load subsequent history
    while True:
        # Load next block
        scroll_url = 'http://{0}.tumblr.com/archive?before_time={1}'.format(blog_name, last_post_date)
        scroll_response = common.fetch(
            requests_session=req_ses,
            url=base_url,
            method='get',
        )
        common.write_file(
            file_path=os.path.join('debug', 'scroll_response.html'),
            data=scroll_response.content
        )
        all_history += scroll_response.content
        # Find last post date
        last_post_date = find_last_post_date(html = scroll_response.content)
        # Stop if no more posts
        if not last_post_date:
            break

    # Store combined page
    common.write_file(
        file_path=os.path.join('debug', 'all_history.html'),
        data=all_history
    )
    return all_history





def main():
    # Setup requests session
    req_ses = requests.Session()
    # Load history
    load_archive(
        req_ses=req_ses,
        blog_name='askflufflepuff',
        )

if __name__ == '__main__':
    common.setup_logging(os.path.join("debug", "load_all_archive.log.txt"))# Setup logging
    try:
        main()
    # Log exceptions
    except Exception, e:
        logging.critical(u"Unhandled exception!")
        logging.exception(e)
    logging.info(u"Program finished.")