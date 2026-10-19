from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
out=Path(__file__).resolve().parents[1]/'figuras'
f,ax=plt.subplots(figsize=(4.2,1.7));ax.set(xlim=(0,10),ylim=(0,4));ax.axis('off')
for x,label in [(0.1,'Ponte\n940 µF'),(3.65,'Forward\n60:18'),(7.2,'Filtro\ne saída')]:
 ax.add_patch(Rectangle((x,2.4),2.6,1.2,fill=False,lw=1));ax.text(x+1.3,3,label,ha='center',va='center',fontsize=10)
for x1,x2 in [(2.7,3.65),(6.25,7.2)]:ax.annotate('',xy=(x2,3),xytext=(x1,3),arrowprops=dict(arrowstyle='->',lw=1))
ax.text(1.4,3.8,'176–264 Vca',ha='center',fontsize=8)
ax.text(8.5,3.8,'20–27 V / 15 A',ha='center',fontsize=8)
ax.add_patch(Rectangle((3.3,.25),3.3,1.0,fill=False,lw=1));ax.text(4.95,.75,'CC/CV + PWM',ha='center',va='center',fontsize=10)
ax.annotate('',xy=(4.95,2.4),xytext=(4.95,1.25),arrowprops=dict(arrowstyle='->',lw=1));ax.text(4.7,1.8,'Q1 = Q2',ha='right',fontsize=8)
ax.plot([8.5,8.5,6.6],[2.4,.75,.75],color='black',lw=1);ax.annotate('',xy=(6.6,.75),xytext=(7,.75),arrowprops=dict(arrowstyle='->',lw=1));ax.text(8.7,1.6,'Vo, IL',fontsize=8)
f.tight_layout(pad=.1);f.savefig(out/'arquitetura.png',dpi=300);f.savefig(out/'arquitetura.pdf');plt.close(f)
