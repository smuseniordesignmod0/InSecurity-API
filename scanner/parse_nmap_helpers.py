# python3

from libnmap.parser import NmapParser
from shared_functions import *


def libnmap_parse_xml(xml_path):
    """
    Read in nmap scan from xml file with NmapParser from libnmap library
    :param xml_path: 
    :return: 
    """
    try:
        return NmapParser.parse_fromfile(xml_path)
    
    except Exception as e:
        print(e, file=sys.stderr)
        print("Error with nmap XML format in file: %s" % xml_path, file=sys.stderr)
        
        return None


def cpe_object_to_dict(libnmap_cpe_obj):
    service_cpe_list = {
        'cpeString': default_value(str),
        'getProduct': default_value(str),
        'getUpdate': default_value(str),
        'getVendor': default_value(str),
        'getVersion': default_value(str),
        'isApplication': default_value(bool),
        'isHardware': default_value(bool),
        'isOperatingSystem': default_value(bool)
    }

    if hasattr(libnmap_cpe_obj, 'cpestring'):
        service_cpe_list['cpeString'] = return_json_value(libnmap_cpe_obj.cpestring, str)
    else:
        service_cpe_list['cpeString'] = return_json_value(libnmap_cpe_obj, str)

    if hasattr(libnmap_cpe_obj, 'getProduct'):
        service_cpe_list['getProduct'] = return_json_value(libnmap_cpe_obj.getProduct, str)

    if hasattr(libnmap_cpe_obj, 'getUpdate'):
        service_cpe_list['getUpdate'] = return_json_value(libnmap_cpe_obj.getUpdate, str)

    if hasattr(libnmap_cpe_obj, 'getVendor'):
        service_cpe_list['getVendor'] = return_json_value(libnmap_cpe_obj.getVendor, str)

    if hasattr(libnmap_cpe_obj, 'getVersion'):
        service_cpe_list['getVersion'] = return_json_value(libnmap_cpe_obj.getVersion, str)

    if hasattr(libnmap_cpe_obj, 'is_application'):
        service_cpe_list['isApplication'] = return_json_value(libnmap_cpe_obj.is_application, bool)

    if hasattr(libnmap_cpe_obj, 'is_hardware'):
        service_cpe_list['isHardware'] = return_json_value(libnmap_cpe_obj.is_hardware, bool)

    if hasattr(libnmap_cpe_obj, 'is_operating_system'):
        service_cpe_list['isOperatingSystem'] = return_json_value(libnmap_cpe_obj.is_operating_system, bool)

    return service_cpe_list


def libnmap_host_to_device_schema(host):
    device = {
        'Vulnerability_Score': default_value(int),
        'IP': return_json_value(host.get("ip"), str),             
        'MAC_Address':  return_json_value(host.get("mac"), str),
        'Vendor': return_json_value(host.get("vendor"), str),
        'host_CPE_list': [],
        'host_CVE_list': [],
        'Services': [],                                         
        'Identification_Accuracy': default_value(int)
    }

    # Host CPE list
    host_cpe_list = []
    
    for c in host.get('cpes'):
        host_cpe_list.extend(c.get('cpe'))
    
    host_cpe_list = list(set(host_cpe_list))
    device['host_CPE_list'] = [cpe_object_to_dict(c) for c in host_cpe_list]

    # Services
    for s in host.get('services'):
        service={
            'port': s.get('port'),#return_json_value(s.port,int),
            'banner': s.get('banner'),#return_json_value(s.banner,str),
            'protocol': s.get('protocol'),#return_json_value(s.protocol, str),
            'name': s.get('service'),#return_json_value(s.service, str),
            'state': s.get('state'),#return_json_value(s.state,str),
            'reason': s.get('reason'),#return_json_value(s.reason,str),
            'service_CPE_list': [],
            'service_CVE_list': []
        }

        #if s.cpelist:
        if "cpelist" in s:
            # Service CPE list
            for c in s.get('cpelist'):
                service['service_CPE_list'].append(cpe_object_to_dict(c))

        device['Services'].append(service)

    return device
