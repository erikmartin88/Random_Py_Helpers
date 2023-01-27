from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x =[9975, 10944, 132, 791, 10622, 1307, 27935, 40, 61, 25274, 9750, 17935, 2220, 8314, 5, 7651, 6312, 23001, 4135, 14788, 1230, 6645, 734, 3763, 7437, 7567, 17731, 6265, 2551, 2093, 1879, 11631, 10392, 9182, 10714, 12638, 8427, 9340, 8277, 9378]
y =[57.05188, 54.74771, 85.46905, 80.76425, 55.60758, 77.97668, 51.01239, 86.21508, 85.76121, 51.11282, 57.64727, 51.38063, 74.16076, 58.78351, 86.41393, 61.09713, 69.06699, 54.11835, 72.52402, 52.44466, 78.62599, 65.0938, 84.94718, 73.7547, 67.137, 64.62401, 59.80875, 73.04021, 75.32301, 76.68723, 78.64956, 54.0873, 59.32618, 60.11634, 55.83376, 53.56688, 59.83233, 58.42517, 60.87666, 58.7047]
z =[562, 638, 1841, 1643, 707, 1309, 212, 1957, 1890, 246, 593, 401, 1026, 718, 1983, 779, 1084, 232, 1282, 477, 1382, 841, 1932, 1190, 737, 822, 407, 996, 740, 1306, 1244, 518, 436, 587, 562, 562, 594, 683, 840, 652]

xint = [27931, 734, 5025, 14788, 23001, 10392, 7567, 15474, 24573, 474, 2551, 11631, 6265, 17731, 6027, 9378, 7167, 4395, 7204, 3670, 3215, 8277, 10159, 8427, 3933, 2250, 4258, 502, 0, 4236, 7779, 5450, 2892, 7758, 2093, 576, 3353, 5726, 1230, 367, 9340, 6312, 5349, 7191, 10003, 13466, 5542, 2753, 15587, 26743, 1429, 930, 3243, 5114, 7437, 6645, 326, 1879, 12638, 23979, 2071, 3257, 4135, 2729, 17931, 16436, 3763, 6603, 8146, 9182, 10714, 7861, 4964, 350, 682, 677, 1486, 9858, 3711, 7362, 25587, 3505, 1548, 7651, 5, 14574, 8314, 16743, 7762, 5167, 2022, 14236, 1145, 2220, 17935, 1486, 7047, 11707, 5147, 25353, 4, 9750, 24, 1882, 1, 24005, 821, 45, 8, 1833, 54, 25274, 1781, 3057, 7769, 4106, 8958, 12036, 61, 4161, 26181, 40, 453, 426, 4541, 2574, 27935, 26743, 2849, 13849, 1307, 4064, 2155, 10622, 791, 12961, 4653, 1485, 27455, 139, 13294, 1413, 440, 132, 653, 10944, 5772, 9975, 4709, 6204, 6234, 2245, 6749]
yint = [51.01264, 84.94718, 68.15612, 52.44466, 54.11835, 59.32618, 64.62401, 51.40307, 51.33541, 81.88262, 75.32301, 54.0873, 73.04021, 59.80875, 68.57045, 58.7047, 62.25445, 69.02192, 59.41328, 72.13155, 72.25083, 60.87666, 55.54138, 59.83233, 71.35075, 73.86552, 68.37872, 82.64819, 86.42457, 66.74039, 60.96229, 67.00333, 72.52164, 60.69623, 76.68723, 82.99056, 71.12923, 66.19167, 78.62599, 84.23469, 58.42517, 69.06699, 66.49249, 60.30624, 56.52328, 51.97128, 65.58475, 73.15595, 51.41154, 51.01405, 76.0527, 78.82007, 71.50761, 65.16821, 67.137, 65.0938, 81.55935, 78.64956, 53.56688, 51.42245, 74.94095, 71.48238, 72.52402, 73.24715, 51.38379, 51.42995, 73.7547, 63.2864, 60.99572, 60.11634, 55.83376, 60.98801, 66.05314, 82.21386, 83.95493, 81.93147, 76.08849, 57.28366, 70.39165, 61.17649, 51.04331, 70.42516, 76.60852, 61.09713, 86.41393, 51.42295, 58.78351, 51.38229, 60.68779, 65.66096, 74.89775, 51.6393, 78.06518, 74.16076, 51.38063, 76.7792, 61.84319, 53.75975, 65.89042, 51.10696, 86.41631, 57.64727, 86.27644, 75.9762, 86.41702, 51.12499, 78.70575, 85.96011, 86.29456, 76.29162, 85.78461, 51.11282, 76.34866, 70.5378, 60.55596, 70.05854, 57.98556, 53.53534, 85.76121, 68.90421, 51.01717, 86.21508, 81.1918, 82.86206, 67.65763, 72.61652, 51.01239, 51.01405, 71.58623, 52.38131, 77.97668, 70.37025, 74.23709, 55.60758, 80.76425, 52.79861, 67.11853, 76.79635, 51.01402, 82.92332, 52.65104, 76.83022, 82.85117, 85.46905, 80.92814, 54.74771, 64.89668, 57.05188, 66.85906, 64.74954, 63.23304, 74.01421, 62.65334]
zint =[212, 1932, 822, 477, 232, 436, 822, 401, 212, 1623, 740, 518, 996, 407, 937, 652, 753, 1027, 512, 927, 1178, 840, 596, 594, 1273, 966, 697, 1774, 1983, 443, 495, 886, 1173, 512, 1306, 1637, 951, 948, 1382, 1713, 683, 1084, 663, 732, 401, 401, 842, 1107, 401, 212, 1009, 1373, 759, 537, 737, 841, 1641, 1244, 562, 212, 978, 945, 1282, 763, 401, 401, 1190, 827, 666, 587, 562, 758, 550, 1731, 1784, 1721, 855, 485, 838, 738, 212, 495, 1130, 779, 1983, 401, 718, 401, 512, 657, 880, 443, 946, 1026, 401, 1062, 701, 562, 663, 212, 1983, 593, 1958, 1070, 1983, 246, 984, 1906, 1952, 1081, 1890, 246, 984, 560, 687, 1081, 401, 401, 1890, 890, 212, 1957, 1438, 1396, 711, 646, 212, 212, 771, 426, 1309, 797, 1007, 707, 1643, 426, 746, 752, 212, 1693, 426, 955, 1788, 1841, 1624, 638, 868, 562, 550, 833, 886, 600, 658]

ax.scatter(xint, yint, zint, c='b', marker='o')
ax.scatter(x, y, z, c='r', marker='o')



ax.set_xlabel('MW')
ax.set_ylabel('SCEN_WCSI_PCT')
ax.set_zlabel('SCEN_BASIN_CON_KM')

plt.show()