import xlwt


def cluster_to_excel(path, clusters, noise, clusters_compressed, noise_compressed, comp_to_normal_map):
    if not (path.endswith('.xls')):
        path += '.xls'

    # newfile (path)
    workbook = xlwt.Workbook()
    style_caption = xlwt.easyxf('font: bold 1, color red;')
    style_sum = xlwt.easyxf('font: bold 1, color blue;')

    sheet1 = workbook.add_sheet("Cluster_Original")

    sheet1.write(2, 0, "#original", style_sum)

    sheet1.write(1, 1, "NOISE", style_caption)
    sheet1.write(2, 1, str(len(noise)), style_sum)
    write_list_to_sheet(sheet1, 4, 1, noise)

    for i, cluster in enumerate(clusters):
        name = "Cluster " + str(i + 1)
        sheet1.write(1, i + 2, name, style_caption)
        sheet1.write(2, i + 2, str(len(cluster)), style_sum)
        write_list_to_sheet(sheet1, 4, i + 2, cluster)

    sheet2 = workbook.add_sheet("Cluster_Repr")

    sheet2.write(2, 0, "#compressed", style_sum)
    sheet2.write(3, 0, "#original", style_sum)

    sheet2.write(1, 1, "NOISE", style_caption)
    sheet2.write(2, 1, str(len(noise_compressed)), style_sum)
    sheet2.write(3, 1, str(len(noise)), style_sum)
    noise_repr = get_repr_list(noise_compressed, comp_to_normal_map)
    write_list_to_sheet(sheet2, 5, 1, noise_repr)

    for i, cluster in enumerate(clusters_compressed):
        name = "Cluster " + str(i + 1)
        sheet2.write(1, i + 2, name, style_caption)
        sheet2.write(2, i + 2, str(len(cluster)), style_sum)
        sheet2.write(3, i + 2, str(len(clusters[i])), style_sum)
        cluster_repr = get_repr_list(cluster, comp_to_normal_map)
        write_list_to_sheet(sheet2, 5, i + 2, cluster_repr)

    workbook.save(path)


def write_list_to_sheet(sheet, x, y, list):
    for i, v in enumerate(list):
        sheet.write(x + i, y, v)


def get_repr_list(list, map):
    result = []
    for i in list:
        result.append(get_repr(i, map))
    return result


def get_repr(compressed_value, map):
    try:
        return map[compressed_value][0]
    except:
        return ""


if __name__ == '__main__':
    path = "file.xl"
    clusters = [
        ['value1', 'value2', 'value3', 'value4'],
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
