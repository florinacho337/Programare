from PIL import Image, ImageFilter
import os
import matplotlib.pyplot as plt


def resize_image(image_path, size):
    """
    resize_image(image_path, size) resizes the image in image_path to the size specified in size
    :param image_path: string
    :param size: tuple
    :return: image
    """
    img = Image.open(image_path)
    img = img.resize(size)
    return img


def resize_images(image_folder, size):
    """
    resize_images(image_folder, size) resizes the images in image_folder to the size specified in size
    :param image_folder: string
    :param size: tuple
    :return: list of images
    """
    images = []
    for image in os.listdir(image_folder):
        img = resize_image(os.path.join(image_folder, image), size)
        images.append(img)
    return images


def visualize_images(images):
    """
    visualize_images(images) visualizes the images in a 3x4 grid
    :param images: list of images
    :return: void
    """
    fig, axes = plt.subplots(3, 4, figsize=(20, 20))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i])
        ax.axis('off')
    plt.show()


def grayscale_images(image_folder):
    """
    grayscale_images(image_folder) transforms the images in image_folder to grayscale
    :param image_folder: string
    :return: list of images
    """
    images = []
    for image in os.listdir(image_folder):
        img = Image.open(os.path.join(image_folder, image)).convert('L')
        images.append(img)
    return images


def visualize_image(path):
    """
    visualize_image(path) visualizes the image in path
    :param path: string
    :return: void
    """
    image = Image.open(path)
    image.show()


def blur_image(image_path):
    """
    blur_image(image_path) blurs the image in image_path
    :param image_path: string
    :return: image
    """
    img = Image.open(image_path)
    img = img.filter(ImageFilter.BLUR)
    return img


def show_before_after(original_image, transformed_image):
    """
    show_before_after(original_image, transformed_image) shows the original_image and the transformed_image in a table
    :param original_image: image
    :param transformed_image: image
    :return: void
    """
    fig, axes = plt.subplots(1, 2, figsize=(20, 20))
    axes[0].imshow(original_image)
    axes[0].axis('off')
    axes[0].set_title('Original image')
    axes[1].imshow(transformed_image)
    axes[1].axis('off')
    axes[1].set_title('Transformed image')
    plt.show()


def determine_edges(image_path):
    """
    determine_edges(image_path) determines the edges of the image in image_path
    :param image_path: string
    :return: image
    """
    img = Image.open(image_path)
    img = img.filter(ImageFilter.FIND_EDGES)
    return img


def ex2():
    # 1. Visualize an image from the data/images folder
    # Visualize the image data/images/chatGPT.png
    visualize_image('data/images/chatGPT.png')

    # Visualize the image data/images/Altman.webp
    visualize_image('data/images/Altman.webp')

    # 2. If the images from data/images/ are not 128x128, resize them, then visualize them in a table
    visualize_images(resize_images('data/images', (128, 128)))

    # 3. Transform the images from data/images/ to grayscale, then visualize them in a table
    visualize_images(grayscale_images('data/images'))

    # 4. Blur an image from data/images/ then show in format before-after
    # Blur the image data/images/YOLO.jpg
    image = Image.open('data/images/YOLO.jpg')
    blurred_image = blur_image('data/images/YOLO.jpg')
    # Show the images
    show_before_after(image, blurred_image)

    # 5. Determine the edges of an image from data/images/ then show in format before-after
    # Determine the edges of the image data/images/diffusionModel.jpg
    image = Image.open('data/images/diffusionModel.jpg')
    edges_image = determine_edges('data/images/diffusionModel.jpg')
    # Show the images
    show_before_after(image, edges_image)
