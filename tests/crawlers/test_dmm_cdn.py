"""DMM 图片候选地址的构造.

分类目录改写与候选顺序是 DMM 详情页与 r18 dump 共用的契约, 数据驱动用例只覆盖其中的常规分类.
"""

import pytest

from amane.crawlers.sites.dmm import _poster_candidates
from amane.crawlers.sites.dmm_cdn import image_candidates


@pytest.mark.parametrize(
    ("pics_url", "expected"),
    [
        (
            "https://pics.dmm.co.jp/mono/movie/adult/118abf295/118abf295pl.jpg",
            [
                "https://awsimgsrc.dmm.co.jp/pics_dig/mono/movie/118abf295/118abf295pl.jpg",
                "https://pics.dmm.co.jp/mono/movie/adult/118abf295/118abf295pl.jpg",
            ],
        ),
        (
            "https://pics.dmm.co.jp/mono/movie/118abf295r/118abf295rpl.jpg",
            [
                "https://awsimgsrc.dmm.co.jp/pics_dig/mono/movie/118abf295r/118abf295rpl.jpg",
                "https://pics.dmm.co.jp/mono/movie/118abf295r/118abf295rpl.jpg",
            ],
        ),
        (
            "https://pics.dmm.co.jp/digital/video/ssis00497/ssis00497pl.jpg",
            [
                "https://awsimgsrc.dmm.co.jp/pics_dig/digital/video/ssis00497/ssis00497pl.jpg",
                "https://pics.dmm.co.jp/digital/video/ssis00497/ssis00497pl.jpg",
            ],
        ),
        (
            "https://pics.dmm.co.jp/digital/e-book/b044appnt00019/b044appnt00019pl.jpg",
            ["https://pics.dmm.co.jp/digital/e-book/b044appnt00019/b044appnt00019pl.jpg"],
        ),
        ("https://pics.dmm.co.jp/p/ms/top/pic_packing.jpg", ["https://pics.dmm.co.jp/p/ms/top/pic_packing.jpg"]),
        # 已在高清 CDN 上的地址不重复推导.
        (
            "https://awsimgsrc.dmm.co.jp/pics_dig/mono/movie/118abf295/118abf295pl.jpg",
            ["https://awsimgsrc.dmm.co.jp/pics_dig/mono/movie/118abf295/118abf295pl.jpg"],
        ),
        # 段数不足的异常路径仍构造高清候选, 由下载期按序回退.
        (
            "https://pics.dmm.co.jp/mono/movie/broken.jpg",
            [
                "https://awsimgsrc.dmm.co.jp/pics_dig/mono/movie/broken.jpg",
                "https://pics.dmm.co.jp/mono/movie/broken.jpg",
            ],
        ),
    ],
)
def test_image_candidates(pics_url: str, expected: list[str]) -> None:
    assert image_candidates(pics_url) == expected


@pytest.mark.parametrize(
    ("cover_url", "expected"),
    [
        (
            "https://pics.dmm.co.jp/mono/movie/adult/118abf295/118abf295pl.jpg",
            [
                "https://awsimgsrc.dmm.co.jp/pics_dig/mono/movie/118abf295/118abf295ps.jpg",
                "https://pics.dmm.co.jp/mono/movie/adult/118abf295/118abf295ps.jpg",
            ],
        ),
        ("https://pics.dmm.co.jp/mono/movie/adult/118abf295/118abf295ps.jpg", []),
        ("", []),
    ],
)
def test_poster_candidates(cover_url: str, expected: list[str]) -> None:
    assert _poster_candidates(cover_url) == expected
