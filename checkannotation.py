from goody import type_as_str
from collections import defaultdict
import inspect

class Bag:
    def __init__(self,values=[]):
        self.counts = defaultdict(int)
        for v in values:
            self.counts[v] += 1
    
    def __str__(self):
        return 'Bag('+', '.join([str(k)+'['+str(v)+']' for k,v in self.counts.items()])+')'

    def __repr__(self):
        param = []
        for k,v in self.counts.items():
            param += v*[k]
        return 'Bag('+str(param)+')'

    def __len__(self):
        return sum(self.counts.values())
        
    def unique(self):
        return len(self.counts)
        
    def __contains__(self,v):
        return v in self.counts
    
    def count(self,v):
        return self.counts[v] if v in self.counts else 0

    def add(self,v):
        self.counts[v] += 1
    
    def remove(self,v):
        if v in self.counts:
            self.counts[v] -= 1
            if self.counts[v] == 0:
                del self.counts[v]
        else:
            raise ValueError('Bag.remove('+str(v)+'): not in Bag')
        
    def __eq__(self,right):
        if type(right) is not Bag or len(self) != len(right):
            return False
        else:
            for i in self.counts:
                # check not it to avoid creating count of 0 via defaultdict
                if i not in right or self.counts[i] != right.counts[i]:
                    return False
            return True
        
    @staticmethod
    def _gen(x):
        for k,v in x.items():
            for i in range(v):
                yield k  
                
    def __iter__(self):
        return Bag._gen(dict(self.counts))
    
    #define this method to implement the check annotation protocol
    #The check parameter refers to the check function in Check_Annotation,
    #  so that it can be called from here
    def __check_annotation__(self, check, param, value, text_history):
        assert isinstance(value, Bag), repr(param)+" failed annotation check(wrong type): value ="+repr(value)+\
        "\n  was type "+type_as_str(value)+" ...should be type Bag\n"+text_history
        for a in self.counts:
            pass
        for v in value.counts:
            check(param, a, v, text_history+"Bag value check: "+str(a)+"\n")
            
class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (raises AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (raise AssertionError) this classes raises AssertionError and prints its
      failure, along with a list of all annotations tried followed by the check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation():
    # set name to True for checking to occur
    checking_on  = True
  
    # self._checking_on must also be true for checking to occur
    def __init__(self,f):
        self._f = f
        self.checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        
        def check_list_tup(t):
            assert isinstance(value,t), repr(param)+" failed annotation check(wrong type): value = "+repr(value)+\
            "\n  was type "+type_as_str(value)+" ...should be type "+str(t)+"\n"+check_history
            
            if len(annot) == 1:
                for v in value:
                    self.check(param, annot[0], v, check_history+type_as_str(value)+"["+str(value.index(v))+"] check: "+str(annot[0])+"\n")
            else:
                assert len(annot) == len(value), repr(param)+" failed annotation check(wrong number of elements): value = "+repr(value)+\
                "\n  annotation had "+str(len(annot))+" elements"+str(annot)+"\n"+check_history
                for a,v in zip(annot,value):
                    self.check(param, a, v, check_history+type_as_str(value)+"["+str(value.index(v))+"] check: "+str(annot.index(a))+"\n")
        
        def check_dict():
            assert isinstance(value,dict), repr(param)+" failed annotation check(wrong type): value = "+repr(value)+\
            "\n  was type "+type_as_str(value)+" ...should be type dict\n"+check_history
            assert len(annot) == 1, repr(param)+" annotation inconsistency: dict should have 1 item but had "+str(len(annot))+\
            "\n  annotation = "+str(annot)
            for k,v in value.items():
                self.check(param, list(annot.keys())[0], k, check_history+"dict key check: "+str(list(annot.keys())[0])+"\n")
                self.check(param, list(annot.values())[0], v, check_history+"dict value check: "+str(list(annot.values())[0])+"\n")
        
        def check_set_fset(t):
            assert isinstance(value,t), repr(param)+" failed annotation check(wrong type): value = "+repr(value)+\
            "\n  was type "+type_as_str(value)+" ...should be type "+str(t)+"\n"+check_history
            assert len(annot) == 1, repr(param)+" annotation inconsistency: "+str(t)+" should have 1 value but had "+str(len(annot))+\
            "\n  annotation = "+str(annot)
            for v in value:
                self.check(param, type(v), v, check_history+str(t)+" value check: "+str(annot))
                
        def check_func():
            assert len(annot.__code__.co_varnames) == 1, repr(param)+" annotation inconsistency: predicate should have 1 parameter but had "+str(len(annot.__code__.co_varnames))+\
            "\n predicate = "+str(annot)+"\n"+check_history
            try:
                annot(value)
            except Exception as e:
                assert False, repr(param)+" annotation predicate("+str(annot)+") raised exception"+\
                "\n  exception = "+str(e.__class__)[8:-2]+": "+str(e)+"\n"+check_history
            else:
                assert annot(value), repr(param)+" failed annotation check: value = "+repr(value)+\
                "\n  predicate = "+str(annot)+"\n"+check_history
              
        def check_str():
            try:
                eval(annot,dict(self._d))
            except Exception as e:
                assert False, repr(param)+" annotation check(str predicate: "+repr(annot)+") raised exception"+\
                "\n  exception = "+str(e.__class__)[8:-2]+": "+str(e)+"\n"+check_history
            else:
                assert eval(annot,self._d), repr(param)+" failed annotation check(str predicate: "+repr(annot)+")"+\
                "\n  args for evaluation: "+", ".join([str(k)+"->"+str(v) for k,v in self._d.items()])
        
        # Decode annotation and check it
        if annot is None:
            return
        elif type(annot) is type:
            assert isinstance(value,annot), repr(param)+" failed annotation check(wrong type): value = "+repr(value)+\
            "\n  was type "+type_as_str(value)+" ...should be type "+str(annot)[8:-2]+"\n"+check_history
        elif isinstance(annot, list):
            check_list_tup(list)
        elif isinstance(annot, tuple):
            check_list_tup(tuple)
        elif isinstance(annot, dict):
            check_dict()
        elif isinstance(annot, set):
            check_set_fset(set)
        elif isinstance(annot, frozenset):
            check_set_fset(frozenset)
        elif inspect.isfunction(annot):
            check_func()
        elif isinstance(annot, str):
            check_str()
        else:
            try:
                annot.__check_annotation__(self.check, param, value, check_history)
            except AttributeError:
                assert False, repr(param)+" annotation undecipherable: "+str(annot)+"\n"+check_history
            except Exception as e:
                if e.__class__ is AssertionError:
                    raise
                else:
                    assert False, repr(param)+" annotation predicate"+str(annot)+" raised exception"+\
                    "\n  exception = "+str(e.__class__)[8:-2]+": "+str(e)+"\n"+check_history
        
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict, in the order parameters occur in the function's header)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if param.name not in bound_f_signature.arguments:
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        if not (Check_Annotation.checking_on and self.checking_on):
            return self._f(*args, **kargs)
        
        self._d = param_arg_bindings()
        
        try:
            # Check the annotation for every parameter (if there is one)
            for k,v in self._d.items():
                if k in self._f.__annotations__:
                    self.check(k, self._f.__annotations__[k], v)
                
            # Compute/remember the value of the decorated function
            value = self._f(*args, **kargs)
            
            # If 'return' is in the annotation, check it
            if 'return' in self._f.__annotations__:
                self._d['_return'] = value
                self.check('_return', self._f.__annotations__['return'], value)
                
            # Return the decorated answer
            return value
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
        #    print(80*'-')
        #    for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
        #        print(l.rstrip())
        #    print(80*'-')
            raise




  
if __name__ == '__main__':
    # an example of testing a simple annotation  
    def f(x:int): pass
    f = Check_Annotation(f)
    f(3)
    f('a')

    #import driver
    #driver.driver()
