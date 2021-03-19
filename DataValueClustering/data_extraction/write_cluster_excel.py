import xlsxwriter


def cluster_to_excel(path, clusters, noise, clusters_compressed, noise_compressed, comp_to_normal_map, cluster_sizes,
                         noise_size, cluster_sizes_compressed, noise_size_compressed):
    if not (path.endswith('.xlsx')):
        path += '.xlsx'

    workbook = xlsxwriter.Workbook(path)
    style_caption = workbook.add_format({'bold': True, 'font_color': 'red', 'left': 2})
    style_sum = workbook.add_format({'bold': True, 'font_color': 'blue', 'left': 2, 'bottom': 1})
    style_sum_right = workbook.add_format({'right': 2, 'bottom': 1})
    style_value = workbook.add_format({'left': 2})
    style_occurrence = workbook.add_format({'right': 2, 'font_color': 'grey'})

    sheet1 = workbook.add_worksheet("Cluster_Original")
    sheet1.write(2, 0, "#original", style_sum)
    sheet1.set_column(0, 0, 12)

    sheet1.write(1, 1, "Noise", style_caption)
    sheet1.write(2, 1, str(len(noise)), style_sum)
    sheet1.write(2, 2, "", style_sum_right)
    sheet1.set_column(2, 2, 6)
    noise_unique, noise_count = get_sorted_unique_values_counts(noise)
    write_list_to_sheet(sheet1, 3, 1, noise_unique, style_value)
    write_list_to_sheet(sheet1, 3, 2, noise_count, style_occurrence)

    cluster_sizes = list(map(len, clusters))
    cluster_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(clusters))), cluster_sizes)

    for i in cluster_indices_sorted:
        name = "Cluster " + str(i + 1)
        sheet1.write(1, i * 2 + 3, name, style_caption)
        sheet1.write(1, i * 2 + 4, "", style_occurrence)
        sheet1.write(2, i * 2 + 3, str(cluster_counts_sorted[i]), style_sum)
        sheet1.write(2, i * 2 + 4, "", style_sum_right)
        sheet1.set_column(3 + i * 2, 3 + i * 2, 15)
        sheet1.set_column(4 + i * 2, 4 + i * 2, 6)
        cluster_unique, cluster_count = get_sorted_unique_values_counts(clusters[i])
        write_list_to_sheet(sheet1, 3, i * 2 + 3, cluster_unique, style_value)
        write_list_to_sheet(sheet1, 3, i * 2 + 4, cluster_count, style_occurrence)

    if not comp_to_normal_map is None:

        sheet2 = workbook.add_worksheet("Cluster_Repr")
        sheet2.write(2, 0, "#compressed", style_sum)
        sheet2.write(3, 0, "#original", style_sum)
        sheet2.set_column(0, 0, 12)

        sheet2.write(1, 1, "NOISE", style_caption)
        sheet2.write(2, 1, str(len(noise_compressed)), style_sum)
        sheet2.write(2, 2, "", style_sum_right)
        sheet2.write(3, 1, str(len(noise)), style_sum)
        sheet2.write(3, 2, "", style_sum_right)
        sheet2.set_column(1, 1, 15)
        sheet2.set_column(2, 2, 6)
        noise_repr, noise_count = get_sorted_representatives_counts(comp_to_normal_map, noise_compressed)
        write_list_to_sheet(sheet2, 4, 1, noise_repr, style_value)
        write_list_to_sheet(sheet2, 4, 2, noise_count, style_occurrence)

        cluster_compressed_indices_sorted, cluster_counts_sorted = sort_values_counts(list(range(0, len(clusters_compressed))), cluster_sizes)

        for i in cluster_compressed_indices_sorted:
            name = "Cluster " + str(i + 1)
            sheet2.write(1, i * 2 + 3, name, style_caption)
            sheet2.write(1, i * 2 + 4, "", style_occurrence)
            sheet2.write(2, i * 2 + 3, str(len(clusters_compressed[i])), style_sum)
            sheet2.write(2, i * 2 + 4, "", style_sum_right)
            sheet2.write(3, i * 2 + 3, str(cluster_counts_sorted[i]), style_sum)
            sheet2.write(3, i * 2 + 4, "", style_sum_right)
            sheet2.set_column(3 + i * 2, 3 + i * 2, 15)
            sheet2.set_column(4 + i * 2, 4 + i * 2, 6)
            cluster_repr, cluster_count = get_sorted_representatives_counts(comp_to_normal_map, clusters_compressed[i])
            write_list_to_sheet(sheet2, 4, i * 2 + 3, cluster_repr, style_value)
            write_list_to_sheet(sheet2, 4, i * 2 + 4, cluster_count, style_occurrence)

    workbook.close()


def get_sorted_representatives_counts(comp_to_normal_map, values_compressed):
    noise_repr = get_repr_list(values_compressed, comp_to_normal_map)
    noise_count = get_compressed_count(values_compressed, comp_to_normal_map)
    return sort_values_counts(noise_repr, noise_count)


def sort_values_counts(values, counts):
    cluster_unique_count_dict = dict(zip(values, counts))
    d_sorted = {k: v for k, v in sorted(cluster_unique_count_dict.items(), key=lambda item: item[1], reverse=True)}
    return list(d_sorted.keys()), list(d_sorted.values())


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


def write_list_to_sheet(sheet, x, y, list, style = None):
    for i, v in enumerate(list):
        sheet.write(x + i, y, v, style)


def get_repr_list(values_compressed, comp_to_normal_map):
    result = []
    for i in values_compressed:
        result.append(get_repr(i, comp_to_normal_map))
    return result


def get_repr(value_compressed, comp_to_normal_map):
    try:
        return comp_to_normal_map[value_compressed][0]
    except:
        return ""


if __name__ == '__main__':
    path = "file.xlsx"
    clusters = [
        ['value1', 'value2', 'value3', 'value4', 'value1', 'value2'],
        ['value5', 'value6']
    ]
    noise = ['value7']
    clusters_compressed = [
        ['key1', 'key2'],
        ['key3']
    ]
    noise_compressed = ['key4']
    comp_to_normal_map = {'key1': ['value1', 'value2'], 'key2': ['value3', 'value4'], 'key3': ['value5', 'value6'],
                          'key4': ['value7']}

    cluster_to_excel(path, clusters, noise, clusters_compressed, noise_compressed, comp_to_normal_map)
