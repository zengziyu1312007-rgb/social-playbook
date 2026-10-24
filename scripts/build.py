"""Generate the offline site, guide and Skill with Python 3 standard library."""
from pathlib import Path
from collections import Counter
import json, zipfile
R=Path(__file__).resolve().parents[1]
cases=json.loads((R/'data/cases.json').read_text()); sources=json.loads((R/'data/sources.json').read_text()); sm={s['id']:s for s in sources}
assert len(cases)>=100 and len({c['id'] for c in cases})==len(cases)==len({c['title'] for c in cases})
for c in cases:
 for k in ['group','title','context','say','push','reply','check','action','limit']:assert c[k].strip(),(c['id'],k)
 assert all(s in sm for s in c['sources'])
def dump(v):return json.dumps(v,ensure_ascii=False).replace('</','<\\/')
(R/'index.html').write_text((R/'templates/page.html').read_text().replace('__DATA__',dump(cases)).replace('__SOURCES__',dump(sources)))
intro='# 人情世故指南\n\n151 个场景，18 个主题；覆盖 103 个职场场景和 48 个生活场景。先理清自己的选择，再找到说得出口的一句。\n\n每条包括适用情境、开口前判断、第一句、被反问后的下一句、后续动作和判断边界。话术全部独立编写，不是来源文章的原话。资料只支持问题类型或一般原则，不能证明每个场景实际发生、某句话一定有效。\n\n涉及法律、医疗、财务等专业事项，本文只提供沟通参考，专业判断需由相关人员结合地区、时间和具体事实作出。国外机构资料只用于一般沟通和管理原则，不直接套用其法律。\n\n'
def entry(c):
 out=f"## {c['id']} · {c['title']}\n\n"
 for label,k in [('情境','context'),('开口之前','check'),('可以这样说','say'),('对方说','push'),('下一句','reply'),('接下来做什么','action'),('判断边界','limit')]:out+=f"**{label}**：{c[k]}\n\n"
 out+='**依据**：'+('资料启发；场景与话术为独立编写。 '+ '；'.join(f"[{s} {sm[s]['title']}]({sm[s]['url']})（{sm[s]['verification']}）" for s in c['sources']) if c['sources'] else '原创建议，未声称对应某个真实事件。')+'\n\n'
 return out
source_text='# 来源与编写说明\n\n核查日期：2026-10-24。这里区分机构资料、公开案例、个人讨论和只读到检索摘要的线索。个人叙述未独立核实；检索摘要不能视为已读正文。每条的来源是选题或原则依据，全部话术、人物和情境细节均为独立编写，不是逐案采访记录，也不代表来源作者赞同本文。\n\n未收录或再分发 HowToGetAlong 正文、下载包或其他第三方全文。该项目的发现是本项目选题起点：https://github.com/kkk-bot/HowToGetAlong 。本项目内容与代码独立制作。\n\n'
for s in sources:source_text+=f"## {s['id']} · {s['title']}\n\n- 链接：{s['url']}\n- 类型：{s['type']}\n- 核查：{s['verification']}\n- 使用范围：{s['scope']}\n\n"
(R/'SOURCES.md').write_text(source_text)
groups=list(dict.fromkeys(c['group'] for c in cases));guide=intro
skill=R/'skills/social-conversation';refs=skill/'references';refs.mkdir(parents=True,exist_ok=True)
index='# 场景目录\n\n按用户问题选择最相关的一个主题文件，不必一次读完。所有话术需要根据用户真实职责与目标调整。\n\n'
for i,g in enumerate(groups,1):
 filename=f'{i:02d}-{g}.md';items=[c for c in cases if c['group']==g];body=''.join(entry(c) for c in items)
 guide+=f'# {g}\n\n'+body
 (refs/filename).write_text(f'# {g}\n\n'+body)
 index+=f'## [{g}]({filename})\n\n'+'\n'.join(f"- {c['id']} {c['title']}" for c in items)+'\n\n'
(R/'GUIDE.md').write_text(guide);(refs/'目录.md').write_text(index);(refs/'来源.md').write_text(source_text)
(skill/'SKILL.md').write_text('''---
name: social-conversation
description: 处理朋友往来、亲戚家庭、借还钱、聚会随礼、邻里与线上隐私，以及加班边界、抢功甩锅、绩效谈判、求职离职等生活和职场沟通问题，拟写自然回应并逐轮陪练。用户问人际难题、如何回朋友家人或领导同事、想练习难开口的对话时使用。
---
# 人情世故对话陪练

读取 references/目录.md，按问题选最相关的主题文件。共 151 个场景、18 个主题，涵盖生活与职场；仅按需加载，不必一次读取全部案例。需要核查出处再读 references/来源.md。

## 判断与回答

1. 先区分生活或职场情境；生活中的情感关系不要机械套用上下级管理口吻。识别用户要守住或争取什么、对方角色、已承诺职责、事实与沟通渠道。只追问会改变方案的缺失信息；可先说明假设给出暂定方案。
2. 先给一句自然可说的话，再解释适用条件、下一步动作和实际代价。不把维护关系默认放在用户边界之上，也不预设对方有恶意。
3. 面对继续施压，再给第二句，以及停止解释、升级协调或安全离场的条件。微信、会议、饭局使用相应语气，避免长篇模板。
4. 用户要求陪练时，扮演对方一次只说一句，等待用户回应。两到三轮后点评是否表达目标、是否承诺过量、下一步是否可观察。不要自问自答冒充用户。
5. 用户纠正事实后重新判断。已承诺值班、紧急安全事件、反复侵占成果等信息可能改变方案。话术不能保证对方满意。

## 事实与边界

- “资料启发”只表示问题类型或一般原则有来源；“原创建议”没有对应的真实事件声明。所有场景细节和话术均独立编写。不要伪造原作者引用、真实案例结果、研究结论或成功率。
- 检索摘要不是已读正文；社区帖子不是已核实事实。不得把本指南当作劳动法资料库。国外机构原则不能当成中国法律。
- 法律、报酬、解雇、医疗等专业结论需核对所在地与当前权威资料，必要时引导专业咨询；沟通方案与专业判断分开。
- 不编疾病、家庭事故、上级指示、证据和身份。不提供羞辱、造谣、报复、逼酒、泄露隐私的方案；改为事实澄清、边界表达或安全退出。
- 遇到骚扰或安全威胁，优先安全与支持，不要求先私下和解或忍耐。尊重当事人对求助渠道的选择。
- 未覆盖场景明确属于延伸建议，不把最接近的模板硬套进去。
- 不代发消息、不联系当事人、不保存私人档案，除非用户另行明确要求；只使用最少必要信息。
''')
for f in [R/'GUIDE.md', R/'SOURCES.md', *refs.glob('*.md')]:
 f.write_text(f.read_text().rstrip()+'\n')
(R/'downloads').mkdir(exist_ok=True)
with zipfile.ZipFile(R/'downloads/social-conversation.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(skill.rglob('*')):
  if f.is_file():
   info=zipfile.ZipInfo(str(f.relative_to(skill.parent)));info.date_time=(2026,10,24,0,0,0);info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,f.read_bytes())
print(json.dumps({'scenes':len(cases),'themes':len(groups),'basis':dict(Counter(c['basis'] for c in cases)),'sources':len(sources)},ensure_ascii=False))
