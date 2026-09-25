name = "icarus_dcc_maya"
version = "0.1.0"

requires = [
    "maya-2024",
    "icarus_dcc-0.1.0",
]

def commands():
    env.MAYA_MODULE_PATH.prepend("{root}/modules".format(root=this.root))