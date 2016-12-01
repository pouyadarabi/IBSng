import re

mac_address_check_pattern=re.compile("^[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}$")
def checkMacAddress(mac_addr):
    """
        return True if mac_addr is valid, else return False
    """
    if mac_address_check_pattern.match(mac_addr)!=None:
        return True
    return False
    