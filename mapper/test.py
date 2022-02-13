import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "map.settings")
django.setup()

import pandas as pd
from mapper.models import RELATION

import pyecharts.options as opts
from pyecharts.charts import Line

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType

c = (
    Geo()
    .add_schema(maptype="china")
    .add(
        "",
        [("广州", 55), ("北京", 66), ("杭州", 77), ("重庆", 88)],
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
    .add(
        "geo",
        [("广州", "上海"), ("广州", "北京"), ("广州", "杭州"), ("广州", "重庆")],
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="blue"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Lines"))
    .render("geo_lines.html")
)

