import maya.api.OpenMaya as om

import icarus_dcc.maya.dag_node as dag_node


class MeshHandle(dag_node.DagNodeHandle):
    """Provide API 2.0 access to a Maya mesh shape.

    Validate that the resolved node is a mesh shape and expose its
    MFnMesh function set.

    Parameters
    ----------
    node_name : str
        Name of the Maya mesh shape to resolve, not its transform.

    Raises
    ------
    ValueError
        If node_name is empty, the node cannot be resolved, or the
        resolved node is not a mesh shape.

    Examples
    --------
    >>> mesh = MeshHandle("pCubeShape1")
    >>> mesh.mesh_fn.name()
    'pCubeShape1'
    """

    def __init__(self, node_name: str) -> None:
        super().__init__(node_name=node_name)

        if not self.m_object.hasFn(om.MFn.kMesh):
            raise ValueError(
                f'Node "{node_name}" is not a mesh shape'
            )

        self._mesh_fn = om.MFnMesh(self.dag_path)

    def _resolve_mesh_shape(self, path: om.MDagPath) -> None:
        """Reserve mesh shape resolution for a future implementation.

        Parameters
        ----------
        path : om.MDagPath
            DAG path intended for mesh shape resolution.

        Notes
        -----
        This method is a placeholder. It currently returns None without
        inspecting the path or updating the handle.
        """

    @property
    def mesh_fn(self) -> om.MFnMesh:
        """om.MFnMesh : Function set for the mesh shape."""
        return self._mesh_fn
