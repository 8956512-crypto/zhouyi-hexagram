#!/usr/bin/env python3
"""
周易卦爻速查 - 蓍草大衍之数模拟排卦
Hexagram Divination using Yarrow Stalk Method (Dayan)
"""

import sys
import random
import argparse
from typing import List, Tuple, Dict, Optional

# ==================== 蓍草起卦 ====================

def yarrow_stalk_divination() -> int:
    """
    模拟蓍草大衍之数，三变成一爻
    返回: 6(老阴), 7(少阳), 8(少阴), 9(老阳)
    """
    stalks = 49  # 大衍之数五十，其用四十有九
    
    for _ in range(3):
        # 第一变：随机分而为二
        left = random.randint(1, stalks - 1)
        right = stalks - left
        
        # 挂一（从右组取一根置于左手指间）
        right -= 1
        
        # 揲之以四（以四为组数）
        left_rem = left % 4 or 4
        right_rem = right % 4 or 4
        
        # 归奇于扐（指间余数）
        between = 1 + left_rem + right_rem
        stalks -= between
    
    # 三变后蓍草数 → 爻值
    # 36→9(老阳), 32→8(少阴), 28→7(少阳), 24→6(老阴)
    count_map = {36: 9, 32: 8, 28: 7, 24: 6}
    final = min(count_map.keys(), key=lambda x: abs(x - stalks))
    return count_map[final]

def cast_hexagram(lines: List[int] = None) -> List[int]:
    """起六爻（从初爻到上爻）"""
    if lines is None:
        lines = [yarrow_stalk_divination() for _ in range(6)]
    return lines

# ==================== 卦象解析 ====================

def line_value_to_symbol(value: int) -> str:
    """爻值转符号"""
    return {
        9: ("⚊", "老阳", "—", "○"),  # 老阳动变阴
        6: ("⚋", "老阴", "- -", "×"), # 老阴动变阳
        7: ("⚊", "少阳", "—", " "),  # 少阳不动
        8: ("⚋", "少阴", "- -", " "), # 少阴不动
    }[value]

def line_to_binary(value: int) -> int:
    """转二进制：阳=1, 阴=0"""
    return 1 if value in (9, 7) else 0

# 八卦（从初爻到三爻）
TRIGRAMS: Dict[Tuple, Tuple[str, str, str]] = {
    (1,1,1): ("乾", "☰", "天"),
    (0,0,0): ("坤", "☷", "地"),
    (1,0,0): ("震", "☳", "雷"),
    (0,1,1): ("巽", "☴", "风"),
    (0,1,0): ("坎", "☵", "水"),
    (1,0,1): ("离", "☲", "火"),
    (0,0,1): ("艮", "☶", "山"),
    (1,1,0): ("兑", "☱", "泽"),
}

def get_trigram(bits: Tuple[int, int, int]) -> Tuple[str, str, str]:
    return TRIGRAMS.get(bits, ("?", "?", "?"))

# 六十四卦
HEXAGRAMS: Dict[Tuple[str, str], Tuple[str, str, str, str]] = {
    ("乾","乾"): ("乾", "☰☰", "天天乾", "元亨利贞"),
    ("坤","坤"): ("坤", "☷☷", "地地坤", "元亨，利牝马之贞"),
    ("坎","震"): ("屯", "☵☳", "水雷屯", "元亨利贞，勿用有攸往，利建侯"),
    ("艮","坎"): ("蒙", "☶☵", "山水蒙", "亨，匪我求童蒙，童蒙求我"),
    ("乾","坎"): ("需", "☰☵", "天水需", "有孚，光亨，贞吉，利涉大川"),
    ("坎","乾"): ("讼", "☵☰", "水天讼", "有孚窒惕，中吉，终凶"),
    ("坤","坎"): ("师", "☷☵", "地水师", "贞丈人吉，无咎"),
    ("坎","坤"): ("比", "☵☷", "水地比", "吉，原筮元永贞，无咎"),
    ("乾","巽"): ("小畜", "☰☴", "天风小畜", "亨，密云不雨，自我西郊"),
    ("兑","乾"): ("履", "☱☰", "泽天履", "履虎尾，不咥人，亨"),
    ("乾","坤"): ("泰", "☰☷", "天地泰", "小往大来，吉亨"),
    ("坤","乾"): ("否", "☷☰", "地天否", "否之匪人，不利君子贞"),
    ("乾","离"): ("同人", "☰☲", "天火同人", "同人于野，亨，利涉大川"),
    ("离","乾"): ("大有", "☲☰", "火天大有", "元亨"),
    ("艮","坤"): ("谦", "☶☷", "山地谦", "亨，君子有终"),
    ("坤","震"): ("豫", "☷☳", "地雷豫", "利建侯行师"),
    ("兑","震"): ("随", "☱☳", "泽雷随", "元亨利贞，无咎"),
    ("巽","艮"): ("蛊", "☴☶", "风山蛊", "元亨，利涉大川"),
    ("乾","兑"): ("临", "☰☱", "天泽临", "元亨利贞，至于八月有凶"),
    ("巽","坤"): ("观", "☴☷", "风地观", "盥而不荐，有孚颙若"),
    ("离","兑"): ("噬嗑", "☲☱", "火泽噬嗑", "亨，利用狱"),
    ("艮","离"): ("贲", "☶☲", "山火贲", "亨，小利有攸往"),
    ("艮","乾"): ("大畜", "☶☰", "山天大畜", "利贞，不家食吉，利涉大川"),
    ("震","坤"): ("复", "☳☷", "雷地复", "亨，出入无疾，朋来无咎"),
    ("乾","震"): ("无妄", "☰☳", "天雷无妄", "元亨利贞，其匪正有眚"),
    ("坎","坎"): ("坎", "☵☵", "水水坎", "习坎，有孚，维心亨，行有尚"),
    ("离","离"): ("离", "☲☲", "火火离", "利贞，亨，畜牝牛吉"),
    ("兑","巽"): ("中孚", "☱☴", "泽风中孚", "豚鱼吉，利涉大川，利贞"),
    ("震","震"): ("震", "☳☳", "雷雷震", "亨，震来虩虩，笑言哑哑"),
    ("艮","艮"): ("艮", "☶☶", "山山艮", "艮其背，不获其身，行其庭，不见其人，无咎"),
    ("巽","巽"): ("巽", "☴☴", "风风巽", "小亨，利有攸往，利见大人"),
    ("兑","兑"): ("兑", "☱☱", "泽泽兑", "亨，利贞"),
    ("乾","艮"): ("遁", "☰☶", "天山遁", "亨，小利贞"),
    ("坎","巽"): ("井", "☵☴", "水风井", "改邑不改井，无丧无得，往来井井"),
    ("离","坎"): ("既济", "☲☵", "火水既济", "亨小利贞，初吉终乱"),
    ("坎","离"): ("未济", "☵☲", "水火未济", "亨，小狐汔济，濡其尾，无攸利"),
    ("震","离"): ("丰", "☳☲", "雷火丰", "亨，王假之，勿忧，宜日中"),
    ("离","震"): ("旅", "☲☳", "火雷旅", "小亨，旅贞吉"),
    ("坎","艮"): ("蹇", "☵☶", "水山蹇", "利西南，不利东北，利见大人，贞吉"),
    ("震","坎"): ("解", "☳☵", "雷水解", "利西南，无所往，其来复吉"),
    ("艮","兑"): ("损", "☶☱", "山泽损", "有孚，元吉，无咎可贞，利有攸往"),
    ("巽","震"): ("益", "☴☳", "风雷益", "利有攸往，利涉大川"),
    ("乾","兑"): ("夬", "☰☱", "天泽夬", "扬于王庭，孚号有厉，告自邑，不利即戎"),
    ("巽","乾"): ("姤", "☴☰", "风天姤", "女壮，勿用取女"),
    ("坤","兑"): ("萃", "☷☱", "地泽萃", "亨，王假有庙，利见大人，亨利贞"),
    ("巽","坤"): ("升", "☴☷", "风地升", "元亨，用见大人，勿恤，南征吉"),
    ("震","艮"): ("小过", "☳☶", "雷山小过", "亨利贞，可小事，不可大事"),
    ("艮","震"): ("颐", "☶☳", "山雷颐", "贞吉，观颐，自求口实"),
    ("兑","坎"): ("困", "☱☵", "泽水困", "亨，贞大人吉，无咎，有言不信"),
    ("坤","离"): ("明夷", "☷☲", "地火明夷", "利艰贞"),
    ("离","坤"): ("晋", "☲☷", "火地晋", "康侯用锡马蕃庶，昼日三接"),
    ("巽","离"): ("家人", "☴☲", "风火家人", "利女贞"),
    ("离","巽"): ("睽", "☲☴", "火泽睽", "小事吉"),
    ("坤","震"): ("复", "☷☳", "地雷复", "亨，出入无疾，朋来无咎"),
    ("坤","艮"): ("剥", "☷☶", "地山剥", "不利有攸往"),
    ("离","艮"): ("旅", "☲☶", "火山旅", "小亨，旅贞吉"),
    ("兑","离"): ("革", "☱☲", "泽火革", "己日乃孚，元亨利贞，悔亡"),
    ("震","兑"): ("归妹", "☳☱", "雷泽归妹", "征凶，无攸利"),
    ("艮","巽"): ("渐", "☶☴", "风山渐", "女归吉，利贞"),
    ("兑","艮"): ("咸", "☱☶", "泽山咸", "亨利贞，取女吉"),
}

# 爻辞（仅列出常见卦的动爻）
LINE_JUDGMENTS: Dict[str, Dict[int, str]] = {
    "豫": {
        1: "初六，鸣豫，凶。",
        2: "六二，介于石，不终日，贞吉。",
        3: "六三，盱豫悔，迟有悔。",
        4: "六四，由豫，大有得。勿疑朋盍簪。",
        5: "六五，贞疾，乘刚也。恒不死，中未亡也。",
        6: "上六，冥豫成，有渝无咎。",
    },
    "屯": {
        1: "初九，磐桓，利居贞，利建侯。",
        2: "六二，屯如邅如，乘马班如。匪寇婚媾。",
        3: "六三，即鹿无虞，惟入于林中，君子几不如舍。",
        4: "六四，乘马班如，求婚媾，往吉无不利。",
        5: "屯其膏，小贞吉，大贞凶。",
        6: "乘马班如，泣血涟如。",
    },
    "乾": {
        1: "初九，潜龙勿用。",
        2: "九二，见龙在田，利见大人。",
        3: "九三，君子终日乾乾，夕惕若厉，无咎。",
        4: "九四，或跃在渊，无咎。",
        5: "九五，飞龙在天，利见大人。",
        6: "上九，亢龙有悔。",
    },
}

def analyze_hexagram(lines: List[int]) -> Dict:
    """完整解析卦象"""
    # 本卦
    bottom_bits = tuple(line_to_binary(l) for l in lines[:3])
    top_bits = tuple(line_to_binary(l) for l in lines[3:])
    
    lower = get_trigram(bottom_bits)
    upper = get_trigram(top_bits)
    
    key = (upper[0], lower[0])
    if key in HEXAGRAMS:
        hname, hsym, hfull, hmeaning = HEXAGRAMS[key]
    else:
        hname, hsym, hfull, hmeaning = "未知", "??", "??", "请查阅周易原典"
    
    # 变卦
    changing = [i+1 for i, v in enumerate(lines) if v in (6, 9)]
    
    if changing:
        changed_lines = lines.copy()
        for i in changing:
            changed_lines[i-1] = 9 if lines[i-1] == 6 else 6  # 变
        
        cb_bits = tuple(line_to_binary(l) for l in changed_lines[:3])
        ct_bits = tuple(line_to_binary(l) for l in changed_lines[3:])
        cl = get_trigram(cb_bits)
        cu = get_trigram(ct_bits)
        ckey = (cu[0], cl[0])
        if ckey in HEXAGRAMS:
            cname, csym, cfull, _ = HEXAGRAMS[ckey]
        else:
            cname, csym, cfull = "未知", "??", "??"
    else:
        cl = cu = ("无变卦", "", "")
        cname = csym = ""
    
    return {
        "lines": lines,
        "lower_trigram": lower,
        "upper_trigram": upper,
        "hexagram_name": hname,
        "symbol": hsym,
        "full_name": hfull,
        "meaning": hmeaning,
        "changing_lines": changing,
        "changed_hexagram": cname,
        "changed_symbol": csym,
        "line_details": [
            {
                "position": i+1,
                "value": lines[i],
                "symbol": line_value_to_symbol(lines[i]),
                "is_changing": lines[i] in (6, 9)
            }
            for i in range(6)
        ],
        "line_judgments": LINE_JUDGMENTS.get(hname, {})
    }

def display_hexagram(analysis: Dict):
    """终端显示卦象"""
    print("\n" + "━" * 26)
    print("　　周易卦爻速查")
    print("━" * 26)
    
    # 爻象（从上到下）
    positions = ["上爻", "五爻", "四爻", "三爻", "二爻", "初爻"]
    for i in range(5, -1, -1):
        detail = analysis["line_details"][i]
        sym = detail["symbol"]
        change = " ← 动爻!" if detail["is_changing"] else ""
        print(f"{positions[i]} {sym[0]} {sym[1]:5} {change}")
    
    print("━" * 26)
    print(f"\n本卦: {analysis['hexagram_name']}卦 {analysis['symbol']} ({analysis['full_name']})")
    print(f"卦义: {analysis['meaning']}")
    
    if analysis["changing_lines"]:
        print(f"\n变卦: {analysis['changed_hexagram']}卦 {analysis['changed_symbol']}")
        print(f"动爻: {', '.join(str(x) for x in analysis['changing_lines'])}")
    
    judgments = analysis["line_judgments"]
    if judgments:
        print("\n━━━ 动爻爻辞 ━━━")
        for pos in analysis["changing_lines"]:
            if pos in judgments:
                print(f"\n【{positions[6-pos]}】{judgments[pos]}")
    
    print()

def main():
    parser = argparse.ArgumentParser(description="周易卦爻速查 - 蓍草大衍之数模拟排卦")
    parser.add_argument("--lines", "-l", nargs=6, type=int, 
                       metavar("N",), help="指定六爻(6/7/8/9)复现特定卦")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    
    args = parser.parse_args()
    
    lines = cast_hexagram(args.lines) if args.lines else args.lines
    if args.lines and len(args.lines) == 6:
        lines = args.lines
    else:
        lines = cast_hexagram()
    
    analysis = analyze_hexagram(lines)
    
    if args.json:
        import json
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        display_hexagram(analysis)

if __name__ == "__main__":
    main()
