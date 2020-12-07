import sys
import csv
import re
import numpy as np
import pandas as pd

maxInt = sys.maxsize

while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)


def get_article_length_in_byte(s):
    return len(s.encode('utf-8'))


def get_ref_tag_count(s):
    s = s.replace('\n', ' ')
    single_ref = re.findall(r'<\s*ref[^>]*/>', s, re.IGNORECASE)
    double_ref = re.findall(r'<\s*ref[^>/]*>.*?<\s*/\s*ref\s*>', s, re.IGNORECASE)
    ref_name_list = []
    tmp = 0
    for x in single_ref+double_ref:
        if x in single_ref:
            if re.findall(r'<\s*[Rr]eferences\s*/>', x):
                continue
            name = re.findall(r'<\s*ref[^>]*name\s*=(.*?)/>', x, re.IGNORECASE)
        else:
            for sr in single_ref:
                if sr in x:
                    x = x.replace(sr, ' ')
            for dr in double_ref:
                if dr == x:
                    continue
                if dr in x:
                    x = x.replace(dr, ' ')
            name = re.findall(r'<\s*ref[^>]*name\s*=(.*?)>', x, re.IGNORECASE)
        if len(name) > 1:
            # print(name)
            # raise ValueError(f'name length: {len(name)}')
            ref_name_list.append(name[0].replace(' ', '').replace('"', '').replace('\'', '').replace('”', ''))
        else:
            if len(name) == 0:
                ref_name_list.append(tmp)
                tmp += 1
            else:
                ref_name_list.append(name[0].replace(' ', '').replace('"', '').replace('\'', '').replace('”', ''))
    return len(np.unique(ref_name_list))


def get_refTag_count(s):
    s = s.replace('\n', ' ')
    ref_tag = list()
    for x in ['參考', '参考', '[Rr]efTag', '[Rr]efGT', '参', '參', '[Rr]efGroupTag', '[Rr]efcite', '[Rr]efCite',
              '[Rr]eftag', '考']:
        ref_tag += re.findall(f'{{{{{x}.*?}}}}', s)
    ref_name_list = []
    tmp = 0
    for x in ref_tag:
        while len(re.findall('{{.*?}}', x[1:])):
            x = x.replace(re.findall('{{.*?}}', x[1:])[0], ' ')
        spilt_tag = x.replace('{', '').replace('}', '').split('|')
        name_count = sum([True if re.match('^name', y) else False for y in spilt_tag])
        if name_count == 0:
            ref_name_list.append(tmp)
            tmp += 1
        elif name_count == 1:
            ref_name_list.append(spilt_tag[[True if re.match('^name', y) else False for y in spilt_tag].index(True)])
        else:
            raise ValueError(f'name length: {name_count}')
    return len(np.unique(ref_name_list))


def get_header2_reference_count(s):
    header_list = re.findall('^==[^=]+==', s, re.M)
    target_index = -1
    for i, header in zip(range(len(header_list)), header_list):
        if '参考资料' in header or '参考文献' in header:
            target_index = i
            break
    if target_index == -1:
        return 0
    if target_index != len(header_list)-1:
        s = s[s.index(header_list[target_index]):s.index(header_list[target_index+1])]
    else:
        s = s[s.index(header_list[target_index]):]
    try:
        return s.count('*')
    except ValueError:
        return 0


def get_infobox_check(s):
    if len(re.findall('{{[Ii]nfobox', s)):
        return 1
    else:
        return 0


def get_image_count(s):
    image_file_type_list = ['.jpg', '.jpeg', '.jpe' '.jif', '.jfif', '.jfi', '.png', '.gif', '.webp', '.tiff', '.tif',
                            '.psd', '.raw', '.arw', '.cr2', '.nrw', '.k25', '.bmp', '.dib', '.heif', '.heic', '.ind',
                            '.indd', '.indt', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2', '.svg', '.svgz', '.ai',
                            '.eps']
    total_image_count = 0
    for image_file_type in image_file_type_list:
        total_image_count += len(re.findall(image_file_type, s))
    return total_image_count


def get_wiki_inside_link_count(s):
    return len(re.findall(r'\[\[.*?\]\]', s))


def get_level2_heading_count(s):
    return len(re.findall('^==[^=]+?==', s, re.M))


def get_level3_heading_count(s):
    return len(re.findall('^===[^=]+?===', s, re.M))


def get_category_count(s):
    return len(re.findall(r'\[\[[Cc]ategory.*?\]\]', s))


def get_citation_templates_count(s):
    count = 0
    citation_list = ['[Cc]ite', '[Cc]itation', '[Cc]ite[ _]study']
    for x in citation_list:
        # {{citation needed}} ?
        count += len(re.findall(f'{{{{{x}.*?}}}}', s))
    return count


def get_non_citation_templates_count(s):
    return len(re.findall('{{.*?}}', s)) - get_citation_templates_count(s)


def get_all_feature(s):
    return [get_article_length_in_byte(s), get_header2_reference_count(s), get_refTag_count(s), get_ref_tag_count(s),
            get_wiki_inside_link_count(s), get_citation_templates_count(s), get_non_citation_templates_count(s),
            get_category_count(s), get_image_count(s)/len(s), get_infobox_check(s), get_level2_heading_count(s),
            get_level3_heading_count(s)]


def main():
    #  '甲级條目.csv': 'A'
    content_type_dict = {'典范條目.csv': 'FA', '優良條目.csv': 'GA', '乙级條目.csv': 'B',
                         '丙级條目.csv': 'C', '初级條目.csv': 'Start', '全部小作品.csv': 'Stub'}
    df = pd.DataFrame(columns=['title', 'content length', 'num_header2_reference', 'num_refTag', 'num_ref_tag',
                               'num_page_links', 'num_cite_temp', 'num_non_cite_templates', 'num_categories',
                               'num_images_length', 'has_infobox', 'num_lv2_headings', 'num_lv3_headings', 'type'])
    for key, value in content_type_dict.items():
        with open(key, newline='', encoding='utf-8') as csv_file:
            spam_reader = csv.reader(csv_file)
            for row in spam_reader:
                if row[0] == 'title':
                    continue
                for x in re.findall('<!--.*?-->', row[1], re.S):
                    row[1] = row[1].replace(x, '')
                features = get_all_feature(row[1])
                features.insert(0, row[0])
                features.append(value)
                df.loc[len(df)] = features
                if len(df) > 100:
                    break
        if len(df) > 100:
            break
    df.to_csv('sample_feature_data.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    main()