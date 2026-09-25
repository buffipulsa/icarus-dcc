"""Run with mayapy -m unittest discover -s tests -p test_mesh_handle_maya.py."""

import unittest

try:
    import maya.standalone
    import maya.cmds as cmds
    import maya.api.OpenMaya as om
except ImportError:
    cmds = None


@unittest.skipIf(cmds is None, 'Requires Maya')
class MeshHandleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        maya.standalone.initialize(name='python')
        from icarus_dcc.maya.mesh import MeshHandle

        cls.handle_type = MeshHandle

    @classmethod
    def tearDownClass(cls):
        maya.standalone.uninitialize()

    def setUp(self):
        cmds.file(new=True, force=True)

    def test_shape_and_transform_bind_all_handles_to_shape(self):
        transform, _ = cmds.polyCube()
        shape = cmds.listRelatives(transform, shapes=True)[0]

        for name in (transform, shape):
            with self.subTest(name=name):
                handle = self.handle_type(name)
                self.assertEqual(handle.dependency_fn.name(), shape)
                self.assertEqual(handle.mesh_fn.name(), shape)
                self.assertEqual(handle.dag_fn.name(), shape)
                self.assertEqual(handle.dag_path.node(), handle.m_object)

    def test_intermediate_child_is_skipped_but_explicit_shape_is_valid(self):
        transform, _ = cmds.polyCube()
        shape = cmds.listRelatives(transform, shapes=True)[0]
        other_transform, _ = cmds.polyCube()
        other_shape = cmds.listRelatives(other_transform, shapes=True)[0]
        intermediate = cmds.parent(
            other_shape, transform, shape=True, relative=True
        )[0]
        intermediate = intermediate.rsplit('|', 1)[-1]
        cmds.setAttr(f'{intermediate}.intermediateObject', True)

        self.assertEqual(
            self.handle_type(transform).mesh_fn.name(), shape
        )
        self.assertEqual(
            self.handle_type(intermediate).mesh_fn.name(), intermediate
        )

    def test_rejects_missing_empty_and_non_mesh_nodes(self):
        camera_transform, camera_shape = cmds.camera()
        empty = cmds.createNode('transform')
        material = cmds.shadingNode('lambert', asShader=True)

        for name in ('', 'missingNode', empty, camera_transform,
                     camera_shape, material):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    self.handle_type(name)

    def test_rejects_multiple_mesh_children(self):
        transform, _ = cmds.polyCube()
        cmds.createNode('mesh', parent=transform)

        with self.assertRaisesRegex(ValueError, 'found 2'):
            self.handle_type(transform)

    def test_does_not_search_nested_transforms(self):
        parent = cmds.createNode('transform')
        transform, _ = cmds.polyCube()
        cmds.parent(transform, parent)

        with self.assertRaisesRegex(ValueError, 'found 0'):
            self.handle_type(parent)

    def test_resolver_copies_path_and_preserves_instance(self):
        transform, _ = cmds.polyCube()
        instance = cmds.instance(transform)[0]
        selection = om.MSelectionList()
        selection.add(instance)
        path = selection.getDagPath(0)
        original = path.fullPathName()
        handle = self.handle_type(transform)

        resolved = handle._resolve_mesh_shape(path)

        self.assertEqual(path.fullPathName(), original)
        self.assertEqual(
            resolved.fullPathName().rsplit('|', 1)[0], original
        )


if __name__ == '__main__':
    unittest.main()
