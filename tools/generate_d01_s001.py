import argparse,csv,hashlib,json,random
from pathlib import Path
M=[('IM-01',2,15,380,50,2940),('IM-02',2,37,380,50,2950),('IM-03',4,22,380,50,1470),('IM-04',4,45,380,50,1475),('IM-05',4,75,380,50,1480),('IM-06',4,132,380,50,1485),('IM-07',4,315,6000,50,1487),('IM-08',6,55,380,50,980),('IM-09',8,37,380,50,730),('IM-10',4,90,380,50,1482)]
p=argparse.ArgumentParser();p.add_argument('--out',default='generated/D01-S001');p.add_argument('--rows',type=int,default=10000);p.add_argument('--seed',type=int,default=20260817);a=p.parse_args()
if a.rows<1:raise ValueError('rows must be positive')
o=Path(a.out);o.mkdir(parents=True,exist_ok=True);r=random.Random(a.seed);j=o/'D01-S001_generated_unreviewed.jsonl';c=o/'D01-S001_deterministic_audit.csv';audit=[]
with j.open('w',encoding='utf-8') as f:
 for i in range(a.rows):
  mid,k,kw,u,fs,n0=M[i%len(M)];ns=120*fs/k;n=n0+r.uniform(-8,5);s=(ns-n)/ns;po=kw*r.uniform(.2,1.05);t=9550*po/n;fr=s*fs;vf=u/fs
  x={'sample_id':f'D01-S001-{i+1:05d}','status':'generated_unreviewed','domain_id':'D01','shard_id':'D01-S001','evidence_level':'E0','engineering_claim_allowed':False,'known_conditions':{'motor_id':mid,'poles':k,'line_voltage_v':u,'supply_frequency_hz':fs,'speed_rpm':n,'output_power_kw':po},'derived_values':{'sync_speed_rpm':ns,'slip':s,'rotor_frequency_hz':fr,'conditional_torque_nm':t,'vf_v_per_hz':vf},'instruction':f'教学记录{i+1}: {mid}，{k}极，{u}V，{fs}Hz，转速{n:.6f}r/min，输出功率{po:.6f}kW。完成条件推导与边界说明。','assistant_response':f'同步转速={ns:.6f}r/min；转差率={s:.10f}；转子频率={fr:.10f}Hz；条件转矩={t:.8f}N·m；V/f={vf:.8f}V/Hz。前提为异步机、频率与极数正确、速度和功率口径一致且时间对齐；结论仅限教学计算，不确认现场故障或操作决定。'}
  f.write(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n');ok=0<s<1 and fr>0 and t>0 and vf>0;audit.append({'sample_id':x['sample_id'],'numeric_recompute':ok,'physical_properties':ok,'overall':'pass' if ok else 'fail'})
with c.open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=audit[0]);w.writeheader();w.writerows(audit)
h=lambda q:hashlib.sha256(q.read_bytes()).hexdigest();z={'shard_id':'D01-S001','row_count':a.rows,'status':'generated_unreviewed','seed':a.seed,'files':{'jsonl_sha256':h(j),'audit_sha256':h(c)},'deterministic_audit':{'pass_count':sum(x['overall']=='pass' for x in audit),'fail_count':sum(x['overall']!='pass' for x in audit)},'pending':['label_blind_diversity','corpus_duplicate_leakage','cross_domain_contradiction','expert_review']};(o/'D01-S001_manifest.json').write_text(json.dumps(z,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(z,ensure_ascii=False,indent=2))