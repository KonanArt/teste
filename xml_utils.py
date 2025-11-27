import xmltodict

def dict_to_xml(data: dict, root="root"):
    return xmltodict.unparse({root: data}, pretty=True)

def xml_to_dict(xml_str: str):
    return xmltodict.parse(xml_str)
