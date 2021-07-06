'''Export calculated clustering to excel file.'''
import xlsxwriter

from data_extraction.representants import get_repr_list


def cluster_to_excel(path, clusters, noise, clusters_compressed, noise_compressed, comp_to_normal_map, cluster_sizes,
                     noise_size, cluster_sizes_compressed, noise_size_compressed,
                     average_intra_cluster_distances_per_cluster_per_value,
                     intra_cluster_distances):
    aicdpcpv = average_intra_cluster_distances_per_cluster_per_value

    if not (path.endswith('.xlsx')):
        path += '.xlsx'

    workbook = xlsxwriter.Workbook(path)
    style_caption = workbook.add_format({'bold': True, 'font_color': 'red', 'left': 2, 'bottom': 1, 'font_size': 15, 'bg_color': '#DDDDDD'})
    style_sum = workbook.add_format({'bold': True, 'font_color': 'blue', 'left': 2, 'bottom': 1, 'bg_color': '#DDDDDD'})
    style_grey = workbook.add_format({'bg_color': '#DDDDDD', 'bottom': 1})
    style_grey_right = workbook.add_format({'right': 2, 'bg_color': '#DDDDDD', 'bottom': 1})
    # style_sums = workbook.add_format({'right': 2, 'bottom': 1})
    # style_value = workbook.add_format({'left': 2})
    # style_occurrence = workbook.add_format({'right': 2, 'font_color': 'grey'})

    style_val = workbook.add_format()
    style_val_right = workbook.add_format({'right': 2})
    style_val_left = workbook.add_format({'left': 2})

    sheet1 = workbook.add_worksheet("Cluster_Original")
    sheet1.write(2, 0, "#original", style_sum)
    sheet1.set_column(0, 0, 12)

    sheet1.write(1, 0, "", style_grey)
    sheet1.write(1, 1, "Noise", style_caption)
    sheet1.write(1, 2, "", style_grey)
    sheet1.write_number(2, 1, len(noise), style_sum)
    sheet1.write(2, 2, "", style_grey_right)
    sheet1.set_column(1, 1, 15)
    sheet1.set_column(2, 2, 6)
    noise_unique, noise_count = get_sorted_unique_values_counts(noise)
    write_list_to_sheet(sheet1, 3, 1, noise_unique, style_val_left)
    write_list_to_sheet(sheet1, 3, 2, noise_count, style_val_right, True)
    sheet1.conditional_format(3, 2, 3 + len(noise_count), 2, {'type': 'data_bar'})

    cluster_sizes = list(map(len, clusters))
    cluster_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(clusters))), cluster_sizes)

    for i, v in enumerate(cluster_indices_sorted):
        name = "Cluster " + str(i + 1)
        sheet1.write(1, i * 2 + 3, name, style_caption)
        sheet1.write(1, i * 2 + 4, "", style_grey_right)
        sheet1.write_number(2, i * 2 + 3, cluster_counts_sorted[i], style_sum)
        sheet1.write(2, i * 2 + 4, "", style_grey_right)
        sheet1.set_column(3 + i * 2, 3 + i * 2, 15)
        sheet1.set_column(4 + i * 2, 4 + i * 2, 6)
        cluster_unique, cluster_count = get_sorted_unique_values_counts(clusters[v])
        write_list_to_sheet(sheet1, 3, i * 2 + 3, cluster_unique, style_val_left)
        write_list_to_sheet(sheet1, 3, i * 2 + 4, cluster_count, style_val_right, True)
        sheet1.conditional_format(3, i * 2 + 4, 3 + len(cluster_count), i * 2 + 4, {'type': 'data_bar'})
    sheet1.conditional_format(2, 1, 2, 3 + 2 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#63C384'})

    if not comp_to_normal_map is None:

        sheet2 = workbook.add_worksheet("Cluster_Repr")
        sheet2.write(2, 0, "#original", style_sum)
        sheet2.write(3, 0, "#compressed", style_sum)
        sheet2.set_column(0, 0, 12)

        sheet2.write(1, 0, "", style_grey)
        sheet2.write(1, 1, "Noise", style_caption)
        sheet2.write(1, 2, "", style_grey)
        sheet2.write_number(2, 1, len(noise_compressed), style_sum)
        sheet2.write(2, 2, "", style_grey_right)
        sheet2.write_number(3, 1, len(noise), style_sum)
        sheet2.write(3, 2, "", style_grey_right)
        sheet2.set_column(1, 1, 15)
        sheet2.set_column(2, 2, 6)
        noise_repr, noise_count = get_sorted_representatives_counts(comp_to_normal_map, noise_compressed)
        write_list_to_sheet(sheet2, 4, 1, noise_repr, style_val_left)
        write_list_to_sheet(sheet2, 4, 2, noise_count, style_val_right, True)
        sheet2.conditional_format(4, 2, 3 + len(noise_count), 2, {'type': 'data_bar'})

        cluster_compressed_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(clusters_compressed))), cluster_sizes)

        for i, v in enumerate(cluster_compressed_indices_sorted):
            name = "Cluster " + str(i + 1)
            sheet2.write(1, i * 2 + 3, name, style_caption)
            sheet2.write(1, i * 2 + 4, "", style_grey_right)
            sheet2.write_number(2, i * 2 + 3, cluster_counts_sorted[i], style_sum)
            sheet2.write(2, i * 2 + 4, "", style_grey_right)
            sheet2.write_number(3, i * 2 + 3, len(clusters_compressed[v]), style_sum)
            sheet2.write(3, i * 2 + 4, "", style_grey_right)
            sheet2.set_column(3 + i * 2, 3 + i * 2, 15)
            sheet2.set_column(4 + i * 2, 4 + i * 2, 6)
            cluster_repr, cluster_count = get_sorted_representatives_counts(comp_to_normal_map, clusters_compressed[v])
            write_list_to_sheet(sheet2, 4, i * 2 + 3, cluster_repr, style_val_left)
            write_list_to_sheet(sheet2, 4, i * 2 + 4, cluster_count, style_val_right, True)
            sheet2.conditional_format(4, i * 2 + 4, 4 + len(cluster_count), i * 2 + 4, {'type': 'data_bar'})
        sheet2.conditional_format(2, 1, 2, 3 + 2 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#63C384'})
        sheet2.conditional_format(3, 1, 3, 3 + 2 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#C3C365'})

    if not comp_to_normal_map is None and True:

        sheet3 = workbook.add_worksheet("Cluster_Repr_Dists")
        sheet3.write(2, 0, "#original", style_sum)
        sheet3.write(3, 0, "#compressed", style_sum)
        sheet3.write(4, 0, "#variance", style_sum)
        sheet3.set_column(0, 0, 12)

        sheet3.write(1, 0, "", style_grey)
        sheet3.write(1, 1, "Noise", style_caption)
        sheet3.write(1, 2, "", style_grey)
        sheet3.write(1, 3, "", style_grey_right)
        sheet3.write_number(2, 1, len(noise_compressed), style_sum)
        sheet3.write(2, 2, "", style_grey)
        sheet3.write(2, 3, "", style_grey_right)
        sheet3.write_number(3, 1, len(noise), style_sum)
        sheet3.write(3, 2, "", style_grey)
        sheet3.write(3, 3, "", style_grey_right)
        sheet3.write(4, 1, "", style_sum)
        sheet3.write(4, 2, "", style_grey)
        sheet3.write(4, 3, "", style_grey_right)
        sheet3.set_column(1, 1, 15)
        sheet3.set_column(2, 2, 6)
        noise_repr, noise_count = get_sorted_representatives_counts(comp_to_normal_map, noise_compressed)
        write_list_to_sheet(sheet3, 5, 1, noise_repr, style_val_left)
        write_list_to_sheet(sheet3, 5, 2, noise_count, style_val, True)
        sheet3.conditional_format(5, 2, 5 + len(noise_count), 2, {'type': 'data_bar'})

        cluster_compressed_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(clusters_compressed))), cluster_sizes)

        for i, v in enumerate(cluster_compressed_indices_sorted):
            name = "Cluster " + str(i + 1)
            sheet3.write(1, i * 3 + 4, name, style_caption)
            sheet3.write(1, i * 3 + 5, "", style_grey)
            sheet3.write(1, i * 3 + 6, "", style_grey_right)

            sheet3.write_number(2, i * 3 + 4, cluster_counts_sorted[i], style_sum)
            sheet3.write(2, i * 3 + 5, "", style_grey)
            sheet3.write(2, i * 3 + 6, "", style_grey_right)

            sheet3.write_number(3, i * 3 + 4, len(clusters_compressed[v]), style_sum)
            sheet3.write(3, i * 3 + 5, "", style_grey)
            sheet3.write(3, i * 3 + 6, "", style_grey_right)

            sheet3.write_number(4, i * 3 + 4, intra_cluster_distances[v], style_sum)
            sheet3.write(4, i * 3 + 5, "", style_grey)
            sheet3.write(4, i * 3 + 6, "", style_grey_right)

            sheet3.set_column(4 + i * 3, 4 + i * 3, 15)
            sheet3.set_column(5 + i * 3, 5 + i * 3, 6)
            sheet3.set_column(6 + i * 3, 6 + i * 3, 6)

            cluster_repr, cluster_count, cluster_intra = get_sorted_representatives_counts(comp_to_normal_map, clusters_compressed[v], aicdpcpv[v])
            write_list_to_sheet(sheet3, 5, i * 3 + 4, cluster_repr, style_val_left)
            write_list_to_sheet(sheet3, 5, i * 3 + 5, cluster_count, style_val, True)
            write_list_to_sheet(sheet3, 5, i * 3 + 6, cluster_intra, style_val_right)

            sheet3.conditional_format(5, i * 3 + 5, 5 + len(cluster_count), i * 3 + 5, {'type': 'data_bar'})
            sheet3.conditional_format(5, i * 3 + 6, 5 + len(cluster_count), i * 3 + 6, {'type': 'data_bar', 'bar_color': '#C36565'})

        sheet3.conditional_format(2, 1, 2, 4 + 3 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#63C384'})
        sheet3.conditional_format(3, 1, 3, 4 + 3 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#C3C365'})
        sheet3.conditional_format(4, 1, 4, 4 + 3 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#666666'})

    workbook.close()


def get_sorted_representatives_counts(comp_to_normal_map, values_compressed, values_intra=None):
    noise_repr = get_repr_list(values_compressed, comp_to_normal_map)
    noise_count = get_compressed_count(values_compressed, comp_to_normal_map)
    if not values_intra is None:
        a, b = sort_values_counts(noise_repr, noise_count)
        c, d = sort_values_counts(values_intra, noise_count)
        return a, b, c
    else:
        return sort_values_counts(noise_repr, noise_count)


def sort_values_counts(values, counts):
    if not values or not counts:
        return [], []
    res = list(zip(*sorted(zip(counts, values), reverse=True)))
    return res[1], res[0]
    # cluster_unique_count_dict = dict(zip(values, counts))
    # d_sorted = {k: v for k, v in sorted(cluster_unique_count_dict.items(), key=lambda item: item[1], reverse=True)}
    # return list(d_sorted.keys()), list(d_sorted.values())


def get_compressed_count(values_compressed, comp_to_normal_map):
    noise_count = []
    for u in values_compressed:
        noise_count.append(len(comp_to_normal_map[u]))
    return noise_count


def get_sorted_unique_values_counts(cluster):
    cluster_unique = list(set(cluster))
    cluster_count = []
    for u in cluster_unique:
        cluster_count.append(cluster.count(u))
    return sort_values_counts(cluster_unique, cluster_count)


def write_list_to_sheet(sheet, x, y, list, style=None, number=False):
    for i, v in enumerate(list):
        if number:
            sheet.write_number(x + i, y, v, style)
        else:
            sheet.write(x + i, y, v, style)


if __name__ == '__main__':
    X = ["abcd", "basd", "bqwr", "ayc", "cyc", "  ayc", "vyc", "das", "bdas"]
    Y = [0, 1, 1, 0, 13, 2, 2, 0, 1]
    print(list(zip(*sorted(zip(Y, X))))[0])
    print(list(zip(*sorted(zip(Y, X))))[1])

    result: [(0, 0, 0, 1, 1, 1, 1, 2, 2), ('a', 'a', 'd', 'b', 'b', 'b', 'c', 'a', 'v')]

    #
    # path = "file.xlsx"
    # clusters = [
    #     ['value1', 'value2', 'value3', 'value4', 'value1', 'value2'],
    #     ['value5', 'value6']
    # ]
    # noise = ['value7']
    # clusters_compressed = [
    #     ['key1', 'key2'],
    #     ['key3']
    # ]
    # noise_compressed = ['key4']
    # comp_to_normal_map = {'key1': ['value1', 'value2'], 'key2': ['value3', 'value4'], 'key3': ['value5', 'value6'],
    #                       'key4': ['value7']}
    #
    # cluster_to_excel(path, clusters, noise, clusters_compressed, noise_compressed, comp_to_normal_map)
