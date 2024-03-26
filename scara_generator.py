import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Get extrude features
        extrudes = rootComp.features.extrudeFeatures

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Parametars
        diameter = 1.2
        num_of_holes_y = 5
        num_of_holes_x = 10
        spacing = 0.2
        offset_x = diameter/2 + spacing
        offset_y = diameter/2 + spacing
        i = 1
        a = 1 
        rec_end_x = num_of_holes_x*(diameter/2) + (num_of_holes_x)*offset_x + spacing
        rec_end_y = num_of_holes_y*(diameter/2) + (num_of_holes_y)*offset_y + spacing

        # Draw some circles.
        circles = sketch.sketchCurves.sketchCircles
        while a <= num_of_holes_y:
            while i <= num_of_holes_x:
                circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(offset_x, offset_y, 0), diameter/2)
                offset_x = offset_x + diameter + spacing
                i += 1
            i = 1
            offset_x = diameter/2 + spacing
            offset_y = offset_y + diameter + spacing
            a += 1

        # Create a rectangle
        lines = sketch.sketchCurves.sketchLines;

        #recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(rec_end_x, rec_end_y, 0))
        line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(rec_end_x, 0, 0))
        line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(rec_end_x, rec_end_y, 0))
        line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(0, rec_end_y, 0))
        line4 = lines.addByTwoPoints(line3.endSketchPoint, adsk.core.Point3D.create(0, 0, 0))
        # Add a fillet
        arc1 = sketch.sketchCurves.sketchArcs.addFillet(line1, line1.endSketchPoint.geometry, line2, line2.startSketchPoint.geometry, 0.5)
        arc2 = sketch.sketchCurves.sketchArcs.addFillet(line2, line2.endSketchPoint.geometry, line3, line3.startSketchPoint.geometry, 0.5)
        arc3 = sketch.sketchCurves.sketchArcs.addFillet(line3, line3.endSketchPoint.geometry, line4, line4.startSketchPoint.geometry, 0.5)
        arc4 = sketch.sketchCurves.sketchArcs.addFillet(line4, line4.endSketchPoint.geometry, line1, line1.startSketchPoint.geometry, 0.5)

        # Get the profile
        prof1 = sketch.profiles.item(num_of_holes_y*num_of_holes_x)
        #prof2 = sketch.profiles.item(0)

        # Extrude the sketch
        # Extrude Sample 1: A simple way of creating typical extrusions (extrusion that goes from the profile plane the specified distance1).
        # Define a distance1 extent of 2 cm
        distance1 = adsk.core.ValueInput.createByReal(2)
        distance2 = adsk.core.ValueInput.createByReal(0.5)
        extrude1 = extrudes.addSimple(prof1, distance1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        #extrude2 = extrudes.addSimple(prof2, distance2, adsk.fusion.FeatureOperations.JoinFeatureOperation)   
        b = 0; 
        while b < num_of_holes_y*num_of_holes_x:
            prof2 = sketch.profiles.item(b)
            extrude2 = extrudes.addSimple(prof2, distance2, adsk.fusion.FeatureOperations.JoinFeatureOperation)
            b += 1

        # Get the extrusion body
        body1 = extrude1.bodies.item(0)
        body1.name = "simple"

        # Get the state of the extrusion
        health = extrude1.healthState
        if health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState or health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState:
            message = extrude1.errorOrWarningMessage
        
        # Get the state of timeline object
        timeline = design.timeline
        timelineObj = timeline.item(timeline.count - 1);
        health = timelineObj.healthState
        message = timelineObj.errorOrWarningMessage
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))