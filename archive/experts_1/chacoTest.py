#!/usr/bin/env python
"""Plot chaco graphics in wxFrame (with option to save as PDF)."""
#--------------------------------------------------------------------------------
#
#  Plot chaco graphics in a wxPython wxFrame window (with option to save as PDF).
#
#  Written by: Andrew D. Straw
#
#  Date: 04/18/2003
#
#  (c) Copyright 2003 by Andrew D. Straw
#  May be distributed under terms of Scipy license (BSD style).
#
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
#  Imports:
#--------------------------------------------------------------------------------

from wxPython.wx  import *
from chaco.wxplot import *
from Numeric      import pi
import Experts

try:
    import kiva.pdfcore2d
except:
    have_pdf = False
else:
    have_pdf = True

#--------------------------------------------------------------------------------
#  Constants:
#--------------------------------------------------------------------------------

try:
    True
except NameError:
    True  = 1 == 1
    False = 1 == 0

# Screen size:
screen_dx = wxSystemSettings_GetSystemMetric( wx.wxSYS_SCREEN_X ) or 1024
screen_dy = wxSystemSettings_GetSystemMetric( wx.wxSYS_SCREEN_Y ) or 768

#=============================================================================== 
#  SimpleFigureFrame class
#=============================================================================== 

class SimpleFigureFrame( wxFrame ):
    """A simple, interactive wxFrame that plots chaco graphics"""
    def __init__( self, *args, **kw ):
        wxFrame.__init__( *(self,) + args, **kw )
        self.my_item = None
        self.SetAutoLayout( True )
        self.Show( True )
        self._redraw()
        
    def _redraw( self ):
        # Get rid of anything already here:
        self.DestroyChildren() 
    
        box = wxBoxSizer( wxVERTICAL )
        if self.my_item is not None:
            pw = PlotWindow( self,-1 )
            pw.add( self.my_item )
            box.Add( pw, 1, wxEXPAND )

            # Only add button if there's PDF support available:
            if have_pdf: 
                btn = wxButton( self, -1, "Save as PDF..." )
                box.Add( btn, 0, wxEXPAND )
                EVT_BUTTON( self, btn.GetId(), self.save_pdf )
        else:
            box.Add( wxStaticText( self, -1, 
                     "No chaco item set. (Call set_item() method.)" ), 
                     1, wxEXPAND )

        self.SetSizer( box )
        self.Layout() # tell wx to call the layout algorithm again
            
    def set_item( self, item ):
        """Insert your chaco graphics item with this call

        Your item can be a PlotGroup, PlotIndexed, PlotCanvas, or
        PlotValue."""
        
        self.my_item = item
        self._redraw()
        
    def save_pdf( self, event ):
        """Handle button-press event to save item as PDF file"""
        if self.my_item is None:
            raise RuntimeError( "save_pdf called before set_item()" )
        
        dlg = wxFileDialog( self,"Choose a filename", "", 
                            "figure.pdf","PDF files (*.pdf)|*.pdf",
                            wxSAVE | wxOVERWRITE_PROMPT )
                            
        try:
            if dlg.ShowModal() == wxID_OK:
                # Get a kiva PDF canvas:
                canv = kiva.pdfcore2d.Canvas( filename = dlg.GetPaths()[0] )
        
                # Get the canvas's associated kiva GraphicsContext:
                gc = canv.gc
                
                # Rotate/Translate from portrait to landscape mode:
                gc.rotate_ctm( 90.0 * (2.0 * pi) / 360.0 )
                gc.translate_ctm( 0.0, -590.0 )
                
                # Render the plot as PDF:
                self.my_item.render( gc, 40, 35, 752, 510 )
                
                # Save it to the specified file:
                canv.save()
        finally:
            dlg.Destroy()

#=============================================================================== 
#  'plot_it' function:
#=============================================================================== 

def plot_it( object ):
    """Run SimpleFigureFrame with your chaco graphics object."""
    app   = wxPySimpleApp()
    frame = SimpleFigureFrame( None, -1, "Plot" )
    frame.SetSize( ( 2 * screen_dx / 3, 2 * screen_dy / 3 ) )
    frame.set_item( object )
    app.SetTopWindow( frame )
    frame.Show( True )
    app.MainLoop()

#=============================================================================== 
#  Chaco use demonstration:
#=============================================================================== 

def main():
    """Demonstration of chaco"""
    
    import Numeric
    x  = Numeric.arange( 200 )
    #a = Experts.VectorExpertsProblem(75,100,1)
    a = Experts.ScalarExpertsProblem(20,1)
    result = a.mixture(200,0.9)
    y1 = result[0]
    b = result[1]
    y2 = Numeric.repeat([b],200)
    
#    y1 = 10 * Numeric.sin( x * 0.3 ) + 3 * Numeric.sin( x * 0.2 ) + 15
##    y2 =  8 * Numeric.cos( x * 0.3 ) + 3 * Numeric.sin( x * 0.2 ) + 15
##    y3 =  2 * Numeric.sin( x * 0.5 ) + 1 * Numeric.sin( x * 0.1 )
##    y4 =  8 * Numeric.cos( x * 0.2 ) + 3 * Numeric.sin( x * 0.1 )
##
    x_ax = PlotAxis( title = 'Time' )
    y_ax = PlotAxis( title = 'Loss' )
    pv1  = PlotValue( zip( x, y1 ),
                    axis_index = x_ax,
                    axis       = y_ax,
                    type       = 'line',
                    line_color = 'blue' )
    pv2  = PlotValue( zip( x, y2 ),
                    axis_index = x_ax,
                    axis       = y_ax,
                    type       = 'line',
                    line_color = 'red' )
##    pv2 = PlotValue( zip( x, y2 ),
##                    axis_index = x_ax,
##                    axis       = y_ax,
##                    type       = 'line,scatter',
##                    symbol     = 'cross',
##                    line_color = 'green')
##
##    pv3       = PlotValue( y3 )
##    pv4       = PlotValue( y4 )
##    x_val     = PlotValue( x )
##    fill_canv = PlotCanvas( pv3, pv4, plot_type = 'rangebar', index = x_val,
##                                      axis_index = x_ax, axis = y_ax )
    pc        = PlotCanvas( pv1,pv2,
                    PlotTitle( 'Vector Experts Experiment' ),
                    margin = 15 )
    plot_it( pc )

#=============================================================================== 
#  Program start-up:
#=============================================================================== 

if __name__ == '__main__':
    main()
