import argparse
import os
import DBSCAN
import EnFCM
import FCM
import KMeans
import MFCM
from utils import makedirs

WORKSPACE = os.path.split(os.getcwd())[-1]  # current workspace
# IMG_PATH = os.path.join(os.getcwd(), "img")  # path for input image directory
OUTPUT_PATH = os.path.join(os.getcwd(), "output")  # path for output directory


# OUTPUT_PLOT_PATH = os.path.join(OUTPUT_PATH, 'segmentation')  # path for output (plot directory)
# OUTPUT_FILT_IMG_PATH = os.path.join(OUTPUT_PATH, 'filtered_img')

def get_needed_args(selected_algorithm, *ooo):
    others = ooo[0][0]
    print(others, type(others))
    # for i in ooo:
    #     others.append(i)

    # 创建一个 ArgumentParser 对象，用于解析命令行参数
    parser = argparse.ArgumentParser(
        description="Clustering Algorithm on Cell Segmentation.")
    # -----------------共同的参数-----------------
    # 选择哪种聚类算法，默认为 selected_algorithm (通过选择按钮选择算法，可以保证selected_algorithm∈choices)
    parser.add_argument('-a', '--algorithm', default=selected_algorithm,
                        choices=['DBSCAN', 'KMeans', 'FCM', 'EnFCM', 'MFCM'],
                        type=str, help="Choose a clustering algorithm. (DBSCAN, KMeans, FCM, EnFCM, MFCM)")
    # 输入图像的位数，默认为 8
    parser.add_argument('--num_bit', default=8, type=int, help="number of bits of input images")
    # 是否显示聚类结果的可视化图像，默认为 1
    parser.add_argument('--plot_show', default=1, choices=[0, 1], help="Show plot about result")
    # 添加一个 argument，表示是否保存聚类结果的可视化图像，默认为 1
    parser.add_argument('--plot_save', default=1, choices=[0, 1], help="Save plot about result")

    if selected_algorithm == 'DBSCAN':
        parser.add_argument('--n_segments', default=int(others[0]), type=int, help="Number of Superpixels")
        parser.add_argument('--compactness', default=float(others[2]), type=float, help="Compactness of superpixels")
        parser.add_argument('--max_SLIC_iter', default=int(others[1]), type=int, help="Max number of SLIC iterations")
        parser.add_argument('--eps', default=int(others[3]), type=int, help="Neighborhood radius")
        parser.add_argument('--min_samples', default=int(others[4]), type=int, help="Minimum cluster size")
    else:  # KMeans | FCM、EnFCM、MFCM
        parser.add_argument('--n_clusters', default=int(others[0]), type=int, help="Number of clusters")
        parser.add_argument('--max_iter', default=int(others[1]), type=int, help="Max number of clustering iterations")

        if selected_algorithm == 'KMeans':
            parser.add_argument('--n_init', default=int(others[2]), type=int, help="Minimum cluster size")
        else:  # FCM、EnFCM、MFCM
            parser.add_argument('--fuzziness', default=int(others[2]), type=int, help="Fuzziness parameter")
            parser.add_argument('--epsilon', default=float(others[3]), type=float, help="Convergence threshold")

            if selected_algorithm == 'EnFCM' or selected_algorithm == 'MFCM':
                parser.add_argument('--neighbour_effect', default=int(others[4]), type=int, help="Neighbour effect")
                parser.add_argument('--kernel_size', default=int(others[5]), type=int, help="Kernel size")

    args = parser.parse_args()
    return args


def M(IMG_PATH, selected_algorithm, *others):
    args = get_needed_args(selected_algorithm, others)
    print(args, type(args))
    algorithm = args.algorithm
    # algorithm = selected_algorithm

    # Subfolders are automatically created with the algorithm name.
    OUTPUT_PATH1 = os.path.join(OUTPUT_PATH, "%s" % (algorithm))
    makedirs(OUTPUT_PATH1)

    DIRECTORY = {}
    DIRECTORY['WORKSPACE'] = WORKSPACE
    DIRECTORY['IMG_PATH'] = IMG_PATH
    DIRECTORY['OUTPUT_PATH'] = OUTPUT_PATH1
    DIRECTORY['OUTPUT_PLOT_PATH'] = os.path.join(OUTPUT_PATH1, 'segmentation')
    DIRECTORY['OUTPUT_FILE_IMG_PATH'] = os.path.join(OUTPUT_PATH1, 'filtered_img')
    # print(IMG_PATH)
    print('------------')

    plt_img_path = ''
    if algorithm == 'FCM':
        plt_img_path = FCM.main(DIRECTORY, args)
    elif algorithm == 'EnFCM':
        plt_img_path = EnFCM.main(DIRECTORY, args)
    elif algorithm == 'MFCM':
        plt_img_path = MFCM.main(DIRECTORY, args)
    elif algorithm == 'KMeans':
        plt_img_path = KMeans.main(DIRECTORY, args)
    elif algorithm == 'DBSCAN':
        plt_img_path = DBSCAN.main(DIRECTORY, args)

    return plt_img_path

# if __name__ == '__main__':
#     # M('img/', 'FCM', 1, 2, 3, 4, 5)
#     M('8bit_data/1.png', 'DBSCAN', 1, 2, 3, 4, 5)
