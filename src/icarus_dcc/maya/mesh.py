import maya.api.OpenMaya as om

import icarus_dcc.maya.dag_node as dag_node


class MeshHandle(dag_node.DagNodeHandle):
    """Provide API 2.0 access to a Maya mesh shape.

    Resolve a mesh shape or its transform and expose the shape's
    MFnMesh function set. All inherited handles refer to the shape.

    Parameters
    ----------
    node_name : str
        Name of a mesh shape or a transform with exactly one direct,
        non-intermediate mesh child.

    Raises
    ------
    ValueError
        If node_name is empty, the node cannot be resolved, or the
        resolved node is neither a mesh nor a transform with exactly
        one direct, non-intermediate mesh child.

    Notes
    -----
    An explicitly named intermediate mesh shape is accepted.

    Examples
    --------
    >>> mesh = MeshHandle("pCubeShape1")
    >>> mesh.mesh_fn.name()
    'pCubeShape1'
    """

    def __init__(self, node_name: str) -> None:
        super().__init__(node_name=node_name)

        mesh_path = self._resolve_mesh_shape(self.dag_path)
        self._bind_to_path(mesh_path)
        self._mesh_fn = om.MFnMesh(self.dag_path)

    def _resolve_mesh_shape(self, path: om.MDagPath) -> om.MDagPath:
        """Resolve a mesh shape from a DAG path.

        Parameters
        ----------
        path : om.MDagPath
            Path to a mesh shape or its transform.

        Returns
        -------
        om.MDagPath
            Copy of the mesh path, or a path extended to the transform's
            single non-intermediate mesh child.

        Raises
        ------
        ValueError
            If the node is neither a mesh nor a transform, or the
            transform has zero or multiple eligible mesh children.

        Notes
        -----
        Only direct children are inspected. Explicit mesh paths are
        accepted even if intermediate. The supplied path is unchanged.
        """
        mesh_path = om.MDagPath(path)
        node = mesh_path.node()

        if node.hasFn(om.MFn.kMesh):
            return mesh_path

        if not node.hasFn(om.MFn.kTransform):
            raise ValueError(
                f'Node "{path.fullPathName()}" is not a mesh or transform.'
            )

        transform_fn = om.MFnDagNode(mesh_path)
        mesh_children = []

        for index in range(transform_fn.childCount()):
            child = transform_fn.child(index)

            if not child.hasFn(om.MFn.kMesh):
                continue

            if om.MFnDagNode(child).isIntermediateObject:
                continue

            mesh_children.append(child)

        if len(mesh_children) != 1:
            raise ValueError(
                f'Transform "{path.fullPathName()}" must have exactly '
                'one direct, non-intermediate mesh child; '
                f'found {len(mesh_children)}.'
            )

        mesh_path.push(mesh_children[0])
        return mesh_path

    @property
    def mesh_fn(self) -> om.MFnMesh:
        """om.MFnMesh : Function set for the mesh shape."""
        return self._mesh_fn
