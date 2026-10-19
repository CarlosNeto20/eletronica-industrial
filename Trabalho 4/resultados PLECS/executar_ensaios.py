"""Executa SOMENTE via PLECS RPC; falha explicitamente se o servidor não responde.
Uso: python executar_ensaios.py [--teste | --ensaio nome | --todos]
"""
from pathlib import Path
import argparse,json,datetime,hashlib,time,socket,xmlrpc.client
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; OUT=Path(__file__).parent
socket.setdefaulttimeout(600)
P=xmlrpc.client.ServerProxy('http://localhost:1080',allow_none=True)
BASE=['tempo_s','v_saida_V','i_indutor_A','v_bus_V','controle_V','portadora_V','PWM_01','u_tensao_V','u_corrente_V','v_Q1_V','i_Q1_A','i_magnetizante_A','v_primario_V']
CASES={
 'degrau_220':('forward_degrau',dict(Vrms=220.),.36,2e-6),
 'degrau_176':('forward_degrau',dict(Vrms=176.),.36,2e-6),
 'degrau_264':('forward_degrau',dict(Vrms=264.),.36,2e-6),
 'curto_220':('forward_curto',dict(Vrms=220.),.36,1e-6),
 'bateria_220':('forward_bateria',dict(Vrms=220.),.6,2e-6),
 'ripple_revisado':('forward_barramento_cc',dict(Vbus=373.),.20,2e-7),
 'ripple_original':('forward_capacitor_original',dict(Vbus=373.),.20,2e-7),
 'convergencia':('forward_degrau',dict(Vrms=220.),.36,1e-6),
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(name,test=False):
    mdl,vars,stop,step=CASES[name];path=ROOT/'simulação PLECS'/f'{mdl}.plecs'
    rec=dict(ensaio=name,modelo=mdl,sha256_modelo=sha(path),inicio=datetime.datetime.now().astimezone().isoformat(),PLECS='5.0.6',ModelVars=vars,status='iniciado')
    logfile=OUT/(name+'_execucao.json');logfile.write_text(json.dumps(rec,indent=2),encoding='utf8')
    try:
        try:P.plecs.close(mdl)
        except xmlrpc.client.Fault:pass
        P.plecs.load(str(path.resolve()))
        if test:stop=.002;step=2e-6
        vars={**vars,'Tstop':stop}
        outputstart=.18 if name.startswith('ripple_') and not test else 0.
        opts={'ModelVars':vars,'SolverOpts':{'TimeSpan':stop,'MaxStep':step,'RelTol':1e-7 if name=='convergencia' else 1e-6,'AbsTol':1e-8,'OutputTimes':np.linspace(outputstart,stop,round((stop-outputstart)/step)+1).tolist(),'OutputTimesOption':'specified'}}
        rec['opcoes']= {**opts,'SolverOpts':{k:v for k,v in opts['SolverOpts'].items() if k!='OutputTimes'}}
        rec['grade_saida']={'inicio_s':outputstart,'passo_s':step,'fim_s':stop}
        t0=time.monotonic();data=P.plecs.simulate(mdl,opts);rec['duracao_real_s']=time.monotonic()-t0
        # Preserve native response, including original signal order.
        import gzip
        with gzip.open(OUT/(name+'_rpc.json.gz'),'wt',encoding='utf8') as f:json.dump(data,f,separators=(',',':'))
        ts=np.asarray(data['Time']); vals=np.asarray(data['Values'])
        if vals.shape[-1]==len(ts):vals=vals.T
        assert vals.shape[0]==len(ts),(vals.shape,ts.shape)
        cols=BASE.copy()
        if mdl not in ('forward_barramento_cc','forward_capacitor_original'):cols+=['i_rede_A']
        if mdl=='forward_bateria':cols+=['i_bateria_A']
        assert len(cols)==vals.shape[1]+1,(cols,vals.shape)
        arr=np.column_stack((ts,vals));assert np.isfinite(arr).all()
        csv=OUT/(name+'.csv');np.savetxt(csv,arr,delimiter=',',header=','.join(cols),comments='',fmt='%.10g')
        rec.update(status='executado',amostras=len(ts),colunas=cols,sha256_csv=sha(csv),tempo_final_s=float(ts[-1]))
        print(name,rec['status'],vals.shape,rec['duracao_real_s'],flush=True)
    except Exception as e:
        rec.update(status='falhou',erro=repr(e));print(name,'FALHOU',repr(e),flush=True);raise
    finally:logfile.write_text(json.dumps(rec,indent=2,ensure_ascii=False),encoding='utf8')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--teste',action='store_true');a.add_argument('--ensaio',choices=CASES);a.add_argument('--todos',action='store_true');args=a.parse_args()
    if args.todos:
        for name in CASES:
            log=OUT/(name+'_execucao.json');mdl,vs,st,sp=CASES[name]
            if log.exists():
                prev=json.loads(log.read_text(encoding='utf8'))
                if prev.get('status')=='executado' and prev.get('tempo_final_s')==st and prev.get('sha256_modelo')==sha(ROOT/'simulação PLECS'/f'{mdl}.plecs'):
                    print(name,'já executado com este modelo; preservado',flush=True);continue
            run(name)
    else:run(args.ensaio or 'degrau_220',args.teste)
