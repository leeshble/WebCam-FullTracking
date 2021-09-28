import pose_module as pm


def main(cam):
    # Change parameter to change input(Camera or videos)
    pm.camera_input(int(cam))


main(input("Please type your camera id."))
