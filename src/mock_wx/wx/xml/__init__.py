from mock_wx._test_case import BaseClass
from wx import Object
XMLDOC_KEEP_WHITESPACE_NODES = {"XMLDOC_KEEP_WHITESPACE_NODES"}
XML_ATTRIBUTE_NODE = {"XML_ATTRIBUTE_NODE"}
XML_CDATA_SECTION_NODE = {"XML_CDATA_SECTION_NODE"}
XML_COMMENT_NODE = {"XML_COMMENT_NODE"}
XML_DOCUMENT_FRAG_NODE = {"XML_DOCUMENT_FRAG_NODE"}
XML_DOCUMENT_NODE = {"XML_DOCUMENT_NODE"}
XML_DOCUMENT_TYPE_NODE = {"XML_DOCUMENT_TYPE_NODE"}
XML_ELEMENT_NODE = {"XML_ELEMENT_NODE"}
XML_ENTITY_NODE = {"XML_ENTITY_NODE"}
XML_ENTITY_REF_NODE = {"XML_ENTITY_REF_NODE"}
XML_HTML_DOCUMENT_NODE = {"XML_HTML_DOCUMENT_NODE"}
XML_NOTATION_NODE = {"XML_NOTATION_NODE"}
XML_PI_NODE = {"XML_PI_NODE"}
XML_TEXT_NODE = {"XML_TEXT_NODE"}
XmlNodeType = {"XmlNodeType"}
class XmlAttribute(BaseClass):
    Name = {"Name"}
    Next = {"Next"}
    Value = {"Value"}
class XmlDoctype(BaseClass):
    FullString = {"FullString"}
    PublicId = {"PublicId"}
    RootName = {"RootName"}
    SystemId = {"SystemId"}
class XmlDocument(Object):
    Doctype = {"Doctype"}
    DocumentNode = {"DocumentNode"}
    EOL = {"EOL"}
    FileEncoding = {"FileEncoding"}
    FileType = {"FileType"}
    Root = {"Root"}
    Version = {"Version"}
class XmlNode(BaseClass):
    Attributes = {"Attributes"}
    Children = {"Children"}
    Content = {"Content"}
    Depth = {"Depth"}
    LineNumber = {"LineNumber"}
    Name = {"Name"}
    Next = {"Next"}
    NoConversion = {"NoConversion"}
    NodeContent = {"NodeContent"}
    Parent = {"Parent"}
    Type = {"Type"}
