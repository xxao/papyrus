#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
from wx.tools import img2py


# get images
try:
    from wx.lib.embeddedimage import PyEmbeddedImage
    imp = '#load libs\nfrom wx.lib.embeddedimage import PyEmbeddedImage\n\n\n'
except:
    imp = '#load libs\nimport cStringIO\nfrom wx import ImageFromStream, BitmapFromImage\n\n\n'

# convert images
for platform in ('mac', 'msw'):
    
    # create file
    image_file = open('images_'+platform+'.py', 'w')
    image_file.write(imp)
    image_file.close()
    
    # make commands
    commands = [
        "-f -a -u -i -n AppIcon16 "+platform+"/app_icon_16.png images_"+platform+".py",
        "-f -a -u -i -n AppIcon32 "+platform+"/app_icon_32.png images_"+platform+".py",
        "-f -a -u -i -n AppIcon48 "+platform+"/app_icon_48.png images_"+platform+".py",
        "-f -a -u -i -n AppIcon128 "+platform+"/app_icon_128.png images_"+platform+".py",
        "-f -a -u -i -n AppIcon256 "+platform+"/app_icon_256.png images_"+platform+".py",
        
        "-f -a -u -i -n IconCollectionLibrary "+platform+"/icon_collection_library.png images_"+platform+".py",
        "-f -a -u -i -n IconCollectionManual "+platform+"/icon_collection_manual.png images_"+platform+".py",
        "-f -a -u -i -n IconCollectionSmart "+platform+"/icon_collection_smart.png images_"+platform+".py",
        "-f -a -u -i -n IconCollectionLabel "+platform+"/icon_collection_label.png images_"+platform+".py",
        
        "-f -a -u -n IconViewCollections "+platform+"/icon_view_collections.png images_"+platform+".py",
        "-f -a -u -n IconViewDetails "+platform+"/icon_view_details.png images_"+platform+".py",
        "-f -a -u -n IconViewCharts "+platform+"/icon_view_charts.png images_"+platform+".py",
        
        "-f -a -u -n IconInfo "+platform+"/app_icon_48.png images_"+platform+".py",
        "-f -a -u -n IconPdf "+platform+"/icon_pdf.png images_"+platform+".py",
        "-f -a -u -n IconPdfMissing "+platform+"/icon_pdf_missing.png images_"+platform+".py",
        "-f -a -u -n BgrTopBar "+platform+"/bgr_top_bar.png images_"+platform+".py",
        "-f -a -u -n BgrBottomBar "+platform+"/bgr_bottom_bar.png images_"+platform+".py",
        "-f -a -u -n Spacer "+platform+"/spacer.png images_"+platform+".py",
    ]
    
    # convert images
    for command in commands:
        img2py.main(command.split())
