# -*- coding: utf-8 -*-
import IPy


def is_ip_valid(ip_number):
    try:
        IPy.IP(ip_number)
    except ValueError:
        return False
    return True
