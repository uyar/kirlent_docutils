import re
from functools import partial

from docutils.core import publish_parts


publish_html = partial(publish_parts, writer_name="kirlent_docutils.slides")


PREAMBLE = ".. title:: Document Title\n\n:author: Author\n\n"
SLIDE = "----\n\n%(f)s\n\nSlide Title %(n)d\n=============\n\nContent %(n)d\n\n"


def test_writer_should_wrap_docinfo_in_a_slide():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<section [^>]*\bid="docinfo"[^>]*\bclass="slide"', html["html_body"]) is not None


def test_writer_should_generate_title_heading_in_docinfo_slide():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert '<h1>Document Title</h1>' in html["docinfo"]


def test_writer_should_not_generate_markup_for_transition():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert '<hr' not in html["body"]


def test_writer_should_not_generate_markup_for_field_list():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ":key: val"}))
    assert ('<dl' not in html["body"]) and ('</dl' not in html["body"])


def test_writer_should_not_generate_markup_for_field_name():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ":key: val"}))
    assert ('<dt' not in html["body"]) and ('</dt' not in html["body"])


def test_writer_should_not_generate_markup_for_field_body():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ":key: val"}))
    assert ('<dd' not in html["body"]) and ('</dd' not in html["body"])


def test_writer_should_not_generate_text_for_field_name():
    html = publish_html(PREAMBLE + ":key: val\n")
    assert 'key' not in html["body"]


def test_writer_should_not_generate_text_for_field_body():
    html = publish_html(PREAMBLE + ":key: val\n")
    assert 'val' not in html["body"]


def test_writer_should_wrap_title_in_header():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert '<header>\n<h2>Slide Title 1</h2>\n</header>\n' in html["body"]


def test_writer_should_generate_div_content_for_slide_contents():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert '</header>\n<div class="content"' in html["body"]


def test_writer_should_generate_script_for_rough_notation():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<script defer src=".*\brough-notation\b.*.js"></script>', html["head"]) is not None


def test_writer_should_generate_script_for_annotating_elements():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<script>.*RoughNotation.annotate\(.*</script>', html["head"], re.DOTALL) is not None


def test_writer_should_generate_span_for_underline_annotation_emphasis():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "*>_Tekir_<*\n")
    assert '<span class="annotation annotation-underline">Tekir</span>' in html["body"]


def test_writer_should_generate_span_for_box_annotation_emphasis():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "*>|Tekir|<*\n")
    assert '<span class="annotation annotation-box">Tekir</span>' in html["body"]


def test_writer_should_generate_span_for_circle_annotation_emphasis():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "*>(Tekir)<*\n")
    assert '<span class="annotation annotation-circle">Tekir</span>' in html["body"]


def test_writer_should_generate_span_for_highlight_annotation_emphasis():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "*>!Tekir!<*\n")
    assert '<span class="annotation annotation-highlight">Tekir</span>' in html["body"]


def test_writer_should_generate_span_for_strike_through_annotation_emphasis():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "*>~Tekir~<*\n")
    assert '<span class="annotation annotation-strike-through">Tekir</span>' in html["body"]


def test_writer_should_generate_span_for_crossed_off_annotation_emphasis():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "*>+Tekir+<*\n")
    assert '<span class="annotation annotation-crossed-off">Tekir</span>' in html["body"]


def test_writer_should_generate_span_for_bracket_annotation_emphasis():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "*>[Tekir]<*\n")
    assert '<span class="annotation annotation-bracket">Tekir</span>' in html["body"]


def test_writer_should_not_generate_span_for_regular_emphasis():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "*Tekir*\n")
    assert '<em>Tekir</em>' in html["body"]


def test_writer_should_generate_regular_link_for_reference_without_annotation():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "`Tekir <https://tekir.org/>`_\n")
    assert '<a href="https://tekir.org/">Tekir</a>' in html["body"]
