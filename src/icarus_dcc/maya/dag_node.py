import logging

import maya.api.OpenMaya as om

import icarus_dcc.maya.dependency_node as dependency_node

logger = logging.getLogger(__name__)


class DagNodeHandle(dependency_node.DependencyNodeHandle):
    """Provide API 2.0 access to a Maya DAG node.

    Validate that the resolved node belongs to the DAG and expose its
    MDagPath and MFnDagNode function set.

    Parameters
    ----------
    node_name : str
        Name of the Maya DAG node to resolve.

    Raises
    ------
    ValueError
        If node_name is empty, the node cannot be resolved, or the
        resolved node is not a DAG node.

    Examples
    --------
    >>> node = DagNodeHandle("pCube1")
    >>> node.dag_fn.fullPathName()
    '|pCube1'
    """
    def __init__(self, node_name: str) -> None:
        super().__init__(node_name=node_name)

        logger.debug(
            'Creating DagNodeHandle for node "%s"',
            node_name
        )

        if not self.m_object.hasFn(om.MFn.kDagNode):
            raise ValueError(
                f'Node "{node_name}" is not a DAG node.'
            )

        self._dag_path = om.MDagPath.getAPathTo(self.m_object)
        self._dag_fn = om.MFnDagNode(self._dag_path)

        logger.debug(
            'Resolved DagNodeHandle for node "%s"',
            node_name
        )

    def _bind_to_path(self, path: om.MDagPath) -> None:
        """Bind the handle's node and DAG state to a path.

        Parameters
        ----------
        path : om.MDagPath
            Valid DAG path identifying the node to represent.

        Notes
        -----
        Copies the supplied path and rebuilds the dependency-node and
        DAG-node function sets for its endpoint.

        Subclass-specific function sets are not updated by this method.
        """

        dag_path = om.MDagPath(path)
        m_object = dag_path.node()

        dependency_fn = om.MFnDependencyNode(m_object)
        dag_fn = om.MFnDagNode(dag_path)

        self._m_object = m_object
        self._dependency_fn = dependency_fn
        self._dag_path = dag_path
        self._dag_fn = dag_fn

    @property
    def dag_path(self) -> om.MDagPath:
        """om.MDagPath : The DAG path associated with the node."""
        return self._dag_path

    @property
    def dag_fn(self) -> om.MFnDagNode:
        """om.MFnDagNode : Function set for the DAG node."""
        return self._dag_fn
