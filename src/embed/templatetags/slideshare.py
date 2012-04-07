from django import template
from django.template import Context, loader, Node

register = template.Library()

def do_slideshare(parser, token):
    try:
        tag_name, id_, doc = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires 2 arguments' % token.contents.split()[0]
    return SlideShareNode(id_, doc)

class SlideShareNode(Node):
    def __init__(self, id_, doc):
        self.id = template.Variable(id_)
        self.doc = template.Variable(doc)
        
    def render(self, context):
        try:
            actual_id = self.id.resolve(context)
        except template.VariableDoesNotExist:
            actual_id = self.id
        
        try:
            actual_doc = self.doc.resolve(context)
        except template.VariableDoesNotExist:
            actual_doc = self.doc
            
        t = loader.get_template('embed/slideshare.html')
        c = Context({'id': actual_id, 'doc': actual_doc}, autoescape=context.autoescape)
        return t.render(c)
        
register.tag('slideshare', do_slideshare)
