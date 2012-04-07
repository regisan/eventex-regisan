from django import template
from django.template import Context, loader, Node

register = template.Library()

def do_youtube(parser, token):
    try:
        tag_name, id_ = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%r tag requires 1 argument' % token.contents.split()[0]
    return YoutubeNode(id_)
    
class YoutubeNode(Node):
    def __init__(self, id_):
        self.id = template.Variable(id_)
    
    def render(self, context):
        try:
            actual_id = self.id.resolve(context)
        except template.VariableDoesNotExist:
            actual_id = self.id
            
        t = loader.get_template('embed/youtube.html')
        c = Context({'id': actual_id}, autoescape=context.autoescape)
        return t.render(c)
        
register.tag('youtube', do_youtube)
