import os
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.constants import INSERT
from all_algorithm import M


class ImageProcessingApp:
    def __init__(self, root):
        self.para = None
        self.file_path = None
        self.image_name = None
        self.right_image_label = None
        self.left_image_label = None
        self.line_canvas = None
        self.n_cluster_input = None
        self.n_cluster = None
        self.selected_algorithm = None
        self.Kmeans_max_iter_ = None
        self.Kmeans_n_init_ = None
        self.Kmeans_n_cluster_num = None
        self.root = root
        self.root.geometry("1300x1050")

        self.create_widgets()

    def create_widgets(self):
        """widgets"""
        # 设置界面顶部的空白区域
        top_space_label = ttk.Label(self.root)
        top_space_label.grid(row=0, column=1, padx=20, pady=10)

        # 上传图片按钮
        upload_button = ttk.Button(self.root, text="❶上传图片", command=self.upload_left_image, width=32)
        upload_button.grid(row=1, column=2, columnspan=2, sticky="w")

        # 算法选择下拉框
        algorithm_label = ttk.Label(self.root, text="❷算法选择:", width=10)
        algorithm_label.grid(row=2, column=2, pady=22, sticky="w")
        algorithm_combo = ttk.Combobox(self.root, values=["KMeans", "FCM", "MFCM", "EnFCM", "DBSCAN"], width=20)
        algorithm_combo.grid(row=2, column=3, padx=10, pady=22, sticky="w")

        # 创建一个Canvas组件，并将宽度设置为300，高度设置为300
        canvas = ttk.Canvas(root, width=300, height=870)
        canvas.place(x=540, y=130)
        canvas.create_line(50, 0, 50, 870, fill="grey", dash=(10, 10))

        # 图像聚类按钮
        cluster_button = ttk.Button(self.root, text="❹图像聚类", command=self.upload_right_image, width=14)

        def on_algorithm_selected(event):
            self.selected_algorithm = algorithm_combo.get()
            print("选择的算法是:", self.selected_algorithm)

            if self.selected_algorithm == "KMeans":
                self.para = []
                self.Kmeans_n_cluster = ttk.Label(self.root, text="n_cluster:", width=8)
                self.Kmeans_n_cluster.grid(row=3, column=2, padx=10, pady=8, sticky="w")
                self.Kmeans_n_cluster_input = ttk.Entry(self.root)
                self.Kmeans_n_cluster_input.grid(row=3, column=3, padx=10, pady=8, sticky="e")

                self.Kmeans_n_init = ttk.Label(self.root, text="n_init:", width=8)
                self.Kmeans_n_init.grid(row=4, column=2, padx=10, pady=2, sticky="w")
                self.Kmeans_n_init_input = ttk.Entry(self.root)
                self.Kmeans_n_init_input.grid(row=4, column=3, padx=10, pady=8, sticky="e")

                self.Kmeans_max_iter = ttk.Label(self.root, text="max_iter:", width=8)
                self.Kmeans_max_iter.grid(row=5, column=2, padx=5, pady=2, sticky="w")
                self.Kmeans_max_iter_input = ttk.Entry(self.root)
                self.Kmeans_max_iter_input.grid(row=5, column=3, padx=10, pady=8, sticky="e")

                self.K_notebook = ttk.Notebook(self.root)
                self.K_notebook.grid(row=7, column=2, columnspan=2, padx=10, pady=0)

                # 创建选项卡表示输出结果
                tab1 = ttk.Frame(self.K_notebook)
                self.K_notebook.add(tab1, text="参数设置")
                # 在选项卡中添加文本框
                self.K_output_panel = ttk.Text(tab1, height=15, width=32)
                self.K_output_panel.pack(pady=10)

                # submit_kmeans
                def on_enter_Kmeans():
                    self.Kmeans_n_cluster_num = self.Kmeans_n_cluster_input.get()
                    self.Kmeans_n_init_ = self.Kmeans_n_init_input.get()
                    self.Kmeans_max_iter_ = self.Kmeans_max_iter_input.get()
                    output_text = f"-----【{self.selected_algorithm}】-----\n" \
                                  f"聚类数n_cluster\t= {self.Kmeans_n_cluster_num}\n随机迭代次数n_init\t= " \
                                  f"{self.Kmeans_n_init_}\n最大迭代次数max_iter\t= {self.Kmeans_max_iter_}\n"
                    self.K_output_panel.insert(INSERT, output_text + "\n")
                    print("聚类数:", self.Kmeans_n_cluster_num)
                    print("随机迭代次数:", self.Kmeans_n_init_)
                    print("最大迭代次数:", self.Kmeans_max_iter_)
                    self.para.append(self.Kmeans_n_cluster_num)
                    self.para.append(self.Kmeans_max_iter_)
                    self.para.append(self.Kmeans_n_init_)

                self.ensure_Kbutton = ttk.Button(self.root, text="❸SUBMIT", command=on_enter_Kmeans, width=14)
                self.ensure_Kbutton.grid(row=6, column=2, padx=10, pady=20, columnspan=2, sticky="w")
                cluster_button.grid(row=6, column=2, padx=10, pady=20, columnspan=2, sticky="e")
            else:
                if hasattr(self, "Kmeans_max_iter_input"):
                    self.Kmeans_n_cluster.destroy()
                    self.Kmeans_n_cluster_input.destroy()
                    self.Kmeans_n_init.destroy()
                    self.Kmeans_n_init_input.destroy()
                    self.Kmeans_max_iter.destroy()
                    self.Kmeans_max_iter_input.destroy()
                    self.K_notebook.destroy()
                    self.ensure_Kbutton.destroy()

            if self.selected_algorithm == "FCM":
                self.para = []
                self.FCM_n_cluster = ttk.Label(self.root, text="n_cluster:", width=8)
                self.FCM_n_cluster.grid(row=3, column=2, padx=10, pady=8, sticky="w")
                self.FCM_n_cluster_input = ttk.Entry(self.root)
                self.FCM_n_cluster_input.grid(row=3, column=3, padx=10, pady=8, sticky="e")

                self.FCM_max_iter = ttk.Label(self.root, text="max_iter:", width=8)
                self.FCM_max_iter.grid(row=4, column=2, padx=10, pady=2, sticky="w")
                self.FCM_max_iter_input = ttk.Entry(self.root)
                self.FCM_max_iter_input.grid(row=4, column=3, padx=10, pady=8, sticky="e")

                self.FCM_fuzziness = ttk.Label(self.root, text="fuzziness:", width=8)
                self.FCM_fuzziness.grid(row=5, column=2, padx=5, pady=2, sticky="w")
                self.FCM_fuzziness_input = ttk.Entry(self.root)
                self.FCM_fuzziness_input.grid(row=5, column=3, padx=10, pady=8, sticky="e")

                self.FCM_epsilon = ttk.Label(self.root, text="epsilon:", width=8)
                self.FCM_epsilon.grid(row=6, column=2, padx=5, pady=2, sticky="w")
                self.FCM_epsilon_input = ttk.Entry(self.root)
                self.FCM_epsilon_input.grid(row=6, column=3, padx=10, pady=8, sticky="e")

                self.FCM_notebook = ttk.Notebook(self.root)
                self.FCM_notebook.grid(row=8, column=2, columnspan=2, padx=10, pady=0)

                # 创建选项卡表示输出结果
                tab1 = ttk.Frame(self.FCM_notebook)
                self.FCM_notebook.add(tab1, text="参数设置")
                # 在选项卡中添加文本框
                self.FCM_output_panel = ttk.Text(tab1, height=13, width=32)
                self.FCM_output_panel.pack(pady=10)

                # submit_FCM
                def on_enter_FCM():
                    self.FCM_n_cluster_num = self.FCM_n_cluster_input.get()
                    self.FCM_max_iter_ = self.FCM_max_iter_input.get()
                    self.FCM_fuzziness_ = self.FCM_fuzziness_input.get()
                    self.FCM_epsilon_ = self.FCM_epsilon_input.get()
                    output_text = f"-----【{self.selected_algorithm}】-----\n" \
                                  f"聚类数n_cluster\t= {self.FCM_n_cluster_num}\n" \
                                  f"最大迭代次数max_iter\t= {self.FCM_max_iter_}\n" \
                                  f"模糊度fuzziness\t= {self.FCM_fuzziness_}\n" \
                                  f"邻域半径epsilon\t= {self.FCM_epsilon_}\n"
                    self.FCM_output_panel.insert(INSERT, output_text + "\n")

                    print("FCM聚类数:", self.FCM_n_cluster_num)
                    print("最大迭代次数:", self.FCM_max_iter_)
                    print("模糊度:", self.FCM_fuzziness_)
                    print("邻域半径:", self.FCM_epsilon_)
                    self.para.append(self.FCM_n_cluster_num)
                    self.para.append(self.FCM_max_iter_)
                    self.para.append(self.FCM_fuzziness_)
                    self.para.append(self.FCM_epsilon_)

                self.ensure_FCMbutton = ttk.Button(self.root, text="❸SUBMIT", command=on_enter_FCM, width=14)
                self.ensure_FCMbutton.grid(row=7, column=2, padx=10, pady=20, columnspan=2, sticky="w")
                cluster_button.grid(row=7, column=2, padx=10, pady=20, columnspan=2, sticky="e")
            else:
                if hasattr(self, "FCM_max_iter_input"):
                    self.FCM_n_cluster.destroy()
                    self.FCM_n_cluster_input.destroy()
                    self.FCM_max_iter.destroy()
                    self.FCM_max_iter_input.destroy()
                    self.FCM_fuzziness.destroy()
                    self.FCM_fuzziness_input.destroy()
                    self.FCM_epsilon.destroy()
                    self.FCM_epsilon_input.destroy()
                    self.FCM_notebook.destroy()
                    self.ensure_FCMbutton.destroy()

            if self.selected_algorithm == "MFCM":
                self.para = []
                self.MFCM_n_cluster = ttk.Label(self.root, text="n_cluster:", width=8)
                self.MFCM_n_cluster.grid(row=3, column=2, padx=10, pady=8, sticky="w")
                self.MFCM_n_cluster_input = ttk.Entry(self.root)
                self.MFCM_n_cluster_input.grid(row=3, column=3, padx=10, pady=8, sticky="e")

                self.MFCM_max_iter = ttk.Label(self.root, text="max_iter:", width=8)
                self.MFCM_max_iter.grid(row=4, column=2, padx=10, pady=2, sticky="w")
                self.MFCM_max_iter_input = ttk.Entry(self.root)
                self.MFCM_max_iter_input.grid(row=4, column=3, padx=10, pady=8, sticky="e")

                self.MFCM_fuzziness = ttk.Label(self.root, text="fuzziness:", width=8)
                self.MFCM_fuzziness.grid(row=5, column=2, padx=5, pady=2, sticky="w")
                self.MFCM_fuzziness_input = ttk.Entry(self.root)
                self.MFCM_fuzziness_input.grid(row=5, column=3, padx=10, pady=8, sticky="e")

                self.MFCM_epsilon = ttk.Label(self.root, text="epsilon:", width=8)
                self.MFCM_epsilon.grid(row=6, column=2, padx=5, pady=2, sticky="w")
                self.MFCM_epsilon_input = ttk.Entry(self.root)
                self.MFCM_epsilon_input.grid(row=6, column=3, padx=10, pady=8, sticky="e")

                self.MFCM_nei_effect = ttk.Label(self.root, text="nei_effect:", width=8)
                self.MFCM_nei_effect.grid(row=7, column=2, padx=5, pady=2, sticky="w")
                self.MFCM_nei_effect_input = ttk.Entry(self.root)
                self.MFCM_nei_effect_input.grid(row=7, column=3, padx=10, pady=8, sticky="e")

                self.MFCM_kernel = ttk.Label(self.root, text="kernel:", width=8)
                self.MFCM_kernel.grid(row=8, column=2, padx=5, pady=2, sticky="w")
                self.MFCM_kernel_input = ttk.Entry(self.root)
                self.MFCM_kernel_input.grid(row=8, column=3, padx=10, pady=8, sticky="e")

                self.MFCM_notebook = ttk.Notebook(self.root)
                self.MFCM_notebook.grid(row=10, column=2, columnspan=2, padx=10, pady=0)

                # 创建选项卡表示输出结果
                tab1 = ttk.Frame(self.MFCM_notebook)
                self.MFCM_notebook.add(tab1, text="参数设置")
                # 在选项卡中添加文本框
                self.MFCM_output_panel = ttk.Text(tab1, height=9, width=32)
                self.MFCM_output_panel.pack(pady=10)

                # submit_MFCM
                def on_enter_MFCM():
                    self.MFCM_n_cluster_num = self.MFCM_n_cluster_input.get()
                    self.MFCM_max_iter_ = self.MFCM_max_iter_input.get()
                    self.MFCM_fuzziness_ = self.MFCM_fuzziness_input.get()
                    self.MFCM_epsilon_ = self.MFCM_epsilon_input.get()
                    self.MFCM_nei_effect_ = self.MFCM_nei_effect_input.get()
                    self.MFCM_kernel_ = self.MFCM_kernel_input.get()
                    output_text = f"-----【{self.selected_algorithm}】-----\n" \
                                  f"聚类数n_cluster\t= {self.MFCM_n_cluster_num}\n" \
                                  f"最大迭代次数max_iter\t= {self.MFCM_max_iter_}\n" \
                                  f"模糊度fuzziness\t= {self.MFCM_fuzziness_}\n" \
                                  f"邻域半径epsilon\t= {self.MFCM_epsilon_}\n" \
                                  f"邻域效应因子neighbour_effect\t= {self.MFCM_nei_effect_}\n" \
                                  f"kernel_size\t= {self.MFCM_kernel_}\n"
                    self.MFCM_output_panel.insert(INSERT, output_text + "\n")

                    print("MFCM聚类数:", self.MFCM_n_cluster_num)
                    print("最大迭代次数:", self.MFCM_max_iter_)
                    print("模糊度:", self.MFCM_fuzziness_)
                    print("邻域半径:", self.MFCM_epsilon_)
                    print("邻域效应因子:", self.MFCM_nei_effect_)
                    print("kernel:", self.MFCM_kernel_)
                    self.para.append(self.MFCM_n_cluster_num)
                    self.para.append(self.MFCM_max_iter_)
                    self.para.append(self.MFCM_fuzziness_)
                    self.para.append(self.MFCM_epsilon_)
                    self.para.append(self.MFCM_nei_effect_)
                    self.para.append(self.MFCM_kernel_)

                self.ensure_MFCMbutton = ttk.Button(self.root, text="❸SUBMIT", command=on_enter_MFCM, width=14)
                self.ensure_MFCMbutton.grid(row=9, column=2, padx=10, pady=20, columnspan=2, sticky="w")
                cluster_button.grid(row=9, column=2, padx=10, pady=20, columnspan=2, sticky="e")
            else:
                if hasattr(self, "MFCM_max_iter_input"):
                    self.MFCM_n_cluster.destroy()
                    self.MFCM_n_cluster_input.destroy()
                    self.MFCM_max_iter.destroy()
                    self.MFCM_max_iter_input.destroy()
                    self.MFCM_fuzziness.destroy()
                    self.MFCM_fuzziness_input.destroy()
                    self.MFCM_epsilon.destroy()
                    self.MFCM_epsilon_input.destroy()
                    self.MFCM_nei_effect.destroy()
                    self.MFCM_nei_effect_input.destroy()
                    self.MFCM_kernel.destroy()
                    self.MFCM_kernel_input.destroy()
                    self.MFCM_notebook.destroy()
                    self.ensure_MFCMbutton.destroy()

            if self.selected_algorithm == "EnFCM":
                self.para = []
                self.EnFCM_n_cluster = ttk.Label(self.root, text="n_cluster:", width=8)
                self.EnFCM_n_cluster.grid(row=3, column=2, padx=10, pady=8, sticky="w")
                self.EnFCM_n_cluster_input = ttk.Entry(self.root)
                self.EnFCM_n_cluster_input.grid(row=3, column=3, padx=10, pady=8, sticky="e")

                self.EnFCM_max_iter = ttk.Label(self.root, text="max_iter:", width=8)
                self.EnFCM_max_iter.grid(row=4, column=2, padx=10, pady=2, sticky="w")
                self.EnFCM_max_iter_input = ttk.Entry(self.root)
                self.EnFCM_max_iter_input.grid(row=4, column=3, padx=10, pady=8, sticky="e")

                self.EnFCM_fuzziness = ttk.Label(self.root, text="fuzziness:", width=8)
                self.EnFCM_fuzziness.grid(row=5, column=2, padx=5, pady=2, sticky="w")
                self.EnFCM_fuzziness_input = ttk.Entry(self.root)
                self.EnFCM_fuzziness_input.grid(row=5, column=3, padx=10, pady=8, sticky="e")

                self.EnFCM_epsilon = ttk.Label(self.root, text="epsilon:", width=8)
                self.EnFCM_epsilon.grid(row=6, column=2, padx=5, pady=2, sticky="w")
                self.EnFCM_epsilon_input = ttk.Entry(self.root)
                self.EnFCM_epsilon_input.grid(row=6, column=3, padx=10, pady=8, sticky="e")

                self.EnFCM_nei_effect = ttk.Label(self.root, text="nei_effect:", width=8)
                self.EnFCM_nei_effect.grid(row=7, column=2, padx=5, pady=2, sticky="w")
                self.EnFCM_nei_effect_input = ttk.Entry(self.root)
                self.EnFCM_nei_effect_input.grid(row=7, column=3, padx=10, pady=8, sticky="e")

                self.EnFCM_kernel = ttk.Label(self.root, text="kernel:", width=8)
                self.EnFCM_kernel.grid(row=8, column=2, padx=5, pady=2, sticky="w")
                self.EnFCM_kernel_input = ttk.Entry(self.root)
                self.EnFCM_kernel_input.grid(row=8, column=3, padx=10, pady=8, sticky="e")

                self.EnFCM_notebook = ttk.Notebook(self.root)
                self.EnFCM_notebook.grid(row=10, column=2, columnspan=2, padx=10, pady=0)

                # 创建选项卡表示输出结果
                tab1 = ttk.Frame(self.EnFCM_notebook)
                self.EnFCM_notebook.add(tab1, text="参数设置")
                # 在选项卡中添加文本框
                self.EnFCM_output_panel = ttk.Text(tab1, height=9, width=32)
                self.EnFCM_output_panel.pack(pady=10)

                # submit_EnFCM
                def on_enter_EnFCM():
                    self.EnFCM_n_cluster_num = self.EnFCM_n_cluster_input.get()
                    self.EnFCM_max_iter_ = self.EnFCM_max_iter_input.get()
                    self.EnFCM_fuzziness_ = self.EnFCM_fuzziness_input.get()
                    self.EnFCM_epsilon_ = self.EnFCM_epsilon_input.get()
                    self.EnFCM_nei_effect_ = self.EnFCM_nei_effect_input.get()
                    self.EnFCM_kernel_ = self.EnFCM_kernel_input.get()
                    output_text = f"-----【{self.selected_algorithm}】-----\n" \
                                  f"聚类数n_cluster\t= {self.EnFCM_n_cluster_num}\n" \
                                  f"最大迭代次数max_iter\t= {self.EnFCM_max_iter_}\n" \
                                  f"模糊度fuzziness\t= {self.EnFCM_fuzziness_}\n" \
                                  f"邻域半径epsilon\t= {self.EnFCM_epsilon_}\n" \
                                  f"邻域效应因子neighbour_effect\t= {self.EnFCM_nei_effect_}\n" \
                                  f"kernel_size\t= {self.EnFCM_kernel_}\n"
                    self.EnFCM_output_panel.insert(INSERT, output_text + "\n")

                    print("EnFCM聚类数:", self.EnFCM_n_cluster_num)
                    print("最大迭代次数:", self.EnFCM_max_iter_)
                    print("模糊度:", self.EnFCM_fuzziness_)
                    print("邻域半径:", self.EnFCM_epsilon_)
                    print("邻域效应因子:", self.EnFCM_nei_effect_)
                    print("kernel:", self.EnFCM_kernel_)
                    self.para.append(self.EnFCM_n_cluster_num)
                    self.para.append(self.EnFCM_max_iter_)
                    self.para.append(self.EnFCM_fuzziness_)
                    self.para.append(self.EnFCM_epsilon_)
                    self.para.append(self.EnFCM_nei_effect_)
                    self.para.append(self.EnFCM_kernel_)

                self.ensure_EnFCMbutton = ttk.Button(self.root, text="❸SUBMIT", command=on_enter_EnFCM, width=14)
                self.ensure_EnFCMbutton.grid(row=9, column=2, padx=10, pady=20, columnspan=2, sticky="w")
                cluster_button.grid(row=9, column=2, padx=10, pady=20, columnspan=2, sticky="e")
            else:
                if hasattr(self, "EnFCM_max_iter_input"):
                    self.EnFCM_n_cluster.destroy()
                    self.EnFCM_n_cluster_input.destroy()
                    self.EnFCM_max_iter.destroy()
                    self.EnFCM_max_iter_input.destroy()
                    self.EnFCM_fuzziness.destroy()
                    self.EnFCM_fuzziness_input.destroy()
                    self.EnFCM_epsilon.destroy()
                    self.EnFCM_epsilon_input.destroy()
                    self.EnFCM_nei_effect.destroy()
                    self.EnFCM_nei_effect_input.destroy()
                    self.EnFCM_kernel.destroy()
                    self.EnFCM_kernel_input.destroy()
                    self.EnFCM_notebook.destroy()
                    self.ensure_EnFCMbutton.destroy()

            if self.selected_algorithm == "DBSCAN":
                self.para = []
                self.DBSCAN_n_segment = ttk.Label(self.root, text="n_segment:", width=8)
                self.DBSCAN_n_segment.grid(row=3, column=2, padx=10, pady=8, sticky="w")
                self.DBSCAN_n_segment_input = ttk.Entry(self.root)
                self.DBSCAN_n_segment_input.grid(row=3, column=3, padx=10, pady=8, sticky="e")

                self.DBSCAN_max_iter = ttk.Label(self.root, text="max_iter:", width=8)
                self.DBSCAN_max_iter.grid(row=4, column=2, padx=10, pady=2, sticky="w")
                self.DBSCAN_max_iter_input = ttk.Entry(self.root)
                self.DBSCAN_max_iter_input.grid(row=4, column=3, padx=10, pady=8, sticky="e")

                self.DBSCAN_compactness = ttk.Label(self.root, text="compactness:", width=8)
                self.DBSCAN_compactness.grid(row=5, column=2, padx=5, pady=2, sticky="w")
                self.DBSCAN_compactness_input = ttk.Entry(self.root)
                self.DBSCAN_compactness_input.grid(row=5, column=3, padx=10, pady=8, sticky="e")

                self.DBSCAN_epsilon = ttk.Label(self.root, text="epsilon:", width=8)
                self.DBSCAN_epsilon.grid(row=6, column=2, padx=5, pady=2, sticky="w")
                self.DBSCAN_epsilon_input = ttk.Entry(self.root)
                self.DBSCAN_epsilon_input.grid(row=6, column=3, padx=10, pady=8, sticky="e")

                self.DBSCAN_min_samples = ttk.Label(self.root, text="min_samples:", width=8)
                self.DBSCAN_min_samples.grid(row=7, column=2, padx=5, pady=2, sticky="w")
                self.DBSCAN_min_samples_input = ttk.Entry(self.root)
                self.DBSCAN_min_samples_input.grid(row=7, column=3, padx=10, pady=8, sticky="e")

                self.DBSCAN_notebook = ttk.Notebook(self.root)
                self.DBSCAN_notebook.grid(row=9, column=2, columnspan=2, padx=10, pady=0)

                # 创建选项卡表示输出结果
                tab1 = ttk.Frame(self.DBSCAN_notebook)
                self.DBSCAN_notebook.add(tab1, text="参数设置")
                # 在选项卡中添加文本框
                self.DBSCAN_output_panel = ttk.Text(tab1, height=11, width=32)
                self.DBSCAN_output_panel.pack(pady=10)

                # submit_DBSCAN
                def on_enter_DBSCAN():
                    self.DBSCAN_n_segment_num = self.DBSCAN_n_segment_input.get()
                    self.DBSCAN_max_iter_ = self.DBSCAN_max_iter_input.get()
                    self.DBSCAN_compactness_ = self.DBSCAN_compactness_input.get()
                    self.DBSCAN_epsilon_ = self.DBSCAN_epsilon_input.get()
                    self.DBSCAN_min_samples_ = self.DBSCAN_min_samples_input.get()
                    output_text = f"-----【{self.selected_algorithm}】-----\n" \
                                  f"超像素数量n_segment\t= {self.DBSCAN_n_segment_num}\n" \
                                  f"最大迭代次数max_iter\t= {self.DBSCAN_max_iter_}\n" \
                                  f"紧凑度compactness\t= {self.DBSCAN_compactness_}\n" \
                                  f"邻域半径epsilon\t= {self.DBSCAN_epsilon_}\n" \
                                  f"最小样本数min_samples\t= {self.DBSCAN_min_samples_}\n"
                    self.DBSCAN_output_panel.insert(INSERT, output_text + "\n")

                    print("DBSCAN超像素数量:", self.DBSCAN_n_segment_num)
                    print("最大迭代次数:", self.DBSCAN_max_iter_)
                    print("紧凑度:", self.DBSCAN_compactness_)
                    print("邻域半径:", self.DBSCAN_epsilon_)
                    print("最小样本数:", self.DBSCAN_min_samples_)
                    self.para.append(self.DBSCAN_n_segment_num)
                    self.para.append(self.DBSCAN_max_iter_)
                    self.para.append(self.DBSCAN_compactness_)
                    self.para.append(self.DBSCAN_epsilon_)
                    self.para.append(self.DBSCAN_min_samples_)

                self.ensure_DBSCANbutton = ttk.Button(self.root, text="❸SUBMIT", command=on_enter_DBSCAN, width=14)
                self.ensure_DBSCANbutton.grid(row=8, column=2, padx=10, pady=20, columnspan=2, sticky="w")
                cluster_button.grid(row=8, column=2, padx=10, pady=20, columnspan=2, sticky="e")
            else:
                if hasattr(self, "DBSCAN_max_iter_input"):
                    self.DBSCAN_n_segment.destroy()
                    self.DBSCAN_n_segment_input.destroy()
                    self.DBSCAN_max_iter.destroy()
                    self.DBSCAN_max_iter_input.destroy()
                    self.DBSCAN_compactness.destroy()
                    self.DBSCAN_compactness_input.destroy()
                    self.DBSCAN_epsilon.destroy()
                    self.DBSCAN_epsilon_input.destroy()
                    self.DBSCAN_min_samples.destroy()
                    self.DBSCAN_min_samples_input.destroy()
                    self.DBSCAN_notebook.destroy()
                    self.ensure_DBSCANbutton.destroy()

        # 绑定选择事件
        algorithm_combo.bind("<<ComboboxSelected>>", on_algorithm_selected)

        # 图片显示区域
        self.left_image_label = ttk.Label(self.root)
        self.left_image_label.place(x=650, y=110)
        ttk.Label(self.root, text="【原 图】").place(x=650, y=60)
        # 右侧显示聚类后图片的区域
        self.right_image_label = ttk.Label(self.root)
        self.right_image_label.place(x=650, y=600)
        ttk.Label(self.root, text="【聚类后的图像】").place(x=650, y=550)

    # 加载原图
    def upload_left_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.bmp")])
        # print(file_path)
        if self.file_path:
            image = Image.open(self.file_path)
            image.thumbnail((550, 550))
            photo = ImageTk.PhotoImage(image)
            self.left_image_label.configure(image=photo)
            self.left_image_label.image = photo  # 保持对图片的引用

            # 获取图片文件名
            self.image_name = os.path.basename(self.file_path)
            print("Uploaded file name:", self.image_name)

    # 加载聚类后的图像
    def upload_right_image(self):
        output_path = M(self.file_path, self.selected_algorithm, self.para)
        # file_path = "algorithm/output/" + self.selected_algorithm + "/segmentation/" + self.image_name
        # file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.bmp")])
        if output_path:
            image = Image.open(output_path)
            image.thumbnail((550, 550))
            photo = ImageTk.PhotoImage(image)
            self.right_image_label.configure(image=photo)
            self.right_image_label.image = photo  # 保持对图片的引用


if __name__ == "__main__":
    root = ttk.Window("基于聚类算法的图像分割系统——图像聚类", themename="superhero")
    app = ImageProcessingApp(root)
    root.mainloop()
