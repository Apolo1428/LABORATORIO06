import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen y convertirla a escala de grises
img = cv2.imread("imagen.jpg", 0)

# Aplicar la Transformada de Fourier
dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

# Calcular el módulo de la Transformada de Fourier
magnitude_spectrum = 20 * \
    np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
magnitude_spectrum = magnitude_spectrum
cv2.imshow("Espectro de imagen",magnitude_spectrum)
cv2.imwrite("espectro_imagen.pjg",magnitude_spectrum)


# Normalizar el espectro y mostrarlo
plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()


# def smooth_kernel(size):
#   # Creamos una matriz de ceros con el tamaño especificado
#   kernel = np.zeros((size, size))
  
#   # Calculamos el centro de la matriz
#   center = size // 2
  
#   # Recorremos la matriz y asignamos valores de suavizado a cada elemento
#   for i in range(size):
#     for j in range(size):
#       kernel[i][j] = 1.0 / (1 + (i - center) ** 2 + (j - center) ** 2)
      
#   # Devolvemos el kernel
#   return kernel
# print(smooth_kernel(4))
input(1)