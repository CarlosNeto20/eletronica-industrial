"""Analisa exclusivamente CSVs acompanhados de execução PLECS bem-sucedida."""
from pathlib import Path
import json,hashlib
import shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]; OUT=Path(__file__).parent;FIG=ROOT/'artigo/figuras'
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.25,'lines.linewidth':.8})
def load(name):
    log=json.loads((OUT/(name+'_execucao.json')).read_text(encoding='utf8'));assert log['status']=='executado'
    path=OUT/(name+'.csv');assert hashlib.sha256(path.read_bytes()).hexdigest()==log['sha256_csv']
    return np.genfromtxt(path,delimiter=',',names=True),log
def mean(t,x):return float(np.trapezoid(x,t)/(t[-1]-t[0]))
def stats(a,lo,hi):
    b=a[(a['tempo_s']>=lo-1e-10)&(a['tempo_s']<=hi+1e-10)];t=b['tempo_s'];out={}
    for k in a.dtype.names[1:]:
        x=b[k];out[k]=dict(media=mean(t,x),min=float(x.min()),max=float(x.max()),pp=float(np.ptp(x)),rms=np.sqrt(mean(t,x*x)))
    out['janela_s']=[float(t[0]),float(t[-1])];out['duty_comando']=out['controle_V']['media']/2.1
    return out
def save(fig,name):
    fig.tight_layout();fig.savefig(FIG/(name+'.png'),dpi=280);fig.savefig(FIG/(name+'.pdf'));plt.close(fig)
    dest=OUT/'graficos';dest.mkdir(exist_ok=True)
    for ext in ['png','pdf']:shutil.copy2(FIG/(name+'.'+ext),dest/(name+'.'+ext))
def main():
    result={}
    for logfile in OUT.glob('*_execucao.json'):
        name=logfile.name.replace('_execucao.json','');log=json.loads(logfile.read_text(encoding='utf8'))
        if log.get('status')!='executado':continue
        a,log=load(name);t=a['tempo_s']
        if t[-1]<.1:continue
        d={'execucao':logfile.name,'sha256_csv':log['sha256_csv']}
        if name.startswith('degrau') or name in ('convergencia','curto_220'):
            d['leve_antes']=stats(a,.08,.10);d['plena_ou_curto']=stats(a,.18,.20);d['leve_apos']=stats(a,.28,.30)
            for event in [.12,.24]:
                b=a[(t>=event)&(t<=event+.04)];u=b['v_saida_V'];d[f'evento_{event}']=dict(v_min=float(u.min()),v_max=float(u.max()),iL_max=float(b['i_indutor_A'].max()))
            if name.startswith('degrau') or name=='convergencia':
                # Integral over exactly two mains periods in steady full load.
                lo=.18;hi=lo+2/60;tt=np.r_[lo,t[(t>lo)&(t<hi)],hi];vrms=log['ModelVars']['Vrms'];v=vrms*np.sqrt(2)*np.cos(2*np.pi*60*tt);i=np.interp(tt,t,a['i_rede_A'])
                pin=mean(tt,v*i);irms=np.sqrt(mean(tt,i*i));d['entrada']=dict(P_W=pin,I_rms_A=irms,FP=pin/(vrms*irms),janela_s=[float(tt[0]),float(tt[-1])])
                # Settling of moving average over 100 us, to the final 1% band.
                dt=np.median(np.diff(t));N=max(1,round(1e-4/dt));smooth=np.convolve(a['v_saida_V'],np.ones(N)/N,mode='same')
                for ev,target in [(.12,d['plena_ou_curto']['v_saida_V']['media']),(.24,d['leve_apos']['v_saida_V']['media'])]:
                    mask=(t>=ev)&(t<=ev+.05);bad=np.flatnonzero(mask&(np.abs(smooth-target)>.01*target));d[f'evento_{ev}']['acomodacao_1pct_media100us_s']=float(t[bad[-1]]-ev) if len(bad) else 0.
            else:
                d['i_curto_pico_derivado_A']=float(np.max(a['v_saida_V'][(t>=.12)&(t<.24)]/.001))
                d['i_curto_regime_A']=d['plena_ou_curto']['v_saida_V']['media']/.001
        elif name.startswith('ripple'):
            d['regime']=stats(a,.19,.1901)
        elif name.startswith('bateria'):
            d['CC']=stats(a,.04,.06);d['CV']=stats(a,.5,.55)
            b=a[(t>=.01)&(a['v_saida_V']>=26.9)]
            d['tempo_26_9V_s']=float(b['tempo_s'][0]) if len(b) else None
            d['carga_C']=float(np.trapezoid(a['i_bateria_A'],t));d['energia_J']=float(np.trapezoid(a['i_bateria_A']*a['v_saida_V'],t))
        result[name]=d
        if name=='degrau_220':
            b=a[(t>=.18)&(t<=.18+2/60)];tt=b['tempo_s']
            fig,ax=plt.subplots(2,1,figsize=(4.2,3.2),sharex=True)
            ax[0].plot(tt,220*np.sqrt(2)*np.cos(2*np.pi*60*tt),label='Rede');ax[0].plot(tt,b['v_bus_V'],label='Barramento');ax[0].set_ylabel('Tensão (V)');ax[0].legend(fontsize=8.5)
            ax[1].plot(tt,b['i_rede_A']);ax[1].set(xlabel='Tempo (s)',ylabel='Rede (A)');save(fig,'retificador_220')
        if name=='curto_220':
            b=a[(t>=.11999)&(t<=.1207)];tt=(b['tempo_s']-.12)*1e6
            fig,ax=plt.subplots(2,1,figsize=(4.2,3.2),sharex=True)
            ax[0].plot(tt,b['i_indutor_A']);ax[0].set_ylabel('Indutor (A)')
            ax[1].plot(tt,np.where(tt>=0,b['v_saida_V']/.001,0));ax[1].set(xlabel='Tempo após curto (µs)',ylabel='Ramo de curto (A)');save(fig,'curto_detalhe')
        if name in ['degrau_220','curto_220','bateria_220']:
            fig,ax=plt.subplots(2,1,figsize=(4.2,3.3),sharex=True)
            skip=max(1,len(a)//20000);ax[0].plot(t[::skip],a['v_saida_V'][::skip],color='#16639b');ax[0].set_ylabel('Saída (V)')
            ax[1].plot(t[::skip],a['i_indutor_A'][::skip],label='Indutor',color='#ab451b')
            if name.startswith('bateria'):ax[1].plot(t[::skip],a['i_bateria_A'][::skip],label='Bateria',color='#27743b');ax[1].legend(fontsize=8.5)
            ax[1].set(xlabel='Tempo (s)',ylabel='Corrente (A)');save(fig,name)
        if name.startswith('ripple'):
            b=a[(t>=.19)&(t<=.1901+1e-12)];tt=(b['tempo_s']-.19)*1e6
            fig,ax=plt.subplots(2,1,figsize=(4.2,3),sharex=True);ax[0].plot(tt,b['v_saida_V']);ax[0].set_ylabel('Saída (V)');ax[1].plot(tt,b['i_indutor_A']);ax[1].set(xlabel='Tempo relativo (µs)',ylabel='Indutor (A)');save(fig,name)
            if name=='ripple_revisado':
                fig,ax=plt.subplots(3,1,figsize=(4.2,3.8),sharex=True)
                ax[0].plot(tt,b['portadora_V'],label='Portadora');ax[0].plot(tt,b['controle_V'],label='Comando');ax[0].set_ylabel('PWM (V)');ax[0].legend(fontsize=8.5)
                ax[1].step(tt,b['PWM_01'],where='post');ax[1].set_ylabel('Gate Q1=Q2');ax[1].set_ylim(-.1,1.2)
                ax[2].plot(tt,b['v_primario_V'],label='Primário');ax[2].plot(tt,b['v_Q1_V'],label='VDS Q1',alpha=.75);ax[2].set(xlabel='Tempo relativo (µs)',ylabel='Tensão (V)');ax[2].legend(fontsize=8.5);save(fig,'pwm_cinco_periodos')
                fig,ax=plt.subplots(2,1,figsize=(4.2,3),sharex=True);ax[0].plot(tt,b['i_magnetizante_A']);ax[0].set_ylabel('Magnetização (A)');ax[1].plot(tt,b['i_Q1_A'])
                ax[1].set_xlabel('Tempo relativo (µs)');ax[1].set_ylabel('Q1 (A)');save(fig,'correntes_primario')
    if all(k in result for k in ['degrau_220','convergencia']):
        a,_=load('degrau_220');b,_=load('convergencia');checks={}
        for k in ['v_saida_V','i_indutor_A','v_bus_V']:
            s1=result['degrau_220']['plena_ou_curto'][k];s2=result['convergencia']['plena_ou_curto'][k]
            checks[k]={'media_base':s1['media'],'media_refinada':s2['media'],'erro_rel_media':abs(s1['media']-s2['media'])/max(abs(s2['media']),1e-12)}
        result['verificacao_convergencia']=checks
    (OUT/'metricas.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
    lines=['# Resultados efetivamente medidos no PLECS','', 'Fonte: CSVs com hash verificado; scripts e logs locais permitem reprodução.','']
    for name,d in result.items():
        lines+=['## '+name,'','```json',json.dumps(d,indent=2,ensure_ascii=False),'```','']
    (OUT/'metricas.md').write_text('\n'.join(lines),encoding='utf8');print('Analisados:',', '.join(result))
if __name__=='__main__':main()
