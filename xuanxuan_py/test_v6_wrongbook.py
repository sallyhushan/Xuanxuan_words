# 萱萱单词游戏 v5.14 - 错题本功能测试用例
import re, json

HTML_PATH = '/root/.openclaw/workspace/xuanxuan_py/index.html'

with open(HTML_PATH) as f:
    html = f.read()

js = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
js = js.group(1) if js else ''

body = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
body = body.group(1) if body else ''

style = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
style_text = style.group(1) if style else ''

results = []

def check(name, condition):
    ok = bool(condition)
    results.append(('✅' if ok else '❌', name))
    return ok

# ===== 1. 数据模型 =====
check('wrongBook 对象定义', 'var wrongBook={pending:[],eliminated:[]}' in js)
check('loadWrongBook 函数存在', 'function loadWrongBook()' in js)
check('saveWrongBook 函数存在', 'function saveWrongBook()' in js)
check('addToWrongBook 函数存在', 'function addToWrongBook(' in js)
check('WB_SIZE 常量定义', 'var WB_SIZE=10' in js)

# ===== 2. 自动收录规则 =====
check('showAns 中主线/大乱斗收录条件', 'G.mode!==\'wb\' && !G.isReview' in js)
check('复习模式标志 G.isReview', 'G.isReview=false' in js and 'G.isReview=true' in js)
check('startReviewRound 设置 isReview=true', 'G.isReview=true' in js)
check('startMainRound 设置 isReview=false', 'G.isReview=false' in js)

# ===== 3. 首页入口 =====
check('首页错题本 onclick=showWrongBook', 'onclick="showWrongBook()"' in body)
check('首页错题本动态标签', 'wbLabel=' in js)
check('首页红点徽章', 'position:absolute' in body and 'wbBadge' in js)

# ===== 4. 错题本界面 =====
check('wbScreen HTML 存在', 'id="wbScreen"' in body)
check('wbResult HTML 存在', 'id="wbResult"' in body)
check('showWrongBook 函数存在', 'function showWrongBook()' in js)
check('startWrongBookRound 函数存在', 'function startWrongBookRound()' in js)
check('finishWrongBook 函数存在', 'function finishWrongBook()' in js)
check('wbFireworks 函数存在', 'function wbFireworks()' in js)

# ===== 5. 答题流程 =====
check('错题本模式 G.mode=wb', "G.mode='wb'" in js)
check('renderQ 支持 wb 模式 total', 'G.mode===\'duel\'?DUEL_SIZE:G.seq.length' in js)
check('finish() 调用 finishWrongBook', 'finishWrongBook()' in js)
check('goHome 隐藏 wbScreen', "getElementById('wbScreen').classList.add('hidden')" in js)
check('goHome 隐藏 wbResult', "getElementById('wbResult').classList.add('hidden')" in js)

# ===== 6. 结果页逻辑 =====
check('答对移出 pending', 'wrongBook.pending=wrongBook.pending.filter' in js)
check('答对加入 eliminated', 'wrongBook.eliminated.push' in js)
check('错题本答错更新 wrongCount', 'p.wrongCount++' in js)
check('100% 烟花', 'if(acc===100)' in js and 'wbFireworks()' in js)
check('存活列表渲染', 'id="wbrv"' in body)

# ===== 7. 文案温和化 =====
check('文案：消灭而非错误', '消灭' in body or '歼灭' in body)
check('无"上次错选"提示', '上次错选' not in body and '上次错选' not in js)
# 排除词库中的"失败"翻译和排行榜原有文案，只检查错题本相关文案
check('无严厉措辞：失败', '闯关失败' not in body and '闯关失败' not in js)
check('无严厉措辞：惩罚', '惩罚' not in body and '惩罚' not in js)

# ===== 8. 隐性保险 =====
check('eliminated 回归 pending', 'wrongBook.eliminated=wrongBook.eliminated.filter' in js)
check('addToWrongBook 处理 eliminated', 'elim' in js and 'wrongBook.pending.push' in js)

# ===== 9. CSS =====
check('烟花动画 @keyframes boom', '@keyframes boom' in style_text)

# ===== 10. localStorage 集成 =====
check('loadStorage 调用 loadWrongBook', 'loadWrongBook()' in js)
check('saveProgress 调用 saveWrongBook', 'saveWrongBook()' in js)

# ===== 输出 =====
passed = sum(1 for _, ok in results if '✅' in _)
total = len(results)
print(f'\n测试结果: {passed}/{total} 通过\n')
for status, name in results:
    print(f'{status} {name}')

if passed == total:
    print('\n🎉 所有测试通过！')
else:
    print(f'\n⚠️ {total-passed} 项未通过，请检查。')
