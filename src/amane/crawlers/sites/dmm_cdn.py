"""DMM 图片 CDN 的域名与路径规则, 由 DMM 详情页与 r18 dump 两个来源共用.

两个 CDN 存放同一份文件, 差别只在路径: pics 的 mono 地址在 cid 前多一层被忽略的分类目录
(adult / amateur / japanese), aws 只接受省去该层的规范路径; 其余分类 (e-book 等) 没有 aws 副本.
aws 通常分辨率更高, 但老片与 pics 同尺寸, 少量条目反而更小, 因此候选必须保留 pics 回退.
"""

PICS_CDN = "https://pics.dmm.co.jp"
HIGH_RES_CDN = "https://awsimgsrc.dmm.co.jp/pics_dig"

# aws 有副本的路径前缀; mono 单独处理, 因为它需要改写路径.
_DIGITAL_HIGH_RES_PREFIXES = ("digital/video/", "digital/amateur/")
_MONO_MOVIE_PREFIX = "mono/movie/"


def _canonical_path(rel_path: str) -> str:
    """省去 mono 路径在 cid 前多出的分类目录."""
    segments = rel_path[len(_MONO_MOVIE_PREFIX) :].split("/")
    return f"{_MONO_MOVIE_PREFIX}{'/'.join(segments[-2:])}" if len(segments) > 2 else rel_path


def high_res_url(pics_url: str) -> str | None:
    """pics 绝对地址 → aws 绝对地址; 非 pics 域名或该分类无 aws 副本时返回 None."""
    if not pics_url.startswith(f"{PICS_CDN}/"):
        return None
    rel_path = pics_url[len(PICS_CDN) + 1 :]
    if rel_path.startswith(_MONO_MOVIE_PREFIX):
        return f"{HIGH_RES_CDN}/{_canonical_path(rel_path)}"
    if rel_path.startswith(_DIGITAL_HIGH_RES_PREFIXES):
        return f"{HIGH_RES_CDN}/{rel_path}"
    return None


def image_candidates(pics_url: str) -> list[str]:
    """pics 绝对地址 → 高清候选在前、标准地址兜底的候选列表.

    aws 对不存在的路径返回 404, pics 返回 302 到 now_printing 占位图, 两者都由下载期按序回退.
    """
    high_res = high_res_url(pics_url)
    return [high_res, pics_url] if high_res else [pics_url]
