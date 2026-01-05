from xml.etree import ElementTree


def _parse_item(elem):
    children = list(elem)
    if not children:
        return (elem.attrib.get('id'), (elem.text or ''))
    values = []
    for child in children:
        values.append(_parse_item(child))
    ids = [k for k, _ in values]
    if all(i is not None and i.isdigit() for i in ids):
        return (elem.attrib.get('id'), [v for _, v in values])
    return (elem.attrib.get('id'), {k: v for k, v in values})


def uc_unserialize(xml_bytes):
    s = xml_bytes.decode('latin-1') if isinstance(xml_bytes, (bytes, bytearray)) else xml_bytes
    root = ElementTree.fromstring(s)
    items = []
    for item in root.findall('item'):
        items.append(_parse_item(item))
    ids = [k for k, _ in items]
    if all(i is not None and i.isdigit() for i in ids):
        return [v for _, v in items]
    return {k: v for k, v in items}