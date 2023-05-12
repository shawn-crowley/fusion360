#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import os.path

def run(context):

    ui = None
    
    try:
        # Change this to your target export directory
        exportPath = "UPDATE THIS PART OF THE FILE PATH/STLAutomationExample"
        
        # Update this list with the sizes to create
        sizes = [125,130,135,140,145]

        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComponent = design.rootComponent
        exportMgr = design.exportManager
        sketches = rootComponent.sketches
        
        # Must match sketch name in Document Sketches
        textSketch = sketches.itemByName("Text")

        # Create the export directory if it isn't already there
        os.path.exists(exportPath) or os.mkdir(exportPath)
        
        for s in sizes:
            
            app.log("changing to " + str(s))
            
            # .sketchTexts returns the sketch text collection
            # Change the sketch text and majorAxis User Parameter
            textSketch.sketchTexts[0].text = str(s) + "MM"
            design.userParameters.itemByName("majorAxis").expression = str(float(s)) + " mm"
            
            # Repaint to see the body update
            app.activeViewport.refresh()
            
            # Create export options
            exportFile = exportPath + "/Example" + str(s)
            stlExportOptions = exportMgr.createSTLExportOptions(rootComponent,exportFile)
            stlExportOptions.sendToPrintUtility = False
            
            # Export STL file
            app.log("exporting " + exportFile)
            exportMgr.execute(stlExportOptions)
            app.log("done exporting " + exportFile)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
