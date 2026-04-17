const fs = require('fs');
const prRaw = fs.readFileSync('memory/raw-prs.json','utf8').replace(/^\uFEFF/,'');
const issRaw = fs.readFileSync('memory/raw-issues.json','utf8').replace(/^\uFEFF/,'');

const prs = JSON.parse(prRaw);
const issues = JSON.parse(issRaw);

// Filter wshten10 PRs
const ws = prs.filter(p=>p.author&&p.author.login==='wshten10');
const merged = ws.filter(p=>p.state==='MERGED');
const closed = ws.filter(p=>p.state==='CLOSED');
const open = ws.filter(p=>p.state==='OPEN');

console.log('=== PR ANALYSIS ===');
console.log('Total wshten10 PRs:', ws.length);
console.log('Merged:', merged.length);
console.log('Closed:', closed.length);
console.log('Open:', open.length);

// Analyze closed reasons
const dupLabel = closed.filter(p=>(p.labels||[]).some(l=>l.name.includes('duplicate')));
const noLabel = closed.filter(p=>!(p.labels||[]).length);
console.log('Closed with blocked:duplicate label:', dupLabel.length);
console.log('Closed without labels:', noLabel.length);

// Average merge time
let totalMergeH = 0;
merged.forEach(p => {
  if (p.mergedAt && p.createdAt) {
    const h = (new Date(p.mergedAt) - new Date(p.createdAt)) / 3600000;
    totalMergeH += h;
  }
});
console.log('Avg merge time (hours):', merged.length ? (totalMergeH/merged.length).toFixed(1) : 'N/A');

// Issues by wshten10
const wsIss = issues.filter(i=>i.author&&i.author.login==='wshten10');
console.log('\n=== ISSUE ANALYSIS ===');
console.log('Total wshten10 issues:', wsIss.length);
const openIss = wsIss.filter(i=>i.state==='OPEN');
const closedIss = wsIss.filter(i=>i.state==='CLOSED');
console.log('Open issues:', openIss.length);
console.log('Closed issues:', closedIss.length);

// Write structured output
const report = {
  prs: { total: ws.length, merged: merged.length, closed: closed.length, open: open.length, avgMergeHours: merged.length ? (totalMergeH/merged.length).toFixed(1) : 0 },
  closedReasons: { duplicateLabel: dupLabel.length, noLabel: noLabel.length },
  issues: { total: wsIss.length, open: openIss.length, closed: closedIss.length },
  mergedPRList: merged.map(p=>({number:p.number, title:p.title.substring(0,100)})),
  closedPRList: closed.map(p=>({number:p.number, title:p.title.substring(0,80), labels:(p.labels||[]).map(l=>l.name)})),
  openPRList: open.map(p=>({number:p.number, title:p.title.substring(0,100)}))
};

fs.writeFileSync('memory/analysis-result.json', JSON.stringify(report, null, 2));
console.log('\nReport saved to memory/analysis-result.json');
