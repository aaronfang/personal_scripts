"""
This is a hacky way to select faces inside a loop.
"""
import maya.cmds as cmds
import maya.mel as mm


class _cmds(object):
    def __init__(self):
        pass

    def is_component(self, sel_list):
        is_comp = []
        for sel in sel_list:
            if ".vtx[" in sel:
                if "vtx" not in is_comp:
                    is_comp.append("vtx")
                is_comp.append(sel)
            elif ".e[" in sel:
                if "edge" not in is_comp:
                    is_comp.append("edge")
                is_comp.append(sel)
            elif ".f[" in sel:
                if "face" not in is_comp:
                    is_comp.append("face")
                is_comp.append(sel)
            elif ".map[" in sel:
                if "uv" not in is_comp:
                    is_comp.append("uv")
                is_comp.append(sel)
        if len(is_comp[1:]) == len(sel_list):
            return is_comp[0]


def select_inside_loop():
    # get selected face loop and one inner face, convert to edges
    get_sel = cmds.ls(os=1, fl=1)
    if _cmds().is_component(get_sel) == "face":
        mesh = cmds.ls(sl=1, fl=1, o=1)
        edge_from_face = cmds.ls(cmds.polyListComponentConversion(get_sel[:-1], te=1, bo=1), fl=1)

        # create temp uvset for uv projection
        current_uvset = cmds.polyUVSet(mesh, q=1, cuv=1)[0]
        for uvset in cmds.polyUVSet(mesh, q=1, auv=1):
            if uvset == "af_tmp_select_uvset":
                cmds.polyUVSet(mesh, delete=1, uvSet="af_tmp_select_uvset")
                cmds.polyUVSet(mesh, create=1, uvSet="af_tmp_select_uvset")
                cmds.polyUVSet(mesh, e=1, cuv=1, uvSet="af_tmp_select_uvset")
            else:
                cmds.polyUVSet(mesh, create=1, uvSet="af_tmp_select_uvset")
                cmds.polyUVSet(mesh, e=1, cuv=1, uvSet="af_tmp_select_uvset")

        cmds.polyProjection(mesh, ch=0, type="Planar", ibd=1, md="y")
        cmds.polyMapCut(edge_from_face, e=0)

        # get inner selection
        cmds.select(cmds.polyListComponentConversion(get_sel[-1], tuv=1), r=1)
        mm.eval("polySelectBorderShell 0;ConvertSelectionToFaces;")
        inner = cmds.ls(sl=1, fl=1)

        # cleanup
        cmds.polyUVSet(mesh, e=1, cuv=1, uvSet=current_uvset)
        cmds.polyUVSet(mesh, delete=1, uvSet="af_tmp_select_uvset")
        cmds.delete(mesh, ch=1)

        # select fill
        cmds.select((inner + get_sel[:-1]), r=1)


select_inside_loop()
