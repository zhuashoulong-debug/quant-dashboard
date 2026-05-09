from __future__ import annotations


VALIDATION_VIEWS = [
    {
        "id": "overview",
        "label": "总览",
        "description": "把旧 A1/A2/A3 的关键结论压成一屏，先判断这根 K 卡在哪一层。",
        "fields": [
            {"key": "pctb", "label": "PCTB", "kind": "number", "digits": 3},
            {"key": "current_width_ratio", "label": "宽比", "kind": "number", "digits": 3},
            {"key": "effective_cross_1", "label": "有效上穿1", "kind": "bool"},
            {"key": "new_breakthrough_background", "label": "新版突破背景", "kind": "bool"},
            {"key": "bullish_strong", "label": "阳强", "kind": "bool"},
            {"key": "long_upper_shadow", "label": "长上", "kind": "bool"},
            {"key": "large_amount", "label": "放额", "kind": "bool"},
            {"key": "structure_break_up", "label": "构上", "kind": "bool"},
        ],
    },
    {
        "id": "base",
        "label": "基础",
        "description": "合并旧 A1：K线质量、成交额强度和结构突破，不在图上铺满连续线。",
        "fields": [
            {"key": "body_ratio", "label": "实体占比", "kind": "number", "digits": 3},
            {"key": "upper_shadow_ratio", "label": "上影占比", "kind": "number", "digits": 3},
            {"key": "close_position", "label": "收盘位置", "kind": "number", "digits": 3},
            {"key": "amount_ratio", "label": "额比", "kind": "number", "digits": 3},
            {"key": "warm_amount", "label": "温额", "kind": "bool"},
            {"key": "large_amount", "label": "放额", "kind": "bool"},
            {"key": "huge_amount", "label": "巨额", "kind": "bool"},
            {"key": "structure_break_up", "label": "构上", "kind": "bool"},
        ],
    },
    {
        "id": "background",
        "label": "背景",
        "description": "合并旧 A2/A3a2/A3b2b1：挤压、收缩、迟发、宽度挡和突破背景。",
        "fields": [
            {"key": "squeeze", "label": "当根挤压", "kind": "bool"},
            {"key": "near_squeeze", "label": "近挤", "kind": "bool"},
            {"key": "new_effective_squeeze", "label": "新版有效挤压", "kind": "bool"},
            {"key": "contraction_process", "label": "收缩过程", "kind": "bool"},
            {"key": "new_true_contraction", "label": "新版真正收缩", "kind": "bool"},
            {"key": "new_late_squeeze", "label": "迟发挤压背景", "kind": "bool"},
            {"key": "width_block", "label": "宽度挡", "kind": "bool"},
            {"key": "old_breakthrough_background", "label": "旧突破背景", "kind": "bool"},
            {"key": "new_breakthrough_background", "label": "新突破背景", "kind": "bool"},
        ],
    },
    {
        "id": "source",
        "label": "上穿来源",
        "description": "合并旧 A3a1/A3a3/A3b2a 当前已搬部分：从上穿到温/暴/极来源。",
        "fields": [
            {"key": "manual_cross", "label": "手工上穿", "kind": "bool"},
            {"key": "cross_pctb_1", "label": "CROSS上穿", "kind": "bool"},
            {"key": "shallow_recross", "label": "浅绕回过滤", "kind": "bool"},
            {"key": "effective_cross_1", "label": "有效上穿1", "kind": "bool"},
            {"key": "warm_up_base", "label": "温上基", "kind": "bool"},
            {"key": "warm_up", "label": "温上", "kind": "bool"},
            {"key": "violent_up", "label": "暴上", "kind": "bool"},
            {"key": "violent_up_risk", "label": "暴上险", "kind": "bool"},
            {"key": "extreme_up", "label": "极上", "kind": "bool"},
            {"key": "extreme_up_risk", "label": "极上险", "kind": "bool"},
        ],
    },
    {
        "id": "blue_yellow",
        "label": "蓝黄",
        "description": "合并旧 A3b2：判断同样上穿来源应进入蓝背景，还是退到黄色来源。",
        "fields": [
            {"key": "previous_width_ratio", "label": "启动前宽比", "kind": "number", "digits": 3},
            {"key": "pre_start_relative_high", "label": "启动前相高", "kind": "number", "digits": 3},
            {"key": "blue_compression_quality", "label": "蓝压缩质量", "kind": "bool"},
            {"key": "blue_squeeze_background", "label": "蓝挤压背景", "kind": "bool"},
            {"key": "blue_contraction_background", "label": "蓝收缩背景", "kind": "bool"},
            {"key": "blue_quality_background", "label": "蓝优质背景", "kind": "bool"},
            {"key": "blue_warm_source", "label": "蓝温源", "kind": "bool"},
            {"key": "blue_violent_source", "label": "蓝暴源", "kind": "bool"},
            {"key": "yellow_warm_source", "label": "黄温源", "kind": "bool"},
            {"key": "yellow_violent_source", "label": "黄暴源", "kind": "bool"},
        ],
    },
    {
        "id": "effective",
        "label": "有效层",
        "description": "A3b2 有效层：观察蓝/黄来源进入有效信号前，被首扩、速度、黄色许可等条件压制的位置。",
        "fields": [
            {"key": "first_expand_start", "label": "首扩启", "kind": "bool"},
            {"key": "speed_valid", "label": "速有效", "kind": "bool"},
            {"key": "speed_after_running", "label": "速后运行", "kind": "bool"},
            {"key": "yellow_display_permission", "label": "黄显示许可", "kind": "bool"},
            {"key": "yellow_fresh_permission", "label": "黄新鲜许可", "kind": "bool"},
            {"key": "blue_warm_valid", "label": "蓝温有效", "kind": "bool"},
            {"key": "blue_violent_valid", "label": "蓝暴有效", "kind": "bool"},
            {"key": "yellow_warm_valid", "label": "黄温有效", "kind": "bool"},
            {"key": "yellow_violent_valid", "label": "黄暴有效", "kind": "bool"},
            {"key": "effective_start_signal_pre", "label": "有效启动预", "kind": "bool"},
        ],
    },
]


def validation_view_ids() -> list[str]:
    return [view["id"] for view in VALIDATION_VIEWS]
