import cv2
import numpy as np

def lowpass_gaussian_filter(image, sigma=10):
    # Aplica la transformada de Fourier a la imagen
    fourier = np.fft.fft2(image)

    # Traslada el espectro de Fourier a la parte central de la imagen
    fourier_shifted = np.fft.fftshift(fourier)

    # Obtiene las dimensiones de la imagen
    rows = image.shape[0]
    cols = image.shape[1]
    # Crea un kernel Gaussiano con el tamaño de la imagen
    kernel = np.zeros((rows, cols))

    # Calcula el centro del kernel
    center_x, center_y = rows // 2, cols // 2

    # Rellena el kernel con valores Gaussianos
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            kernel[i, j] = np.exp(-d**2 / (2 * sigma**2))

    # Aplica el filtro pasa-bajos al espectro de Fourier
    filtered_fourier = fourier_shifted * kernel

    # Deshace la traslación del espectro de Fourier
    fourier = np.fft.ifftshift(filtered_fourier)

    # Aplica la transformada inversa de Fourier a la imagen filtrada
    filtered_image = np.fft.ifft2(fourier)
    # Convierte el resultado a una imagen de tipo entero
    filtered_image = np.abs(filtered_image).astype(np.uint8)

    return filtered_image


def highpass_gaussian_filter(image, sigma=3):
    # Aplica la transformada de Fourier a la imagen
    fourier = np.fft.fft2(image)

    # Traslada el espectro de Fourier a la parte central de la imagen
    fourier_shifted = np.fft.fftshift(fourier)

    # Obtiene las dimensiones de la imagen
    rows = image.shape[0]
    cols = image.shape[1]

    # Crea un kernel Gaussiano con el tamaño de la imagen
    kernel = np.zeros((rows, cols))

    # Calcula el centro del kernel
    center_x, center_y = rows // 2, cols // 2

    # Rellena el kernel con valores Gaussianos
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            kernel[i, j] = np.exp(-d**2 / (2 * sigma**2))

    # Aplica el filtro pasa-altos al espectro de Fourier
    filtered_fourier = fourier_shifted * (1 - kernel)

    # Deshace la traslación del espectro de Fourier
    fourier = np.fft.ifftshift(filtered_fourier)

    # Aplica la transformada inversa de Fourier a la imagen filtrada
    filtered_image = np.fft.ifft2(fourier)

    # Convierte el resultado a una imagen de tipo entero
    filtered_image = np.abs(filtered_image).astype(np.uint8)

    return filtered_image


def laplacian_filter(image):
    # Obtiene las dimensiones de la imagen
    rows = image.shape[0]
    cols = image.shape[1]

    # Padeo de imagen
    image_padded = np.pad(image, ((0, rows), (0, cols)),
                          'constant', constant_values=((0, 0), (0, 0)))

    # Guardamos el tamaño de la imagen padeada
    row_padded, cols_padded = np.ogrid[0:2*rows, 0:2*cols]

    # Aplica la transformada de Fourier a la imagen con paddeo
    fourier = np.fft.fft2(image_padded)

    # Traslada el espectro de Fourier a la parte central de la imagen
    fourier_shifted = np.fft.fftshift(fourier)

    # Crea un kernel Laplaciano con el tamaño de la imagen con paddeo
    kernel = -((row_padded-rows)**2 + (cols_padded-cols)**2)
    # Aplica el filtro Laplaciano al espectro de Fourier
    filtered_fourier = fourier_shifted * kernel

    # Deshace la traslación del espectro de Fourier
    fourier = np.fft.ifftshift(filtered_fourier)

    # Aplica la transformada inversa de Fourier a la imagen filtrada
    filtered_image = np.fft.ifft2(fourier)

    # Convierte el resultado a una imagen de tipo entero
    filtered_image = np.real(filtered_image)

    # Recorta la imagen filtrada eliminando el paddeo
    filtered_image = filtered_image[:rows, :cols]

    return filtered_image


def highboost_filter(image, sigma=2, k=1):
    # Aplica la transformada de Fourier a la imagen
    fourier = np.fft.fft2(image)

    # Traslada el espectro de Fourier a la parte central de la imagen
    fourier_shifted = np.fft.fftshift(fourier)

    # Obtiene las dimensiones de la imagen
    rows = image.shape[0]
    cols = image.shape[1]

    # Crea un kernel Laplaciano con el tamaño de la imagen
    kernel = np.zeros((rows, cols))

    # Calcula el centro del kernel
    center_x, center_y = rows // 2, cols // 2

    # Rellena el kernel con valores Laplacianos
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            kernel[i, j] = (d**2 - sigma**2) * np.exp(-d**2 / (2 * sigma**2))

    # Aplica el filtro HighBoost al espectro de Fourier
    filtered_fourier = fourier_shifted + k * kernel

    # Deshace la traslación del espectro de Fourier
    fourier = np.fft.ifftshift(filtered_fourier)

    # Aplica la transformada inversa de Fourier a la imagen filtrada
    filtered_image = np.fft.ifft2(fourier)

    # Convierte el resultado a una imagen de tipo entero
    filtered_image = np.abs(filtered_image).astype(np.uint8)

    return filtered_image


def enfatizado(image, sigma=0.3, a=0.9, b=0.5):

    # sigma= frecuencia de corte

    # Aplica la transformada de Fourier a la imagen
    fourier = np.fft.fft2(image)

    # Traslada el espectro de Fourier a la parte central de la imagen
    fourier_shifted = np.fft.fftshift(fourier)

    # Obtiene las dimensiones de la imagen
    rows = image.shape[0]
    cols = image.shape[1]

    # Crea un kernel Gaussiano con el tamaño de la imagen
    kernel = np.zeros((rows, cols))

    # Calcula el centro del kernel
    center_x, center_y = rows // 2, cols // 2

    # Rellena el kernel con valores Gaussianos
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            kernel[i, j] = np.exp(-d**2 / (2 * sigma**2))

    # Aplica el filtro pasa-altos al espectro de Fourier
    filtered_fourier = fourier_shifted * (b+a * (1 - kernel))

    # Deshace la traslación del espectro de Fourier
    fourier = np.fft.ifftshift(filtered_fourier)

    # Aplica la transformada inversa de Fourier a la imagen filtrada
    filtered_image = np.fft.ifft2(fourier)

    # Convierte el resultado a una imagen de tipo entero
    filtered_image = np.abs(filtered_image).astype(np.uint8)

    return filtered_image


def homomorphic_filter(image, gamma=0.1, alpha=0.5, beta=0.7):
    # Aplica la transformada de Fourier a la imagen
    fourier = np.fft.fft2(image)

    # Traslada el espectro de Fourier a la parte central de la imagen
    fourier_shifted = np.fft.fftshift(fourier)

    # Obtiene las dimensiones de la imagen
    rows = image.shape[0]
    cols = image.shape[1]

    # Crea un kernel homomórfico con el tamaño de la imagen
    kernel = np.zeros((rows, cols))

    # Calcula el centro del kernel
    center_x, center_y = rows // 2, cols // 2

    # Rellena el kernel con valores homomórficos
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            kernel[i, j] = (1 + alpha*d**2)**(-gamma)

    # Aplica el filtro homomórfico al espectro de Fourier
    filtered_fourier = fourier_shifted * kernel

    # Deshace la traslación del espectro de Fourier
    fourier = np.fft.ifftshift(filtered_fourier)

    # Aplica la transformada inversa de Fourier a la imagen filtrada
    filtered_image = np.fft.ifft2(fourier)

    # Convierte el resultado a una imagen de tipo entero y aplica un factor de multiplicación
    filtered_image = (beta * np.abs(filtered_image)).astype(np.uint8)

    return filtered_image
dict_filtros = {0:lowpass_gaussian_filter,1:highpass_gaussian_filter,2:laplacian_filter,3:highboost_filter,4:enfatizado,5:homomorphic_filter}
