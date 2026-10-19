"""Cálculos analíticos; não integra nem simula o circuito de potência."""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'desenvolvimento'/'calculos'; OUT.mkdir(exist_ok=True)
FIG=ROOT/'artigo'/'figuras'; FIG.mkdir(exist_ok=True)
fs=50000.; L=136.6e-6; n=.3; VD=2.1; Hv=2.5/27; Hi=1/6
def plants(f,V=373,R=1.8,C=2200e-6,r=.11):
    s=2j*np.pi*np.asarray(f)
    den=L*C*(1+r/R)*s*s+(L/R+C*r)*s+1
    return V*n*(1+s*C*r)/den, V*n/R*(1+s*C*(R+r))/den
def comp(f,R1,C1,C2,R2):
    s=2j*np.pi*np.asarray(f)
    return (1+s*C1*R2)/(R1*s*(C1+C2+s*R2*C1*C2))
def design(f,which,C,r,MF=65):
    p=plants(f,C=C,r=r)[which]*(Hv if which==0 else Hi)/VD
    phase=np.angle(p,deg=True); alpha=MF-phase-90
    assert alpha<90,(f,alpha)
    K=np.tan(np.deg2rad((alpha+90)/2)); G=1/abs(p); R1=10000.
    C2=1/(2*np.pi*f*G*K*R1); C1=C2*(K*K-1); R2=K/(2*np.pi*f*C1)
    wz=1/(R2*C1); wp=(C1+C2)/(R2*C1*C2); Ki=1/(R1*(C1+C2)); Kp=Ki*(1/wz-1/wp)
    return dict(R1=R1,C1=C1,C2=C2,R2=R2,fc=f,phase=phase,alpha=alpha,K=K,G=G,Ki=Ki,Kp=Kp,wp=wp,wz=wz)
def margins(fun):
    f=np.logspace(-2,7,40000); z=fun(f); mag=20*np.log10(abs(z)); phase=np.unwrap(np.angle(z))*180/np.pi
    crossings=[]
    for i in np.where(np.diff(np.sign(mag)))[0]:
        fc=brentq(lambda x:20*np.log10(abs(fun(x))),f[i],f[i+1]); ph=np.interp(np.log(fc),np.log(f),phase)
        crossings.append(dict(fc_Hz=fc,MF_deg=180+ph,MF_Ts2_deg=180+ph-180*fc/fs))
    gm=[]
    for i in np.where(np.diff(np.sign(phase+180)))[0]:
        fc=brentq(lambda x:np.imag(fun(x)),f[i],f[i+1]); gm.append(dict(f_Hz=fc,MG_dB=-20*np.log10(abs(fun(fc)))))
    return dict(cruzamentos=crossings,MG_dB=gm if gm else 'sem cruzamento -180 no modelo contínuo')
def main():
    peak=176*np.sqrt(2); valley=.9*peak; theta=np.arccos(.9); P=450
    io=P/((peak+valley)/2); ichg=io*np.pi/theta
    values=dict(Pout_W=405,Pin_orcamento_W=P,Vpeak_min_V=peak,Vvalley_alvo_V=valley,theta_rad=theta,
        Cin_min_F=P*(np.pi-theta)/(np.pi*60*(peak**2-valley**2)),tconducao_s=theta/(2*np.pi*60),
        Ioeq_A=io,Ichg_A=ichg,ICin_rms_A=np.sqrt(io*(ichg-io)),Idiodo_med_A=io/2,
        Idiodo_rms_A=ichg*np.sqrt(theta/(2*np.pi)),Roeq_ohm=((peak+valley)/2)**2/P,
        Dmin=27/(373*n),Lmin_H=27*(1-27/(373*n))/(fs*3),Cmin_F=3/(8*fs*.27),
        ripple_original_V=3*.11+3/(8*fs*.0022),ripple_banco_V=3*.055+3/(8*fs*.0044),
        Cbat_fisico_equivalente_F=150*3600/7,tempo_emulacao_ideal_s=.4*7/15,
        Np=60,Ns=18,Ae_m2=368e-6,Lm_H=5300e-9*60**2,
        Bmax_transitorio_T=373*.45/(fs*60*368e-6),Bnom_T=90/(fs*60*368e-6))
    orig_v=dict(R1=1e4,C1=1.722e-9,C2=81.65e-12,R2=86.88e3)
    orig_i=dict(R1=1e4,C1=2.104e-9,C2=165.8e-12,R2=22.39e3)
    # C bank lowers ESR and shifts plant: redesign both compensators.
    final_v=design(2500,0,.0044,.055,65); final_i=design(5000,1,.0044,.055,65)
    cases=[('original_v',0,orig_v,.0022,.11),('original_i',1,orig_i,.0022,.11),
           ('final_v',0,final_v,.0044,.055),('final_i',1,final_i,.0044,.055)]
    results={}
    plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.3})
    for name,idx,c,C,r in cases:
        pars={k:c[k] for k in ('R1','C1','C2','R2')}
        fun=lambda f:plants(f,C=C,r=r)[idx]*(Hv if idx==0 else Hi)/VD*comp(f,**pars)
        results[name]=dict(componentes=c,margens=margins(fun),cantos=[])
        plantden=[L*C*(1+r/1.8),L/1.8+C*r,1]
        plantnum=np.array([C*r,1])*373*n if idx==0 else np.array([C*(1.8+r),1])*373*n/1.8
        cn=[c['C1']*c['R2'],1]; cd=[c['R1']*c['R2']*c['C1']*c['C2'],c['R1']*(c['C1']+c['C2']),0]
        closed=np.polyadd(np.polymul(plantden,cd),np.polymul(plantnum,cn)*(Hv if idx==0 else Hi)/VD)
        results[name]['polos_malha_fechada']=[[float(p.real),float(p.imag)] for p in np.roots(closed)]
        results[name]['estavel_continuo']=bool(np.all(np.real(np.roots(closed))<0))
        for V in (225,310,373):
            for R in (1.8,9):
                fc=lambda f:plants(f,V=V,R=R,C=C,r=r)[idx]*(Hv if idx==0 else Hi)/VD*comp(f,**pars)
                pd=[L*C*(1+r/R),L/R+C*r,1]
                pn=np.array([C*r,1])*V*n if idx==0 else np.array([C*(R+r),1])*V*n/R
                poles=np.roots(np.polyadd(np.polymul(pd,cd),np.polymul(pn,cn)*(Hv if idx==0 else Hi)/VD))
                results[name]['cantos'].append(dict(V=V,R=R,**margins(fc),polos=[[float(p.real),float(p.imag)] for p in poles],estavel_continuo=bool(np.all(np.real(poles)<0))))
        f=np.logspace(1,5.5,3000); p=plants(f,C=C,r=r)[idx]*(Hv if idx==0 else Hi)/VD; cc=comp(f,**pars); loop=p*cc
        np.savetxt(OUT/(name+'_bode.csv'),np.column_stack((f,20*np.log10(abs(p)),np.angle(p,deg=True),20*np.log10(abs(cc)),np.angle(cc,deg=True),20*np.log10(abs(loop)),np.unwrap(np.angle(loop))*180/np.pi)),delimiter=',',header='f_Hz,planta_dB,planta_graus,comp_dB,comp_graus,laco_dB,laco_graus',comments='')
        fig,ax=plt.subplots(2,1,figsize=(4.2,3.6),sharex=True)
        for z,label in [(p,'Planta + sensores + PWM'),(cc,'Compensador'),(loop,'Laço')]:
            ax[0].semilogx(f,20*np.log10(abs(z)),label=label); ax[1].semilogx(f,np.unwrap(np.angle(z))*180/np.pi)
        ax[0].axhline(0,color='black',lw=.6); ax[0].set_ylabel('Ganho (dB)'); ax[0].legend(fontsize=8)
        ax[1].set(xlabel='Frequência (Hz)',ylabel='Fase (graus)',ylim=(-200,100)); fig.tight_layout();fig.savefig(FIG/(name+'_bode.png'),dpi=250);plt.close(fig)
    values['controle']=results
    (OUT/'parametros.json').write_text(json.dumps(values,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(values,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
