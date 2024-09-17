from PIL import Image
from sklearn.cluster import KMeans
import os
from os import listdir
from os.path import isfile, join
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from utils import makedirs


def main(DIRECTORY, args):
    IMG_PATH = DIRECTORY['IMG_PATH']
    OUTPUT_PATH = DIRECTORY['OUTPUT_PATH']
    OUTPUT_PLOT_PATH = os.path.join(OUTPUT_PATH, 'segmentation')  # path for output (plot directory)

    IS_PLOT = args.plot_show
    IS_SAVE = args.plot_save

    target_img_path = IMG_PATH
    try:
        # --------------Lord image file--------------
        img = Image.open(target_img_path)
        img = np.array(img)  # transfer to np.array

        # --------------Clustering--------------
        pixels = img.reshape(-1, 1)  # 由于是灰度图像，所以reshape(-1, 1)
        kmeans = KMeans(n_clusters=args.n_clusters, max_iter=args.max_iter, n_init=args.n_init, random_state=0).fit(
            pixels)
        labels = kmeans.labels_
        result = labels.reshape(img.shape[0], img.shape[1])

        # -------------------Plot and save result------------------------
        if IS_PLOT:
            fig = plt.figure(figsize=(12, 8), dpi=100)

            ax1 = fig.add_subplot(1, 2, 1)
            ax1.imshow(img, cmap='gray')
            ax1.set_title('image')

            ax2 = fig.add_subplot(1, 2, 2)
            ax2.imshow(result)
            ax2.set_title('segmentation')
            plt.axis('off')
            # plt.show(block=False)
            plt.close()

            # print(11111111111)

        if IS_SAVE:
            # print(22222)
            makedirs(OUTPUT_PLOT_PATH)
            seg_result_path = os.path.join(OUTPUT_PLOT_PATH, "%s.png" % (os.path.basename(IMG_PATH)[:-4]))
            plt.imshow(result)
            plt.axis('off')
            plt.savefig(seg_result_path, bbox_inches='tight', dpi=300)
            plt.close()

    except IOError:
        print("Error")

    return seg_result_path

# if __name__ == '__main__':
#     main()


## 设置K值（聚类数）
# K = 2
#
#
# # 加载图片
# def load_image(file_path):
#     img = Image.open(file_path)
#     return img
#
#
# # 将图片转换为数组
# def image_to_array(img):
#     return np.array(img)
#
#
# # 将数组转换为图片
# def array_to_image(arr):
#     return Image.fromarray(np.uint8(arr))
#
# # 图片可视化
# def visualize_segmentation(segmented_img):
#     plt.figure(figsize=(10, 6))
#     plt.imshow(segmented_img, cmap='viridis')
#     plt.axis('off')
#     plt.show()
#
#
# # 主函数
# # 修改image_segmentation函数，返回聚类标签
# def image_segmentation(img, k):
#     if len(img.shape)==2:  # 灰度图像
#         pixels = img.reshape(-1, 1)
#     elif len(img.shape)==3:
#         pixels = img.reshape(-1, 3)
#         # print(len(img.shape))
#     print(pixels.shape)
#     kmeans = KMeans(n_init=4, n_clusters=k, random_state=0).fit(pixels)
#     labels = kmeans.labels_
#     print(labels.shape)
#     segmented_img = labels.reshape(img.shape[0], img.shape[1])
#     print(segmented_img.shape)
#     return segmented_img  # 只返回聚类标签
#
# def calculate_purity(segmented_img):
#     """计算分割图像的纯度"""
#     cluster_labels = np.unique(segmented_img)
#     num_pixels = segmented_img.shape[0] * segmented_img.shape[1]
#     purity = []
#
#     for label in cluster_labels:
#         mask = segmented_img == label
#         class_counts = np.bincount(mask.ravel())
#         max_class = np.argmax(class_counts)
#         class_purity = class_counts[max_class] / np.sum(class_counts)
#         purity.append(class_purity)
#     return purity
#
#
#
# def calculate_dbi(segmented_img):
#     """计算分割图像的DBI"""
#     cluster_labels = np.unique(segmented_img)
#     num_clusters = len(cluster_labels)
#     centroids = np.zeros((num_clusters, segmented_img.shape[-1]))
#
#     for i, label in enumerate(cluster_labels):
#         mask = segmented_img == label
#         cluster = segmented_img[mask]
#         centroid = np.mean(cluster, axis=0)
#         centroids[i] = centroid
#
#
#     dbi = 0
#
#     for i, centroid_i in enumerate(centroids):
#         max_Rij = -np.inf
#         for j, centroid_j in enumerate(centroids):
#             if i != j:
#                 Rij = (np.sum((centroid_i - centroid_j) ** 2) /
#                        np.sum((segmented_img == i).astype(int)) +
#                        np.sum((centroid_i - centroid_j) ** 2) /
#                        np.sum((segmented_img == j).astype(int)))
#                 if Rij > max_Rij:
#                     max_Rij = Rij
#         dbi += max_Rij
#
#     dbi /= num_clusters
#
#     return dbi
#
#
# if __name__ == '__main__':
#     # 初始化计数器
#     i = 0
#     directory = 'img/'
#
#     # 遍历图片目录下的所有文件
#     for filename in os.listdir(directory):
#         # 检查文件是否以 '.png' 结尾
#         if filename.endswith('.png'):
#             # 更新计数器
#             i += 1
#
#             # 构造文件路径
#             file_path = os.path.join(directory, filename)
#
#             # 加载图片
#             img = load_image(file_path)
#             print(img.size)
#             # 将图片转换为数组
#             arr = image_to_array(img)
#             print(arr.shape)
#
#             # 图片分割
#             segmented_img = image_segmentation(arr, K)
#             # print(segmented_img.shape)
#
#             # 图片可视化
#             visualize_segmentation(segmented_img.astype(float))  # 在可视化前将数据类型转换成浮点型
#
#             # 计算纯度
#             purity = calculate_purity(segmented_img)
#             for j, p in enumerate(purity):
#                 print(f"Image-{i} Purity-{j}: {p}")
#
#             # 计算DBI
#             dbi = calculate_dbi(segmented_img)
#
#             print(f"Image-{i} DBI: {dbi}")

# if __name__ == '__main__':
