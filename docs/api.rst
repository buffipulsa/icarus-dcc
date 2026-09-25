
Python API
==========

Maya Node Handles
-----------------

These wrappers require Maya at runtime. Documentation builds use placeholder
Maya imports and do not run scene operations or example code.

Dependency Node Handle
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: icarus_dcc.maya.dependency_node.DependencyNodeHandle
    :members:

DAG Node Handle
~~~~~~~~~~~~~~~

.. autoclass:: icarus_dcc.maya.dag_node.DagNodeHandle
    :members:
    :show-inheritance:

Mesh Handle
~~~~~~~~~~~

.. autoclass:: icarus_dcc.maya.mesh.MeshHandle
    :members:
    :show-inheritance:

Mesh handles also expose the inherited properties documented above.

Launcher Configuration
----------------------

.. automodule:: icarus_dcc.launcher.config
    :members:

Development Utilities
---------------------

.. automodule:: icarus_dcc.dev.reload
    :members:

Logging
-------

.. automodule:: icarus_dcc.logging_utils
    :members:
    :undoc-members:

Connection Records
------------------

These definitions are an initial scaffold for connection handling.

.. automodule:: icarus_dcc.maya.connections.records
    :members:
    :undoc-members:
