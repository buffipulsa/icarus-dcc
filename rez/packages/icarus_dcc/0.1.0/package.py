name = "icarus_dcc"
version = "0.1.0"

def commands():
    env.PYTHONPATH.prepend("{root}/python".format(root=this.root))

