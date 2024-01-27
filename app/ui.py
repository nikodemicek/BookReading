def get_user_input():
    """
    Gets an image file path from the user.
    """
    print("Please enter the path to your image file:")
    image_path = r"C:\Users\NikodemOlsavsky\OneDrive - Valcon Business Development A S\Projects\BookReading\IMG_0931.JPG" #input()
    return image_path

def display_results(results):
    """
    Displays the results in a simple text format.
    :param results: The data to be displayed, assumed to be a list or similar iterable.
    """
    print("\nDetected Results:")
    for item in results:
        print(item)
