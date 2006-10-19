# -*- coding: utf-8 -*-
##code-section module-header #fill in your manual code here
##/code-section module-header

from Products.feedfeeder.interfaces.contenthandler import IFeedItemContentHandler
from zope import interface

class StandardContentHandler:
    """
    """
    # zope3 interfaces
    interface.implements(IFeedItemContentHandler)

    ##code-section class-header_StandardContentHandler #fill in your manual code here
    ##/code-section class-header_StandardContentHandler


    def __init__(self, context):
        self.context = context

    def apply(self, contentNode):
        self.context.update(text=contentNode.toxml())


##code-section module-footer #fill in your manual code here

from zope.app.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from persistent.dict import PersistentDict

class AnnotationContentHandler(object):
    """A content handler that parses definition list entries to apply
    zope3 style annotations to the context.
    """

    interface.implements(IFeedItemContentHandler)

    ANNO_KEY = 'feedfeeder.metadata'

    def __init__(self, context):
        self.context = context

    def _extractText(self, node):
        s = node.toxml().strip()
        s = s[len(node.nodeName)+2:-1*(len(node.nodeName)+3)]
        return s

    def apply(self, contentNode):
        if not IAttributeAnnotatable.providedBy(self.context):
            directly = interface.directlyProvidedBy(self.context)
            interface.directlyProvides(self.context,
                                            directly + IAttributeAnnotatable)
        annotations = IAnnotations(self.context)
        metadata = annotations.get(self.ANNO_KEY, None)
        if metadata is None:
            metadata = PersistentDict()
            annotations[self.ANNO_KEY] = metadata

        for dl_el in contentNode.childNodes:
            if dl_el.nodeName != 'dl':
                continue

            term = None
            for el in dl_el.childNodes:
                if el.nodeName == 'dt':
                    term = self._extractText(el)
                elif el.nodeName == 'dd':
                    definition = self._extractText(el)
                    metadata[term] = definition

##/code-section module-footer


