
import logging

import maya.api.OpenMaya as om

logger = logging.getLogger(__name__)


class DependencyNodeHandle:
    """Provide API 2.0 access to a Maya dependency node.
    
    Resolve a node name to an MObject and expose its MFnDependencyNode
    function set.

    Parameters
    ----------
    node_name : str
        Name of the Maya node to resolve.

    Raises
    ------
    ValueError
        If node_name is empty or the node cannot be resolved.
        
    Examples
    --------
    >>> node = DependencyNodeHandle("pCube1")
    >>> node.dependency_fn.name()
    'pCube1'
    """
    def __init__(self, node_name: str) -> None:
        
        if not node_name:
            raise ValueError('Please specify a node name.')
        
        logger.debug(
            'Creating DependencyNodeHandle for node "%s"',
            node_name
        )
        
        self._m_object = self._resolve_m_object(node_name)
        self._dependency_fn = om.MFnDependencyNode(self._m_object)
        
        logger.debug(
            'Resolved DependencyNodeHandle for node "%s"', 
            node_name
        )

    def _resolve_m_object(self, node_name: str) -> om.MObject:
        
        selection_list = om.MSelectionList()
        
        try:
            selection_list.add(node_name)
            
            return selection_list.getDependNode(0)
        
        except RuntimeError as error:
            raise ValueError(
                f'No valid node found for "{node_name}"'
            ) from error

    @property
    def m_object(self) -> om.MObject:
        """om.MObject : The resolved dependency node."""
        return self._m_object

    @property
    def dependency_fn(self) -> om.MFnDependencyNode:
        """om.MFnDependencyNode : Function set for the dependency node."""
        return self._dependency_fn