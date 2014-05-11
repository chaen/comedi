from django.views.generic.base import TemplateResponseMixin
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.lib.pagesizes import  A4, landscape



# class NumberedCanvas( canvas.Canvas ):
#   def __init__( self, *args, **kwargs ):
#     canvas.Canvas.__init__( self, *args, **kwargs )
#     self._saved_page_states = []
#
#   def showPage( self ):
#     self._saved_page_states.append( dict( self.__dict__ ) )
#     self._startPage()
#
#   def save( self ):
#       """add page info to each page (page x of y)"""
#       num_pages = len( self._saved_page_states )
#       for state in self._saved_page_states:
#           self.__dict__.update( state )
#           self.draw_page_number( num_pages )
#           canvas.Canvas.showPage( self )
#       canvas.Canvas.save( self )
#
#   def draw_page_number( self, page_count ):
#     # Change the position of this to wherever you want the page number to be
#     self.drawRightString( 211 * mm, 15 * mm + ( 0.2 * inch ),
#                          "Page %d of %d" % ( self._pageNumber, page_count ) )



def render_to_pdf( productName, table_title, table_attribute, items ):
    """ https://docs.djangoproject.com/en/dev/howto/outputting-pdf/ """

    response = HttpResponse( content_type = 'application/pdf' )
    pdfBuffer = BytesIO()

    doc = SimpleDocTemplate( pdfBuffer,
                            rightMargin = 72,
                            leftMargin = 72,
                            topMargin = 72,
                            bottomMargin = 72,
                            pagesize = landscape( A4 ) )

    # Our container for 'Flowable' objects
    elements = []

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    elements.append( Paragraph( "FAR %s" % productName, styles['Title'] ) )

    # Need a place to store our table rows
    table_data = [table_title]
    for item in items:
        # Add a row to the table
        row = [getattr( item, attr ) for attr in table_attribute]
        table_data.append( row )

    # Create the table
    user_table = Table( table_data, colWidths = [doc.width / 5.0] * 5 )
    user_table.setStyle( TableStyle( [( 'INNERGRID', ( 0, 0 ), ( -1, -1 ), 0.25, colors.black ),
                                    ( 'BOX', ( 0, 0 ), ( -1, -1 ), 0.25, colors.black )] ) )

    elements.append( user_table )
    doc.build( elements )

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = pdfBuffer.getvalue()
    pdfBuffer.close()

    response.write( pdf )
    return response

class PDFResponseMixin( TemplateResponseMixin ):
  """
  Mixin for Django class based views.
  Switch normal and pdf template based on request.

  The switch is made when the request has a particular querydict, per
  class attributes, `pdf_querydict_keys` and `pdf_querydict_value`
  example:

      http://www.example.com?[pdf_querydict_key]=[pdf_querydict_value]

  Example with values::

      http://www.example.com?format=pdf

  Simplified version of snippet here:
  http://djangosnippets.org/snippets/2540/
  """
  pdf_querydict_key = 'format'
  pdf_querydict_value = 'pdf'

  def is_pdf( self ):
    value = self.request.REQUEST.get( self.pdf_querydict_key, '' )
    return value.lower() == self.pdf_querydict_value.lower()

  def get_pdf_response( self, context, **response_kwargs ):
    prodName = self.request.session.get( 'far_form', {} ).get( 'product', 'UNKNOWN' )
    return render_to_pdf( prodName , self.pdf_table_title, self.pdf_table_attribute, self.get_queryset() )

  def render_to_response( self, context, **response_kwargs ):
    if self.is_pdf():
      return self.get_pdf_response( context, **response_kwargs )
    # context[self.pdf_url_varname] = self.get_pdf_url()
    return super( PDFResponseMixin, self ).render_to_response( 
        context, **response_kwargs )

#
#
# from django.template import Library, Node, resolve_variable, TemplateSyntaxError
#
# class AddParameter( Node ):
#   def __init__( self, varname, value ):
#     self.varname = varname
#     self.value = value
#
#   def render( self, context ):
#     req = resolve_variable( 'request', context )
#     params = req.GET.copy()
#     params[self.varname] = self.value
#     return '%s?%s' % ( req.path, params.urlencode() )
#
# def addurlparameter( parser, token ):
#   try:
#     tag_name, varname, value = token.split_contents()
#     print "tag_name %s format_string %s value %s" % ( tag_name, varname, value )
#   except ValueError:
#     raise TemplateSyntaxError, "'%s' tag requires two arguments" % tag_name
#   return AddParameter( varname, value )
#
#
#
# def toPdf( parser, token ):
#   tag_name, format_string = token.split_contents()
#   print "tag_name %s format_string %s" % ( tag_name, format_string )
#   return "pdf"
























