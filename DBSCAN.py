# 使用SLIC（Simple Linear Iterative Clustering）超像素分割和DBSCAN（Density-Based Spatial Clustering of Applications with Noise）聚类算法
import os
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from utils import makedirs
import cv2
import hdbscan
import numpy as np
import cv2
from skimage.segmentation import slic
from sklearn.cluster import DBSCAN


def main(DIRECTORY, args):
    IMG_PATH = DIRECTORY['IMG_PATH']
    OUTPUT_PATH = DIRECTORY['OUTPUT_PATH']
    OUTPUT_PLOT_PATH = os.path.join(OUTPUT_PATH, 'segmentation')  # path for output (plot directory)

    IS_PLOT = args.plot_show
    IS_SAVE = args.plot_save

    # files = [f for f in listdir(IMG_PATH) if isfile(join(IMG_PATH, f))]  # read all files in IMG_PATH

    # for file in files:
    #     # print(111111)
    #     target_img_path = "img/" + file
    #     try:
    #         # --------------Lord image file--------------
    #         # img = cv2.imread(target_img_path)
    #         # height, width, channels = img.shape
    #         # data = img.reshape((height * width, channels))
    #
    #         img = cv2.imread(target_img_path)
    #
    #         # 使用SLIC超像素分割
    #         segments = slic(img, n_segments=500, compactness=0.01)  # slic_segments=500
    #
    #         # 将超像素均值作为特征向量
    #         features = []
    #         for segment_id in np.unique(segments):
    #             mask = (segments == segment_id)
    #             mean_color = np.mean(img[mask], axis=0)
    #             features.append(mean_color)
    #
    #         features = np.array(features)
    #
    #         # print(22222)
    #         # --------------Clustering--------------
    #         # # 使用HDBSCAN进行聚类
    #         # hdb = hdbscan.HDBSCAN(min_cluster_size=20, gen_min_span_tree=True, approx_min_span_tree=True)
    #         # labels = hdb.fit_predict(data)
    #         # result = labels.reshape((height, width)).astype(np.uint8)
    #
    #         # 使用DBSCAN进行聚类
    #         dbscan = DBSCAN(eps=4, min_samples=3)  # dbscan_eps=4  dbscan_min_samples=3
    #         labels = dbscan.fit_predict(features)
    #
    #         # 创建分割后的图像
    #         result = np.zeros_like(img)
    #         for segment_id, label in zip(np.unique(segments), labels):
    #             mask = (segments == segment_id)
    #             result[mask] = np.mean(features[labels == label], axis=0)
    #
    #         # print(333333)
    #         # -------------------Plot and save result------------------------
    #         if IS_PLOT:
    #             fig = plt.figure(figsize=(12, 8), dpi=100)
    #
    #             ax1 = fig.add_subplot(1, 2, 1)
    #             ax1.imshow(img, cmap='gray')
    #             ax1.set_title('image')
    #
    #             ax2 = fig.add_subplot(1, 2, 2)
    #             ax2.imshow(result)
    #             ax2.set_title('segmentation')
    #
    #             plt.show(block=False)
    #             plt.close()
    #
    #         if IS_SAVE:
    #             makedirs(OUTPUT_PLOT_PATH)
    #             seg_result_path = os.path.join(OUTPUT_PLOT_PATH, "%s.png" % (os.path.splitext(file)[0]))
    #             plt.imshow(result)
    #             plt.savefig(seg_result_path, dpi=300)
    #             plt.close()
    #
    #
    #     except IOError:
    #         print("Error")

    target_img_path = IMG_PATH
    try:
        # --------------Lord image file--------------
        # img = cv2.imread(target_img_path)
        # height, width, channels = img.shape
        # data = img.reshape((height * width, channels))

        print("====== DBSCAN =====")
        print(target_img_path)
        # img = cv2.imread(os.path.join('algorithm/ori_8bit', IMG_PATH[-5:]))
        # pre_access_path = os.path.dirname(os.path.abspath(target_img_path))  # 获取预访问的路径
        # current_dir = os.getcwd()  # 获取当前工作目录
        # relative_path = os.path.relpath(pre_access_path, current_dir)  # 计算相对路径
        # img = cv2.imread(relative_path.replace('\\', '/'))
        #
        # print("预访问的路径：", pre_access_path)
        # print("当前工作目录：", current_dir)
        # print("相对路径：", relative_path)

        img = cv2.imdecode(np.fromfile(target_img_path, dtype=np.uint8), 1)
        # print(img)
        # print(img.shape)

        # 使用SLIC超像素分割
        segments = slic(img, n_segments=args.n_segments, compactness=args.compactness)  # slic_segments=500

        # 将超像素均值作为特征向量
        features = []
        for segment_id in np.unique(segments):
            mask = (segments == segment_id)
            mean_color = np.mean(img[mask], axis=0)
            features.append(mean_color)

        features = np.array(features)

        # print(22222)
        # --------------Clustering--------------
        # # 使用HDBSCAN进行聚类
        # hdb = hdbscan.HDBSCAN(min_cluster_size=20, gen_min_span_tree=True, approx_min_span_tree=True)
        # labels = hdb.fit_predict(data)
        # result = labels.reshape((height, width)).astype(np.uint8)

        # 使用DBSCAN进行聚类
        dbscan = DBSCAN(eps=args.eps, min_samples=args.min_samples)  # dbscan_eps=4  dbscan_min_samples=3
        labels = dbscan.fit_predict(features)

        # 创建分割后的图像
        result = np.zeros_like(img)
        for segment_id, label in zip(np.unique(segments), labels):
            mask = (segments == segment_id)
            result[mask] = np.mean(features[labels == label], axis=0)

        # print(333333)
        # -------------------Plot and save result------------------------
        if IS_PLOT:
            # fig = plt.figure(figsize=(12, 8), dpi=100)
            fig = plt.figure(dpi=300)

            ax1 = fig.add_subplot(1, 2, 1)
            ax1.imshow(img, cmap='gray')
            ax1.set_title('image')

            ax2 = fig.add_subplot(1, 2, 2)
            ax2.imshow(result)
            ax2.set_title('segmentation')

            plt.axis("off")
            # plt.show(block=False)
            plt.close()

        if IS_SAVE:
            makedirs(OUTPUT_PLOT_PATH)
            seg_result_path = os.path.join(OUTPUT_PLOT_PATH, "%s.png" % (os.path.basename(IMG_PATH)[:-4]))
            plt.axis('off')
            plt.imshow(result)
            plt.savefig(seg_result_path, bbox_inches='tight', dpi=300)
            plt.close()


    except IOError:
        print("Error")

    return seg_result_path

# if __name__ == '__main__':
#     main()
