import streamlit as st
import random
from typing import List, Tuple, Dict

# 页面配置
st.set_page_config(
    page_title="周易卦爻速查",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 样式
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .title {
        text-align: center;
        color: #ffd700;
        font-family: 'Noto Serif SC', serif;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 0.5em;
    }
    
    .subtitle {
        text-align: center;
        color: #aaa;
        font-size: 1em;
        margin-bottom: 2em;
    }
    
    .hexagram-container {
        background: rgba(0,0,0,0.3);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(255,215,0,0.2);
    }
    
    .line-yang {
        background: linear-gradient(90deg, #ffd700, #ffed4a);
        height: 8px;
        border-radius: 4px;
        margin: 12px auto;
        width: 200px;
        box-shadow: 0 0 10px rgba(255,215,0,0.5);
    }
    
    .line-yin {
        display: flex;
        justify-content: space-between;
        width: 200px;
        margin: 12px auto;
    }
    
    .line-yin-part {
        background: linear-gradient(90deg, #888, #aaa);
        height: 8px;
        width: 90px;
        border-radius: 4px;
    }
    
    .line-changing {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    .hexagram-name {
        text-align: center;
        color: #ffd700;
        font-size: 2em;
        font-family: 'Noto Serif SC', serif;
        margin: 20px 0 10px;
    }
    
    .hexagram-symbol {
        text-align: center;
        font-size: 3em;
        color: #fff;
        margin: 10px 0;
    }
    
    .meaning-box {
        background: rgba(255,215,0,0.1);
        border-left: 4px solid #ffd700;
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin: 20px 0;
    }
    
    .meaning-title {
        color: #ffd700;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .meaning-text {
        color: #ddd;
        line-height: 1.8;
        font-size: 1.05em;
    }
    
    .line-detail {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 3px solid #666;
    }
    
    .line-detail.changing {
        border-left-color: #e74c3c;
        background: rgba(231,76,60,0.1);
    }
    
    .line-position {
        color: #ffd700;
        font-weight: bold;
    }
    
    .line-type {
        color: #aaa;
        font-size: 0.9em;
    }
    
    .btn-cast {
        background: linear-gradient(135deg, #8e44ad, #9b59b6) !important;
        color: white !important;
        font-size: 1.2em !important;
        padding: 15px 40px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(142,68,173,0.4) !important;
    }
    
    .info-box {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .trigram-info {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin: 15px 0;
    }
    
    .trigram-box {
        text-align: center;
        padding: 15px 25px;
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    
    .trigram-name {
        color: #ffd700;
        font-size: 1.5em;
        font-weight: bold;
    }
    
    .trigram-symbol {
        font-size: 2em;
        color: #fff;
    }
    
    .trigram-element {
        color: #aaa;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 核心算法 ====================

def yarrow_stalk_divination() -> int:
    """模拟蓍草大衍之数，三变成一爻"""
    stalks = 49
    for _ in range(3):
        left = random.randint(1, stalks - 1)
        right = stalks - left
        right -= 1
        left_rem = left % 4 or 4
        right_rem = right % 4 or 4
        between = 1 + left_rem + right_rem
        stalks -= between
    count_map = {36: 9, 32: 8, 28: 7, 24: 6}
    final = min(count_map.keys(), key=lambda x: abs(x - stalks))
    return count_map[final]

def cast_hexagram() -> List[int]:
    """起六爻（从初爻到上爻）"""
    return [yarrow_stalk_divination() for _ in range(6)]

def line_to_symbol(value: int) -> Tuple[str, str, bool]:
    """返回 (符号, 名称, 是否动爻)"""
    symbols = {
        9: ("⚊", "老阳", True),
        6: ("⚋", "老阴", True),
        7: ("⚊", "少阳", False),
        8: ("⚋", "少阴", False),
    }
    return symbols[value]

def line_to_binary(value: int) -> int:
    return 1 if value in (9, 7) else 0

# 八卦
TRIGRAMS = {
    (1,1,1): ("乾", "☰", "天"),
    (0,0,0): ("坤", "☷", "地"),
    (1,0,0): ("震", "☳", "雷"),
    (0,1,1): ("巽", "☴", "风"),
    (0,1,0): ("坎", "☵", "水"),
    (1,0,1): ("离", "☲", "火"),
    (0,0,1): ("艮", "☶", "山"),
    (1,1,0): ("兑", "☱", "泽"),
}

def get_trigram(bits: Tuple[int, int, int]):
    return TRIGRAMS.get(bits, ("?", "?", "?"))

# 六十四卦
HEXAGRAMS = {
    ("乾","乾"): ("乾", "☰☰", "天天乾", "元亨利贞", "天行健，君子以自强不息"),
    ("坤","坤"): ("坤", "☷☷", "地地坤", "元亨，利牝马之贞", "地势坤，君子以厚德载物"),
    ("坤","震"): ("豫", "☷☳", "地雷豫", "利建侯行师", "雷出地奋，豫。先王以作乐崇德"),
    ("坎","震"): ("屯", "☵☳", "水雷屯", "元亨利贞", "云雷屯，君子以经纶"),
    ("艮","坎"): ("蒙", "☶☵", "山水蒙", "亨", "山下出泉，蒙。君子以果行育德"),
    ("乾","坎"): ("需", "☰☵", "天水需", "有孚", "云上于天，需。君子以饮食宴乐"),
    ("坎","乾"): ("讼", "☵☰", "水天讼", "有孚", "天与水违行，讼。君子以作事谋始"),
    ("坤","坎"): ("师", "☷☵", "地水师", "贞丈人吉", "地中有水，师。君子以容民畜众"),
    ("坎","坤"): ("比", "☵☷", "水地比", "吉", "地上有水，比。先王以建万国，亲诸侯"),
    ("乾","巽"): ("小畜", "☰☴", "天风小畜", "亨", "风行天上，小畜。君子以懿文德"),
    ("兑","乾"): ("履", "☱☰", "泽天履", "履虎尾", "上天下泽，履。君子以辨上下，定民志"),
    ("乾","坤"): ("泰", "☰☷", "天地泰", "小往大来", "天地交，泰。后以财成天地之道"),
    ("坤","乾"): ("否", "☷☰", "地天否", "否之匪人", "天地不交，否。君子以俭德辟难"),
    ("乾","离"): ("同人", "☰☲", "天火同人", "同人于野", "天与火，同人。君子以类族辨物"),
    ("离","乾"): ("大有", "☲☰", "火天大有", "元亨", "火在天上，大有。君子以遏恶扬善"),
    ("艮","坤"): ("谦", "☶☷", "山地谦", "亨", "地中有山，谦。君子以裒多益寡"),
    ("兑","震"): ("随", "☱☳", "泽雷随", "元亨", "泽中有雷，随。君子以向晦入宴息"),
    ("巽","艮"): ("蛊", "☴☶", "风山蛊", "元亨", "山下有风，蛊。君子以振民育德"),
    ("乾","兑"): ("临", "☰☱", "天泽临", "元亨", "泽上有地，临。君子以教思无穷"),
    ("巽","坤"): ("观", "☴☷", "风地观", "盥而不荐", "风行地上，观。先王以省方观民设教"),
    ("离","兑"): ("噬嗑", "☲☱", "火泽噬嗑", "亨", "雷电噬嗑，先王以明罚勅法"),
    ("艮","离"): ("贲", "☶☲", "山火贲", "亨", "山下有火，贲。君子以明庶政"),
    ("艮","乾"): ("大畜", "☶☰", "山天大畜", "利贞", "天在山中，大畜。君子以多识前言往行"),
    ("震","坤"): ("复", "☳☷", "雷地复", "亨", "雷在地中，复。先王以至日闭关"),
    ("乾","震"): ("无妄", "☰☳", "天雷无妄", "元亨", "天下雷行，物与无妄。先王以茂对时"),
    ("坎","坎"): ("坎", "☵☵", "水水坎", "习坎", "水洊至，习坎。君子以常德行，习教事"),
    ("离","离"): ("离", "☲☲", "火火离", "利贞", "明两作，离。大人以继明照于四方"),
    ("兑","巽"): ("中孚", "☱☴", "泽风中孚", "豚鱼吉", "泽上有风，中孚。君子以议狱缓死"),
    ("震","震"): ("震", "☳☳", "雷雷震", "亨", "洊雷，震。君子以恐惧修省"),
    ("艮","艮"): ("艮", "☶☶", "山山艮", "艮其背", "兼山，艮。君子以思不出其位"),
    ("巽","巽"): ("巽", "☴☴", "风风巽", "小亨", "随风，巽。君子以申命行事"),
    ("兑","兑"): ("兑", "☱☱", "泽泽兑", "亨", "丽泽，兑。君子以朋友讲习"),
    ("乾","艮"): ("遁", "☰☶", "天山遁", "亨", "天下有山，遁。君子以远小人"),
    ("坎","巽"): ("井", "☵☴", "水风井", "改邑不改井", "木上有水，井。君子以劳民劝相"),
    ("离","坎"): ("既济", "☲☵", "火水既济", "亨", "水在火上，既济。君子以思患而豫防之"),
    ("坎","离"): ("未济", "☵☲", "水火未济", "亨", "火在水上，未济。君子以慎辨物居方"),
    ("震","离"): ("丰", "☳☲", "雷火丰", "亨", "雷电皆至，丰。君子以折狱致刑"),
    ("离","震"): ("旅", "☲☳", "火雷旅", "小亨", "山上有火，旅。君子以明慎用刑"),
    ("坎","艮"): ("蹇", "☵☶", "水山蹇", "利西南", "山上有水，蹇。君子以反身修德"),
    ("震","坎"): ("解", "☳☵", "雷水解", "利西南", "雷雨作，解。君子以赦过宥罪"),
    ("艮","兑"): ("损", "☶☱", "山泽损", "有孚", "山下有泽，损。君子以惩忿窒欲"),
    ("巽","震"): ("益", "☴☳", "风雷益", "利有攸往", "风雷，益。君子以见善则迁"),
    ("乾","兑"): ("夬", "☰☱", "天泽夬", "扬于王庭", "泽上于天，夬。君子以施禄及下"),
    ("巽","乾"): ("姤", "☴☰", "风天姤", "女壮", "天下有风，姤。后以施命诰四方"),
    ("坤","兑"): ("萃", "☷☱", "地泽萃", "亨", "泽上于地，萃。君子以除戎器"),
    ("巽","坤"): ("升", "☴☷", "风地升", "元亨", "地中生木，升。君子以顺德，积小以高大"),
    ("震","艮"): ("小过", "☳☶", "雷山小过", "亨利贞", "山上有雷，小过。君子以行过乎恭"),
    ("艮","震"): ("颐", "☶☳", "山雷颐", "贞吉", "山下有雷，颐。君子以慎言语"),
    ("兑","坎"): ("困", "☱☵", "泽水困", "亨", "泽无水，困。君子以致命遂志"),
    ("坤","离"): ("明夷", "☷☲", "地火明夷", "利艰贞", "明入地中，明夷。君子以莅众"),
    ("离","坤"): ("晋", "☲☷", "火地晋", "康侯用锡马", "明出地上，晋。君子以自昭明德"),
    ("巽","离"): ("家人", "☴☲", "风火家人", "利女贞", "风自火出，家人。君子以言有物"),
    ("离","巽"): ("睽", "☲☴", "火泽睽", "小事吉", "上火下泽，睽。君子以同而异"),
    ("坤","艮"): ("剥", "☷☶", "地山剥", "不利有攸往", "山附于地，剥。上以厚下安宅"),
    ("兑","离"): ("革", "☱☲", "泽火革", "己日乃孚", "泽中有火，革。君子以治历明时"),
    ("震","兑"): ("归妹", "☳☱", "雷泽归妹", "征凶", "泽上有雷，归妹。君子以永终知敝"),
    ("艮","巽"): ("渐", "☶☴", "风山渐", "女归吉", "山上有木，渐。君子以居贤德善俗"),
    ("兑","艮"): ("咸", "☱☶", "泽山咸", "亨利贞", "山上有泽，咸。君子以虚受人"),
}

LINE_JUDGMENTS = {
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
        5: "九五，屯其膏，小贞吉，大贞凶。",
        6: "上六，乘马班如，泣血涟如。",
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
    bottom_bits = tuple(line_to_binary(l) for l in lines[:3])
    top_bits = tuple(line_to_binary(l) for l in lines[3:])
    
    lower = get_trigram(bottom_bits)
    upper = get_trigram(top_bits)
    
    key = (upper[0], lower[0])
    if key in HEXAGRAMS:
        hname, hsym, hfull, hmeaning, hxiang = HEXAGRAMS[key]
    else:
        hname, hsym, hfull, hmeaning, hxiang = "未知", "??", "??", "请查阅周易原典", ""
    
    changing = [i+1 for i, v in enumerate(lines) if v in (6, 9)]
    
    cname = ""
    if changing:
        changed_lines = lines.copy()
        for i in changing:
            changed_lines[i-1] = 9 if lines[i-1] == 6 else 6
        cb_bits = tuple(line_to_binary(l) for l in changed_lines[:3])
        ct_bits = tuple(line_to_binary(l) for l in changed_lines[3:])
        cl = get_trigram(cb_bits)
        cu = get_trigram(ct_bits)
        ckey = (cu[0], cl[0])
        if ckey in HEXAGRAMS:
            cname = HEXAGRAMS[ckey][0]
    
    return {
        "lines": lines,
        "lower": lower,
        "upper": upper,
        "hexagram": hname,
        "symbol": hsym,
        "full_name": hfull,
        "meaning": hmeaning,
        "xiang": hxiang,
        "changing": changing,
        "changed": cname,
        "judgments": LINE_JUDGMENTS.get(hname, {})
    }

# ==================== 页面内容 ====================

st.markdown('<div class="title">🔮 周易卦爻速查</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">蓍草大衍之数 · 自动排卦 · 卦象解析</div>', unsafe_allow_html=True)

# 起卦按钮
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎲 开始起卦", type="primary", use_container_width=True):
        st.session_state.hexagram = cast_hexagram()
        st.session_state.analyzed = analyze_hexagram(st.session_state.hexagram)

# 显示结果
if 'analyzed' in st.session_state:
    result = st.session_state.analyzed
    
    st.markdown('<div class="hexagram-container">', unsafe_allow_html=True)
    
    # 显示六爻（从上到下）
    positions = ["上爻", "五爻", "四爻", "三爻", "二爻", "初爻"]
    for i in range(5, -1, -1):
        value = result["lines"][i]
        is_changing = value in (6, 9)
        is_yang = value in (9, 7)
        
        if is_yang:
            css_class = "line-yang" + (" line-changing" if is_changing else "")
            st.markdown(f'<div class="{css_class}"></div>', unsafe_allow_html=True)
        else:
            css_class = "line-yin" + (" line-changing" if is_changing else "")
            st.markdown(f'''
                <div class="{css_class}">
                    <div class="line-yin-part"></div>
                    <div class="line-yin-part"></div>
                </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 卦名
    st.markdown(f'<div class="hexagram-name">{result["hexagram"]}卦 {result["symbol"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;color:#aaa;">{result["full_name"]}</div>', unsafe_allow_html=True)
    
    # 上下卦信息
    st.markdown('<div class="trigram-info">', unsafe_allow_html=True)
    st.markdown(f'''
        <div class="trigram-box">
            <div class="trigram-name">{result["upper"][0]}</div>
            <div class="trigram-symbol">{result["upper"][1]}</div>
            <div class="trigram-element">上卦 · {result["upper"][2]}</div>
        </div>
        <div class="trigram-box">
            <div class="trigram-name">{result["lower"][0]}</div>
            <div class="trigram-symbol">{result["lower"][1]}</div>
            <div class="trigram-element">下卦 · {result["lower"][2]}</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 卦义
    st.markdown(f'''
        <div class="meaning-box">
            <div class="meaning-title">📜 卦辞</div>
            <div class="meaning-text">{result["meaning"]}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
        <div class="meaning-box">
            <div class="meaning-title">💡 象曰</div>
            <div class="meaning-text">{result["xiang"]}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # 变卦信息
    if result["changing"]:
        st.markdown(f'''
            <div class="info-box">
                <div style="color:#e74c3c;font-weight:bold;">🔄 变卦</div>
                <div style="color:#ddd;">{result["hexagram"]}卦 → {result["changed"]}卦</div>
                <div style="color:#aaa;font-size:0.9em;">动爻: {', '.join([f'第{x}爻' for x in result["changing"]])}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        # 爻辞
        if result["judgments"]:
            st.markdown('<div class="section-title">📖 动爻爻辞</div>', unsafe_allow_html=True)
            for pos in result["changing"]:
                if pos in result["judgments"]:
                    st.markdown(f'''
                        <div class="line-detail changing">
                            <span class="line-position">{positions[6-pos]}</span>
                            <span class="line-type">动爻</span>
                            <div style="color:#ddd;margin-top:8px;">{result["judgments"][pos]}</div>
                        </div>
                    ''', unsafe_allow_html=True)

# 底部信息
st.markdown("---")
st.markdown("<div style='text-align:center;color:#666;font-size:0.8em;'>基于蓍草大衍之数五十 · 三变成一爻 · 六爻成一卦</div>", unsafe_allow_html=True)
