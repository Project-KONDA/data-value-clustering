'''Export calculated clustering to excel file.'''
import xlsxwriter

from data_extraction.representants import get_repr_list


def cluster_to_excel(path, clusters, noise, clusters_compressed, noise_compressed, comp_to_normal_map,
                     average_intra_cluster_distances_per_cluster_per_value,
                     intra_cluster_distances, simple_cluster=None):
    if path is None:
        return
    if not (path.endswith('.xlsx')):
        path += '.xlsx'

    aicdpcpv = average_intra_cluster_distances_per_cluster_per_value

    workbook = xlsxwriter.Workbook(path)
    style_caption = workbook.add_format({'bold': True, 'font_color': 'red', 'left': 2, 'bottom': 1, 'font_size': 15, 'bg_color': '#DDDDDD'})
    style_sum = workbook.add_format({'bold': True, 'font_color': 'blue', 'left': 2, 'bottom': 1, 'bg_color': '#DDDDDD'})
    style_representative = workbook.add_format({'bold': True, 'font_color': 'orange', 'left': 2, 'bottom': 1, 'bg_color': '#DDDDDD'})
    style_grey = workbook.add_format({'bg_color': '#DDDDDD', 'bottom': 1})
    style_grey_right = workbook.add_format({'right': 2, 'bg_color': '#DDDDDD', 'bottom': 1})
    # style_sums = workbook.add_format({'right': 2, 'bottom': 1})
    # style_value = workbook.add_format({'left': 2})
    # style_occurrence = workbook.add_format({'right': 2, 'font_color': 'grey'})

    style_val = workbook.add_format()
    style_val_right = workbook.add_format({'right': 2})
    style_val_left = workbook.add_format({'left': 2})

    sheet1 = workbook.add_worksheet("Cluster_Original")

    column_offset = 1
    label_column = 0

    row_offset = 4 if comp_to_normal_map is None else 3
    caption_row = 1
    original_row = 2
    representative_row = 3

    sheet1.write(original_row, label_column, "#original", style_sum)
    sheet1.set_column(0, label_column, 14)

    noise_unique, noise_count = get_sorted_unique_values_counts(noise)
    has_noise = len(noise_unique) > 0

    sheet1.write(caption_row, label_column, "", style_grey)

    if has_noise:
        sheet1.write(caption_row, column_offset, "Noise", style_caption)
        sheet1.write(caption_row, column_offset + 1, "", style_grey)
        sheet1.write_number(original_row, column_offset, len(noise), style_sum)
        sheet1.write(original_row, column_offset + 1, "", style_grey_right)

        write_list_to_sheet(sheet1, row_offset, column_offset, noise_unique, style_val_left)
        write_list_to_sheet(sheet1, row_offset, column_offset + 1, noise_count, style_val_right, True)
        sheet1.conditional_format(original_row, column_offset + 1, row_offset + 1 + len(noise_count), column_offset + 1,
                                  {'type': 'data_bar'})
        sheet1.set_column(1, column_offset, 15)
        sheet1.set_column(2, column_offset + 1, 6)
        column_offset += 2

    if comp_to_normal_map is None:
        sheet1.write(representative_row, label_column, "representative", style_representative)

    cluster_sizes = list(map(len, clusters))
    cluster_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(clusters))), cluster_sizes)

    for i, v in enumerate(cluster_indices_sorted):
        name = "Cluster " + str(i + 1)
        sheet1.write(caption_row, i * 2 + column_offset, name, style_caption)
        sheet1.write(caption_row, i * 2 + column_offset + 1, "", style_grey_right)
        sheet1.write_number(original_row, i * 2 + column_offset, cluster_counts_sorted[i], style_sum)
        sheet1.write(original_row, i * 2 + column_offset + 1, "", style_grey_right)

        cluster_unique, cluster_count = get_sorted_unique_values_counts(clusters[v])

        if comp_to_normal_map is None:
            sheet1.write(representative_row, i * 2 + column_offset, cluster_unique[0], style_representative)
            sheet1.write(representative_row, i * 2 + column_offset + 1, "", style_grey_right)

        sheet1.set_column(row_offset + i * 2, column_offset + i * 2, 15)
        sheet1.set_column(row_offset + 1 + i * 2, column_offset + 1 + i * 2, 6)

        write_list_to_sheet(sheet1, row_offset, i * 2 + column_offset, cluster_unique, style_val_left)
        write_list_to_sheet(sheet1, row_offset, i * 2 + column_offset + 1, cluster_count, style_val_right, True)
        sheet1.conditional_format(row_offset, i * 2 + column_offset + 1, row_offset + 1 + len(cluster_count), i * 2 + 4, {'type': 'data_bar'})
    sheet1.conditional_format(original_row, column_offset, original_row, 3 + 2 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#63C384'})

    if comp_to_normal_map is not None:

        sheet2 = workbook.add_worksheet("Cluster_Repr")

        noise_repr, noise_count = get_sorted_representatives_counts(comp_to_normal_map, noise_compressed)
        has_noise = len(noise_unique) > 0

        column_offset = 1

        sheet2.write(2, 0, "#original", style_sum)
        sheet2.write(3, 0, "#abstracted", style_sum)
        sheet2.set_column(0, 0, 14)

        sheet2.write(1, 0, "", style_grey)

        if has_noise:
            sheet2.write(1, column_offset, "Noise", style_caption)
            sheet2.write(1, column_offset + 1, "", style_grey)
            sheet2.write_number(2, column_offset, len(noise_compressed), style_sum)
            sheet2.write(2, column_offset + 1, "", style_grey_right)
            sheet2.write_number(3, column_offset, len(noise), style_sum)
            sheet2.write(3, column_offset + 1, "", style_grey_right)
            write_list_to_sheet(sheet2, 4, column_offset, noise_repr, style_val_left)
            write_list_to_sheet(sheet2, 4, column_offset + 1, noise_count, style_val_right, True)
            sheet2.conditional_format(4, column_offset + 1, 3 + len(noise_count), column_offset + 1, {'type': 'data_bar'})
            sheet2.set_column(1, column_offset, 15)
            sheet2.set_column(2, column_offset + 1, 6)
            column_offset += 2

        cluster_compressed_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(clusters_compressed))), cluster_sizes)

        for i, v in enumerate(cluster_compressed_indices_sorted):
            name = "Cluster " + str(i + 1)
            sheet2.write(1, i * 2 + column_offset, name, style_caption)
            sheet2.write(1, i * 2 + column_offset + 1, "", style_grey_right)
            sheet2.write_number(2, i * 2 + column_offset, cluster_counts_sorted[i], style_sum)
            sheet2.write(2, i * 2 + column_offset + 1, "", style_grey_right)
            sheet2.write_number(3, i * 2 + column_offset, len(clusters_compressed[v]), style_sum)
            sheet2.write(3, i * 2 + column_offset + 1, "", style_grey_right)
            sheet2.set_column(3 + i * 2, column_offset + i * 2, 15)
            sheet2.set_column(4 + i * 2, column_offset + 1 + i * 2, 6)
            cluster_repr, cluster_count = get_sorted_representatives_counts(comp_to_normal_map, clusters_compressed[v])
            write_list_to_sheet(sheet2, 4, i * 2 + column_offset, cluster_repr, style_val_left)
            write_list_to_sheet(sheet2, 4, i * 2 + column_offset + 1, cluster_count, style_val_right, True)
            sheet2.conditional_format(4, i * 2 + column_offset + 1, 4 + len(cluster_count), i * 2 + column_offset + 1, {'type': 'data_bar'})
        sheet2.conditional_format(2, 1, 2, column_offset + 2 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#63C384'})
        sheet2.conditional_format(3, 1, 3, column_offset + 2 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#C3C365'})

    if comp_to_normal_map is not None:

        sheet3 = workbook.add_worksheet("Cluster_Repr_Dists")

        noise_repr, noise_count = get_sorted_representatives_counts(comp_to_normal_map, noise_compressed)
        has_noise = len(noise_unique) > 0

        column_offset = 1

        sheet3.write(2, 0, "#original", style_sum)
        sheet3.write(3, 0, "#abstracted", style_sum)
        sheet3.write(4, 0, "#variance", style_sum)
        sheet3.set_column(0, 0, 14)

        sheet3.write(1, 0, "", style_grey)
        if has_noise:
            sheet3.write(1, column_offset, "Noise", style_caption)
            sheet3.write(1, column_offset + 1, "", style_grey)
            sheet3.write(1, column_offset + 2, "", style_grey_right)
            sheet3.write_number(2, column_offset, len(noise_compressed), style_sum)
            sheet3.write(2, column_offset + 1, "", style_grey)
            sheet3.write(2, column_offset + 2, "", style_grey_right)
            sheet3.write_number(3, column_offset, len(noise), style_sum)
            sheet3.write(3, column_offset + 1, "", style_grey)
            sheet3.write(3, column_offset + 2, "", style_grey_right)
            sheet3.write(4, column_offset, "", style_sum)
            sheet3.write(4, column_offset + 1, "", style_grey)
            sheet3.write(4, column_offset + 2, "", style_grey_right)
            sheet3.set_column(1, 1, 15)
            sheet3.set_column(2, 2, 6)
            write_list_to_sheet(sheet3, 5, column_offset, noise_repr, style_val_left)
            write_list_to_sheet(sheet3, 5, column_offset + 1, noise_count, style_val, True)
            sheet3.conditional_format(5, column_offset + 1, 5 + len(noise_count), column_offset + 1, {'type': 'data_bar'})
            column_offset += 3

        cluster_compressed_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(clusters_compressed))), cluster_sizes)

        for i, v in enumerate(cluster_compressed_indices_sorted):
            name = "Cluster " + str(i + 1)
            sheet3.write(1, i * 3 + column_offset, name, style_caption)
            sheet3.write(1, i * 3 + column_offset + 1, "", style_grey)
            sheet3.write(1, i * 3 + column_offset + 2, "", style_grey_right)

            sheet3.write_number(2, i * 3 + column_offset, cluster_counts_sorted[i], style_sum)
            sheet3.write(2, i * 3 + column_offset + 1, "", style_grey)
            sheet3.write(2, i * 3 + column_offset + 2, "", style_grey_right)

            sheet3.write_number(3, i * 3 + column_offset, len(clusters_compressed[v]), style_sum)
            sheet3.write(3, i * 3 + column_offset + 1, "", style_grey)
            sheet3.write(3, i * 3 + column_offset + 2, "", style_grey_right)

            sheet3.write_number(4, i * 3 + column_offset, intra_cluster_distances[v], style_sum)
            sheet3.write(4, i * 3 + column_offset + 1, "", style_grey)
            sheet3.write(4, i * 3 + column_offset + 2, "", style_grey_right)

            sheet3.set_column(4 + i * 3, column_offset + i * 3, 15)
            sheet3.set_column(5 + i * 3, column_offset + 1 + i * 3, 6)
            sheet3.set_column(6 + i * 3, column_offset + 2 + i * 3, 6)

            cluster_repr, cluster_count, cluster_intra = get_sorted_representatives_counts(comp_to_normal_map, clusters_compressed[v], aicdpcpv[v])
            write_list_to_sheet(sheet3, 5, i * 3 + column_offset, cluster_repr, style_val_left)
            write_list_to_sheet(sheet3, 5, i * 3 + column_offset + 1, cluster_count, style_val, True)
            write_list_to_sheet(sheet3, 5, i * 3 + column_offset + 2, cluster_intra, style_val_right)

            sheet3.conditional_format(5, i * 3 + column_offset + 1, 5 + len(cluster_count), i * 3 + column_offset + 1, {'type': 'data_bar'})
            sheet3.conditional_format(5, i * 3 + column_offset + 2, 5 + len(cluster_count), i * 3 + column_offset + 2, {'type': 'data_bar', 'bar_color': '#C36565'})

        sheet3.conditional_format(2, 1, 2, column_offset + 3 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#63C384'})
        sheet3.conditional_format(3, 1, 3, column_offset + 3 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#C3C365'})
        sheet3.conditional_format(4, 1, 4, column_offset + 3 * len(cluster_indices_sorted), {'type': 'data_bar', 'bar_color': '#666666'})

    if comp_to_normal_map is not None:
        sheet4 = workbook.add_worksheet("Mapping_Original_Repr")
        sheet4.write(2, 0, "#original", style_sum)
        sheet4.set_column(0, 0, 14)

        sheet4.write(1, 0, "", style_grey)
        sheet4.set_column(1, 1, 15)
        sheet4.set_column(2, 2, 6)

        row_offset = 2
        row_offset += 1
        sheet4.write(row_offset, 0, "representative", style_representative)
        row_offset += 1

        cluster_sizes = list(map(len, simple_cluster))
        cluster_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(simple_cluster))), cluster_sizes)

        for i, v in enumerate(cluster_indices_sorted):
            sheet4.write(1, i * 2 + 1, "", style_caption)
            sheet4.write(1, i * 2 + 2, "", style_grey_right)
            sheet4.write_number(2, i * 2 + 1, cluster_counts_sorted[i], style_sum)
            sheet4.write(2, i * 2 + 2, "", style_grey_right)

            representative = simple_cluster[v][0]
            cluster_unique, cluster_count = get_sorted_unique_values_counts(simple_cluster[v])

            row_offset = 2
            row_offset += 1
            sheet4.write(row_offset, i * 2 + 1, representative, style_representative)
            sheet4.write(row_offset, i * 2 + 2, "", style_grey_right)

            row_offset += 1
            sheet4.set_column(row_offset + i * 2, 1 + i * 2, 15)
            sheet4.set_column(row_offset + 1 + i * 2, 2 + i * 2, 6)

            write_list_to_sheet(sheet4, row_offset, i * 2 + 1, cluster_unique, style_val_left)
            write_list_to_sheet(sheet4, row_offset, i * 2 + 2, cluster_count, style_val_right, True)
            sheet4.conditional_format(row_offset, i * 2 + 2, row_offset + 1 + len(cluster_count), i * 2 + 2,
                                      {'type': 'data_bar'})
        sheet4.conditional_format(2, 1, 2, 3 + 2 * len(cluster_indices_sorted),
                                  {'type': 'data_bar', 'bar_color': '#63C384'})

    workbook.close()


def get_abstracted_from_original(comp_to_normal_map, first_noise, first_noise_abstracted):
    for j, abs in enumerate(comp_to_normal_map.keys()):
        if first_noise in comp_to_normal_map[abs]:
            first_noise_abstracted = abs
    return first_noise_abstracted


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
