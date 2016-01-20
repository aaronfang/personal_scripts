# DreamWorks Animation LLC Confidential Information.
# TM and (c) 2011 DreamWorks Animation LLC.  All Rights Reserved.
# Reproduction in whole or in part without prior written permission of a
# duly authorized representative is prohibited.
"""
mod_applyMayaColors
----------------------------------------------------------------------

author: maross

"""

import odwmodeling.maya.parts.part_class_sets
import odwmodeling.maya.parts.color
import odwmaya
from dwacore import io

__author__ = "Michael Ross"

def mod_applyMayaColors():
    cmd = ApplyMayaColorsCmd()
    cmd.run()

run = mod_applyMayaColors

class ApplyMayaColorsCmd(object):
    
    pdiColorAttrName = "PDI_color"
    pdiColorAttrType = "double3"
    pdiTranspAttrName = "PDI_transparency"

    def __init__(self):
        import maya.OpenMaya
        self.maya = odwmaya.importMaya()

        self.mcmd = self.maya.cmds
        self.mmel = self.maya.mel
        self.mapi = self.maya.OpenMaya

        self.pco = odwmodeling.maya.parts.part_class_sets.PartClassSets()

        self.partColorer = odwmodeling.maya.parts.color.Colorer(self.pco)

    def run(self):
        """Apply Maya colors to the selected objects."""

        mcmd = self.mcmd

        self.shadingGroupMembers = {}        

        selection = mcmd.ls(sl=1)

        shapes = mcmd.ls(selection, dag=1, shapes=1)
        
        for shape in shapes:
            
            if mcmd.objectType(shape, isAType="nurbsSurface"):
                self.applyNurbsColor(shape)

            if mcmd.objectType(shape, isAType="mesh"):
                self.applyMeshColor(shape)
                io.write("shape = %s" % (shape))

        if selection: mcmd.select(selection)

    def applyNurbsColor(self, nurbs):
        """Apply the maya colors to the given mesh.  Raise an error if the
        NURBS has shaders with a complex color attribute.

        nurbs: string

            string name of a nurbs shape.
        """
        shaderGroups = self.mcmd.listSets(type=1, o=nurbs)
        if not shaderGroups:

            raise ApplyMayaColorsError(
                "No shader groups found on nurbs object %s" % (nurbs))

        material = self.getMaterialFromSG(shaderGroups[0])

        rgbt = self.materialToRGBT(material)
        self.setPDIColorAttr(nurbs, rgbt)
        self.setPDITranspAttr(nurbs, rgbt[-1])


    def applyMeshColor(self, mesh):
        """Apply the maya colors to the given mesh.

        :Parameters:

            mesh: string

                String name of a mesh shape.
        """
        pco = self.pco
        meshMaterial = self.getMeshMaterial(mesh)

        if not meshMaterial:
            return

        meshRGBT = self.materialToRGBT(meshMaterial)
        
        partFaceDict = pco.objectsToPartFaceDict(mesh)

        meshRGBTCounts = {}
        
        partRGBTs = {}

        for partId,partFaces in partFaceDict.items():
            partFaces = self.mcmd.ls(partFaces, fl=1)
            partSGs = self.partColorer.getCurrentSGsFromPart(partId)

            # If multiple colors are found, pick the color that has the
            # majority of faces.  Note that we're comparing RGB values,
            # not just simple shaders.
            # 
            if len(partSGs) > 1:
                    
                rgbtCounts = {}

                for sg in partSGs:

                    partMaterial = self.partColorer.getMaterialFromSG(sg)
                    rgbt = self.materialToRGBT(partMaterial)
                    if rgbt not in rgbtCounts:
                        rgbtCounts[rgbt] = 0

                    tmpSet = pco.createSet(
                        "mod_applyMayaColors_tmpSet", partFaces)

                    partFacesInSg = self.mcmd.sets(tmpSet, intersection=sg)
                    rgbtCounts[rgbt] += len(self.mcmd.ls(partFacesInSg, fl=1))
                    self.mcmd.delete(tmpSet)

                # The above does not account for materials on the mesh
                # itself.  We assume that any faces not counted are colored
                # by the meshRGBT.
                # 
                totalFaceColorCount = sum(rgbtCounts.values())
                meshColoredFaceCount = len(partFaces) - totalFaceColorCount

                if meshRGBT in rgbtCounts:
                    meshColoredFaceCount += rgbtCounts[meshRGBT]
                    
                rgbtCounts[meshRGBT] = meshColoredFaceCount
                    
                # Find the rgbt for the shader group with the most faces.
                # 
                partRGBTPair = max(rgbtCounts.items(), key=lambda x: x[1])
                partRGBT = partRGBTPair[0]
                
            else:

                partMaterial = self.partColorer.getMaterialFromSG(partSGs[0])
                partRGBT = self.materialToRGBT(partMaterial)

            meshRGBTCounts[partRGBT] = len(partFaces)

            partName = pco.getPartName(partId)
            partSet = pco.getMayaSetName(partName, mesh)

            partRGBTs[partId] = partRGBT

            # If this part has a different color than the overall mesh, set
            # the attribute.  Otherwise, delete the attribute, this part
            # should not be colored separately from the full mesh.
            # 
            if partRGBT[:3] != meshRGBT[:3]:
                self.setPDIColorAttr(partSet, partRGBT[:3])
            else:
                self.removePDIColorAttr(partSet)

            # Do the same for transparency, separately.  Transparency on the
            # mm is not tied to the color.
            # 
            if partRGBT[-1] != meshRGBT[-1]:
                self.setPDITranspAttr(partSet, partRGBT[-1])
            else:
                self.removePDITranspAttr(partSet)

        if not meshRGBT:
            meshRGBT = max(meshRGBTCounts.items(), key=lambda x: x[1])[0]

            # Clean up parts with same color as meshRGBT
            # 
            for partId, partRGBT in partRGBTs.items():

                partName = pco.getPartName(partId)
                partSet = pco.getMayaSetName(partName, mesh)

                if partRGBT[:3] == meshRGBT[:3]:
                    self.removePDIColorAttr(partSet)

                if partRGBT[-1] == meshRGBT[-1]:
                    self.removePDITranspAttr(partSet)

        # Set the color attribute on the mesh.
        # 
        self.setPDIColorAttr(mesh, meshRGBT)


                
    def setPDIColorAttr(self, obj, rgb):
        """Set the PDI Color attribute on the given object."""
        mcmd = self.mcmd
        attrName = self.pdiColorAttrName
        objAttrName = "%s.%s" % (obj, attrName)

        if not mcmd.attributeQuery(attrName, node=obj, exists=1):
            mcmd.addAttr(
                obj, usedAsColor=1, attributeType="float3", longName=attrName)
            mcmd.addAttr(obj, at="float", ln=attrName+"R", parent=attrName)
            mcmd.addAttr(obj, at="float", ln=attrName+"G", parent=attrName)
            mcmd.addAttr(obj, at="float", ln=attrName+"B", parent=attrName)

        #io.write("Applying Color (%.2f, %.2f, %.2f) to %s" % (
        #        rgb[0], rgb[1], rgb[2], obj))
        mcmd.setAttr(objAttrName, rgb[0], rgb[1], rgb[2], type="double3")

    def setPDITranspAttr(self, obj, value):
        """Set the PDI Color attribute on the given object."""
        mcmd = self.mcmd
        attrName = self.pdiTranspAttrName
        objAttrName = "%s.%s" % (obj, attrName)

        if not mcmd.attributeQuery(attrName, node=obj, exists=1):
            mcmd.addAttr(obj, attributeType="float", longName=attrName)

        io.write("Applying Transparency (%.2f) to %s" % (value, obj))
        mcmd.setAttr(objAttrName, value)


    def removePDIColorAttr(self, obj):
        """Remove the PDI_color attribute if it exists."""
        attrName = self.pdiColorAttrName

        if self.mcmd.attributeQuery(attrName, node=obj, exists=1):
            self.mcmd.deleteAttr("%s.%s" % (obj, attrName))
            io.write("Removing color from %s" % (obj))

    def removePDITranspAttr(self, obj):
        """Remove the PDI_transparency attribute if it exists."""
        attrName = self.pdiTranspAttrName

        if self.mcmd.attributeQuery(attrName, node=obj, exists=1):
            self.mcmd.deleteAttr("%s.%s" % (obj, attrName))
            io.write("Removing transparency from %s" % (obj))


    def materialToRGBT(self, material):
        """Return the (r,g,b, transparency) triplet from the given material.
        Note that this is transparency, the complement of alpha."""
        if not material:
            return None
        rgb = self.mcmd.getAttr("%s.color" % (material))[0]
        t = self.mcmd.getAttr("%s.transparency" % (material))[0]
        return (rgb[0], rgb[1], rgb[2], t[0])
        
        
    def getMeshMaterial(self, mesh):
        """Return the shader applying colors to given mesh as a whole (not
        just a subset of the faces.

        If no shader is found for the mesh as a whole, then we find the
        number of faces each shader is applied to.  The shader applied to
        the most faces is assumed to be the mesh color.
        """
        mcmd = self.mcmd

        shadingEngineType = 1
        meshShaderGroups = mcmd.listSets(type=shadingEngineType, o=mesh)

        if not meshShaderGroups:
            return None

        if len(meshShaderGroups) == 1:
            material = self.getMaterialFromSG(meshShaderGroups[0])
            return material

        # Create a set with all the faces of this mesh in it.
        # 
        meshFaceSet = mcmd.sets(
            name="mod_applyMayaColors_getMeshMaterial_tempSet", empty=1)
        mcmd.sets("%s.f[*]" % (mesh), e=1, fe=meshFaceSet)
        
        faceCounts = {}

        try:
            for sg in meshShaderGroups:

                contents = self.getSetContents(sg)

                # If this shading group contains the mesh shape, return the
                # material for this shading group.
                # 
                if mesh in contents:
                    return self.getMaterialFromSG(sg)

                intersection = mcmd.sets(meshFaceSet, intersection=sg)
                faceCounts[sg] = len(mcmd.ls(intersection, fl=1))

        finally:
            mcmd.delete(meshFaceSet)

        # Use the shader group that was applied to the most faces.
        # 
        meshSG = max(faceCounts.keys(), key=(lambda sg: faceCounts[sg]))
        material = self.getMaterialFromSG(meshSG)
        
        return material
            
    def getSetContents(self, s):
        """Return the members of s, using cached results when possible.
        """
        if s in self.shadingGroupMembers:
            return self.shadingGroupMembers[s]

        mcmd = self.mcmd
        
        contents = mcmd.sets(s, q=1)
        contents = set(mcmd.ls(contents))
        self.shadingGroupMembers[s] = contents

        return contents 
            
    def getMaterialFromSG(self, sg):
        """Return the material connected to the given shading group.
        """
        self.pco.procPrint()
        material = str(self.mcmd.connectionInfo(
                sg + ".surfaceShader", sourceFromDestination = 1))

        material = material.split('.')[0]

        return material


class ApplyMayaColorsError(ValueError):
    """Error occurred during mod_applyMayaColors"""


# TM and (c) 2011 DreamWorks Animation LLC.  All Rights Reserved.
# Reproduction in whole or in part without prior written permission of a
# duly authorized representative is prohibited.
