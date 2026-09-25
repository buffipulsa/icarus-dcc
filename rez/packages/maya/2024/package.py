name = "maya"
version = "2024"

def commands():
    maya_location = getenv("ICARUS_MAYA_2024_LOCATION")

    env.MAYA_LOCATION = maya_location
    env.PATH.prepend("{}/bin".format(maya_location))