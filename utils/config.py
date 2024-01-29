ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    if not filename:  # Checks if the filename is not empty
        return False

    if '.' not in filename:  # Checks if there is a file extension
        return False

    extension = filename.rsplit('.', 1)[1].lower()  # Extracts the file extension
    return extension in ALLOWED_EXTENSIONS
