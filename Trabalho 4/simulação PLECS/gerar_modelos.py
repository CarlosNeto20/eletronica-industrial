"""Gera esquemas nativos PLECS 5.0; não simula o circuito em Python."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
PARAM=json.loads((ROOT/'desenvolvimento/calculos/parametros.json').read_text(encoding='utf-8'))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def parameter(k,v):return f'Parameter {{ Variable {q(k)} Value {q(v)} Show off }}'
class Model:
    def __init__(self,name,init):self.name=name;self.init=init;self.cs=[];self.nets={};self.sigs={};self.outindices=[]
    def add(self,typ,name,x,y,params=None,direction='right',extra=''):
        self.cs.append(f'Component {{ Type {typ} Name {q(name)} Show on Position [{x}, {y}] Direction {direction} Flipped off LabelPosition south '+''.join(parameter(k,v) for k,v in (params or {}).items())+extra+' }')
    def node(self,node,*pins):self.nets.setdefault(node,[]).extend(pins)
    def sig(self,src,*dst):self.sigs.setdefault(src,[]).extend(dst)
    def output(self,name,src,index):
        self.outindices.append(index)
        self.add('Output',name,1150,40+index*35,dict(Index=index,Width=-1));self.sig(src,(name,1))
    def write(self):
        con=[]
        for typ,nets in [('Wire',self.nets.values()),('Signal',[[src,*dst] for src,dst in self.sigs.items()])]:
            for pins in nets:
                if len(pins)<2:continue
                s,t=pins[0]; body=f'Type {typ} SrcComponent {q(s)} SrcTerminal {t} '
                if len(pins)==2:
                    d,dt=pins[1];body+=f'DstComponent {q(d)} DstTerminal {dt}'
                else:
                    for d,dt in pins[1:]:body+=f'Branch {{ DstComponent {q(d)} DstTerminal {dt} }} '
                con.append('Connection { '+body+' }')
        header=(ROOT/'simulação PLECS/arquivo_exemplo.plecs').read_text().split('  Schematic {')[0]
        import re
        for key,val in dict(Name=self.name,TimeSpan='Tstop',MaxStep='2e-6',RelTol='1e-6',AbsTol='1e-8',Solver='radau',InitializationCommands=self.init).items():
            header=re.sub(r'(?m)^  '+key+r'\s+"[^"\n]*"',lambda m:'  '+key+' '+q(val),header)
        header+='\n'.join(f'Terminal {{ Type Output Index "{i}" }}' for i in sorted(self.outindices))+'\n'
        txt=header+' Schematic { Location [50, 50; 1350, 850] ZoomFactor 0.8 SliderPosition [0, 0] ShowBrowser off BrowserWidth 100\n'+'\n'.join(self.cs+con)+'\n }\n}\n'
        (ROOT/'simulação PLECS'/f'{self.name}.plecs').write_text(txt,encoding='utf-8')

def build(name='forward_degrau',mode=0,ac=True,original=False):
    cv=PARAM['controle']['final_v']['componentes'];ci=PARAM['controle']['final_i']['componentes']
    init=f'''% Trabalho 4 - parâmetros SI; modos: 0 degrau, 1 curto, 2 bateria
Vrms=220; Vbus=310; fs=50000; Tstop={0.6 if mode==2 else 0.36};
Lo=136.6e-6; Co={.0022 if original else .0044}; ESR={.11 if original else .055}; Cin=940e-6;
Lm=19.08e-3; Rcu=0.02; Rline=0.5; Lline=100e-6; Rbat=0.01; Cbat=0.4;
mode={mode}; Iref=15; Vref=27; Dlim=0.45; Tsoft=0.005;
Kiv={cv['Ki']}; Kpv={cv['Kp']}; wpv={cv['wp']};
Kii={ci['Ki']}; Kpi={ci['Kp']}; wpi={ci['wp']};
'''
    m=Model(name,init)
    if ac:
        m.add('ACVoltageSource','Rede',40,180,dict(V='sqrt(2)*Vrms',w='2*pi*60',phi='pi/2'),direction='down')
        m.add('Resistor','Rrede',100,100,dict(R='Rline'))
        m.add('Inductor','Lrede',160,100,dict(L='Lline',i_init=0))
        m.add('Ammeter','Irede',215,100)
        for k,x,y in [(1,260,100),(2,260,260),(3,330,100),(4,330,260)]:m.add('Diode',f'Ponte{k}',x,y,dict(Vf=.7,Ron=.01),direction='up')
        m.node('ac1',('Rede',1),('Rrede',1));m.node('ac2',('Rede',2),('Ponte3',1),('Ponte4',2))
        m.node('line1',('Rrede',2),('Lrede',1));m.node('line2',('Lrede',2),('Irede',1));m.node('ac3',('Irede',2),('Ponte1',1),('Ponte2',2))
        m.node('bus+',('Ponte1',2),('Ponte3',2));m.node('bus-',('Ponte2',1),('Ponte4',1))
        m.add('Capacitor','Cbus',380,180,dict(C='Cin',v_init='sqrt(2)*Vrms-1.4'),direction='down')
        m.node('bus+',('Cbus',1));m.node('bus-',('Cbus',2))
        m.output('i_rede_A',('Irede',3),10)
    else:
        m.add('DCVoltageSource','Ventrada',380,180,dict(V='Vbus'),direction='down');m.node('bus+',('Ventrada',1));m.node('bus-',('Ventrada',2))
    m.add('Voltmeter','Vbarramento',420,200,direction='down');m.node('bus+',('Vbarramento',1));m.node('bus-',('Vbarramento',2))
    for k,y in [(1,100),(2,290)]:m.add('Mosfet',f'Q{k}',485,y,dict(Ron=.15,s_init=0),direction='down')
    m.add('Diode','ResetSuperior',550,100,dict(Vf=.7,Ron=.01),direction='up')
    m.add('Diode','ResetInferior',430,290,dict(Vf=.7,Ron=.01),direction='up')
    m.add('Transformer','T1',600,190,dict(Windings='[1 1]',n='[60 18]',Polarity='+',Lm='inf',im0=0))
    m.add('Inductor','Lmag',550,190,dict(L='Lm',i_init=0),direction='down')
    m.node('bus+',('Q1',1),('ResetSuperior',2));m.node('bus-',('Q2',2),('ResetInferior',1))
    m.node('pri+',('Q1',2),('T1',1),('ResetInferior',2),('Lmag',1));m.node('pri-',('Q2',1),('T1',2),('ResetSuperior',1),('Lmag',2))
    m.add('Diode','Dforward',690,140,dict(Vf=.7,Ron=.005))
    m.add('Diode','Dlivre',730,245,dict(Vf=.7,Ron=.005),direction='up')
    m.add('Inductor','Lo',770,140,dict(L='Lo',i_init=0))
    m.add('Resistor','RLo',830,140,dict(R='Rcu'))
    m.add('Ammeter','IL',880,140)
    m.add('Diode','Dbloqueio',925,140,dict(Vf=.7,Ron=.005))
    m.add('Resistor','Rsh',690,315,dict(R=.01))
    m.add('Resistor','ESR',975,230,dict(R='ESR'),direction='down')
    m.add('Capacitor','Co',975,290,dict(C='Co',v_init=20 if mode==2 else 27),direction='down')
    m.add('Voltmeter','Vo',1040,230,direction='down')
    m.node('sec+',('T1',3),('Dforward',1));m.node('sec-',('T1',4),('Dlivre',1),('Rsh',1))
    m.node('sw',('Dforward',2),('Dlivre',2),('Lo',1));m.node('Lend',('Lo',2),('RLo',1))
    m.node('Lr',('RLo',2),('IL',1));m.node('Lout',('IL',2),('Dbloqueio',1))
    m.node('out',('Dbloqueio',2),('ESR',1),('Vo',1));m.node('cap',('ESR',2),('Co',1))
    m.node('gnd',('Co',2),('Rsh',2),('Vo',2))
    m.add('Ground','GND',900,350);m.node('gnd',('GND',1))
    if mode==2:
        m.add('Ammeter','Ibat',1080,140);m.add('Resistor','Rbat',1080,200,dict(R='Rbat'),direction='down')
        m.add('Capacitor','Cbat',1080,260,dict(C='Cbat',v_init=0),direction='down');m.add('DCVoltageSource','Ebat',1080,320,dict(V=20),direction='down')
        m.node('out',('Ibat',1));m.node('b0',('Ibat',2),('Rbat',1));m.node('b1',('Rbat',2),('Cbat',1));m.node('b2',('Cbat',2),('Ebat',1));m.node('gnd',('Ebat',2));m.output('i_bateria_A',('Ibat',3),11)
    else:
        m.add('Resistor','Rbase',1080,210,dict(R=9 if mode==0 else 1.8),direction='down')
        m.add('Resistor','Rdegrau',1140,200,dict(R=2.25 if mode==0 else .001),direction='down')
        m.add('Switch','Scarga',1140,290,dict(s_init=0,SwitchModel=1,f_grid=0),direction='down')
        m.node('out',('Rbase',1),('Rdegrau',1));m.node('gnd',('Rbase',2),('Scarga',2));m.node('loadsw',('Rdegrau',2),('Scarga',1))
    declarations='''#include <math.h>
#define EV (2.5-InputSignal(0,0)*(2.5/27.0))
#define EI ((ParamRealData(0,0)/6.0)*fmin(1.0,CurrentTime/ParamRealData(9,0))-InputSignal(1,0)/6.0)
#define UV (ContState(0)+ParamRealData(2,0)*ContState(1))
#define UI (ContState(2)+ParamRealData(5,0)*ContState(3))
#define U (fmax(0.0,fmin(2.1*ParamRealData(8,0),fmin(UV,UI))))
'''
    # Tracking prevents the inactive regulator from winding up at the selector.
    deriv='''ContDeriv(0)=ParamRealData(1,0)*EV+30000.0*(U-UV);
ContDeriv(1)=ParamRealData(3,0)*(EV-ContState(1));
ContDeriv(2)=ParamRealData(4,0)*EI+30000.0*(U-UI);
ContDeriv(3)=ParamRealData(6,0)*(EI-ContState(3));'''
    output='''OutputSignal(0,0)=U;
OutputSignal(1,0)=((CurrentTime>=0.12)&&(CurrentTime<0.24)) ? 1.0 : 0.0;
OutputSignal(2,0)=UV;
OutputSignal(3,0)=UI;'''
    m.add('CScript','Controle_CC_CV',680,470,dict(NumInputs='[1 1]',NumOutputs='[1 1 1 1]',NumContStates=4,NumDiscStates=0,NumZCSignals=2,DirectFeedthrough=1,Ts=0,Parameters='Iref,Kiv,Kpv,wpv,Kii,Kpi,wpi,mode,Dlim,Tsoft',LangStandard=2,GnuExtensions=2,RuntimeCheck=2,Declarations=declarations,StartFcn='for(int k=0;k<4;k++) ContState(k)=0;',OutputFcn=output+'\nZCSignal(0)=CurrentTime-0.12; ZCSignal(1)=CurrentTime-0.24;',DerivativeFcn=deriv,UpdateFcn='',TerminateFcn=''))
    m.add('TriangleGenerator','Portadora',480,530,dict(Min=0,Max=2.1,f='fs',DutyCycle=.5,Delay=0))
    m.add('Comparator','PWM',810,470)
    m.sig(('Vo',3),('Controle_CC_CV',1));m.sig(('IL',3),('Controle_CC_CV',2))
    m.sig(('Controle_CC_CV',3),('PWM',1));m.sig(('Portadora',1),('PWM',2));m.sig(('PWM',3),('Q1',3),('Q2',3))
    if mode!=2:m.sig(('Controle_CC_CV',4),('Scarga',3))
    for i,(name,src) in enumerate([('v_saida_V',('Vo',3)),('i_indutor_A',('IL',3)),('v_bus_V',('Vbarramento',3)),('controle_V',('Controle_CC_CV',3)),('portadora_V',('Portadora',1)),('PWM_01',('PWM',3)),('u_tensao_V',('Controle_CC_CV',5)),('u_corrente_V',('Controle_CC_CV',6))],1):m.output(name,src,i)
    m.add('PlecsProbe','Esforcos',1000,450,extra='Probe { Component "Q1" Path "" Signals {"MOSFET voltage", "MOSFET current"} } Probe { Component "Lmag" Path "" Signals {"Inductor current", "Inductor voltage"} }')
    m.output('esforcos',('Esforcos',1),9)
    m.write()
if __name__=='__main__':
    build();build('forward_curto',1);build('forward_bateria',2)
    build('forward_barramento_cc',0,False)
    build('forward_capacitor_original',0,False,True)
    print('5 modelos nativos escritos.')
