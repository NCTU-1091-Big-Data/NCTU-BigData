# Final Project Data Preprocess
## Data
* 乙级條目.csv
* 丙级條目.csv
* 甲级條目.csv
* 全部小作品.csv
* 典范條目.csv
* 初级條目.csv
* 優良條目.csv

## Feature
- [X] `content_length` : Article length in bytes
- [X] `lead_length` : Article lead section length in bytes
- [X] `lead_length_ratio` : Lead section length / article length
- [X] `num_header2_reference` : Number of level 2 headings reference.
- [X] `num_refTag` : Number of [refTag](https://zh.wikipedia.org/wiki/Template:RefTag)
- [X] `num_ref_tag` : Number of `<ref>...</ref>`
- [X] `num_page_links` : Number of outlinks to other Wikipedia pages
- [X] `num_cite_temp` : Number of citation templates
- [X] `num_non_cite_templates` : Number of non-citation templates
- [X] `num_categories` : Number of categories linked in the text
- [X] `num_images_length` : Number of images / length of article
- [X] `num_files_length` : Number of files / length of article
- [ ] `info_noise_score` : Information noise score
- [X] `has_infobox` : Article has an infobox or not
- [X] `num_lv2_headings` : Number of level 2 headings
- [X] `num_lv3_headings` : Number of level 3+ headings
- [X] `website_count` : 不重複的外部連結網站數量
- [X] `word_count` : 文章中不重複的詞彙數量

## Type


| 條目品質 | Type |
| -------- | -------- |
| 典范條目 | FA |
| 優良條目 | GA |
| 乙级條目 | B |
| 丙级條目 | C |
| 初级條目 | Start |
| 小作品 | Stub |
