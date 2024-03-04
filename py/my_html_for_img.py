""" Exports img_html. """

import my_html
import my_utils

def html_for_imgs(record):
    """ Return HTML for image or images in record. """
    if 'img' in record:
        return [_html_for_single_img(record['img'])]
    if 'imgs' in record:
        imgs_items = record['imgs'].items()
        list_of_lists = list(map(_html_for_imgs_item, imgs_items))
        return my_utils.sum_of_lists(list_of_lists)
    return []


def _html_for_single_img(img_path):
    img_element = my_html.img({'src': f'../img/{img_path}'})
    return my_html.para(img_element)


def _html_for_imgs_item(imgs_item):
    img_label, img_path = imgs_item
    return [
        my_html.para(img_label),
        _html_for_single_img(img_path)]
