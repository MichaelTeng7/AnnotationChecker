# AnnotationChecker
In Python, developers are able to annotate their functions. For example: def f(x : [int]): pass. This annotation checker program takes in a function that has been called and checks whether or not the parameter(s)/return value(s) are correct before returning the function's result.
</br>The Check_Annotation class has a call method that intercepts each call to the decorated function and decides whether to check the annotation, and if so implements annotation checking, both for parameters and returned results, if they are specified; if annotation checking succeeds, this method computes/returns the result of calling the decorated function. The check method that does the annotation checking: it either succeeds silently or raises an AssertionError exception with useful information
</br></br>The <b>__call__</b> method intercepts calls to the decorated function;
  it specifies <b>*args</b> and <b>**kargs</b> to handle all calls,
  regardless of their parameter structure.
My method was about 40 lines (but about 17 lines were comments/blank, and
  7 comprise the <b>param_arg_binding</b> local function supplied in the
  download; this function computes an <b>ordereddict</b> of the parameter
  names (each associated to its argument) in the order that the parameters
  are defined in the function.
The <b>__call__</b> method
<ul>
<li>determines whether to check the annotations (see above); if not just
       call the decorated function and return its result.
<p>
<li>determines the parameters of the function and the matching arguments
      they are bound to.
    The <b>param_arg_bindings</b> function (written locally in this method)
       returns an ordered dictionary of parameter/value bindings; ordered means
       that when iterated, keys always appear in the same order: the order the
       parameters appear in in the function's definition.
    It uses the various attributes in the <b>inspect</b> module to do the job.
    You might be interested in reading the documentation for the <b>inspect</b>
      module: it is quite interesting and many of its (powerful) features are
      new to Python.
<p>
<li>determines the annotations of the parameters by using the
      <b>__annotations__</b> attribute of any function object.
    This name is bound to a dictionary containing as keys every annotated
      parameter name; the associated value for each parameter name is its
      annotation.
    If we defined the function <b>f</b> using
       <b>def f(x:int,y,z:int):->str...</b> its <b>__annotations__</b>
      dictionary is
<b><pre>
{'x': &lt;class 'int'&gt;, 'z': &lt;class 'int'&gt;, 'return': &lt;class 'str'&gt;>}</pre></b>
Notice that parameter <b>y</b> has no annotation so it does not appear as a key
  in this dictionary, and the key <b>return</b> is associated with the
  annotation for the returned value (after the <b>-&gt;</b>).
<p>

<li>If any checked annotations (parameters or returned result) raise the
      <b>AssertionError</b> handle it by printing the relevant source lines
      for the function (see the <b>getsourcelines</b> function in the 
      <b>inspect</b> module's documentation) and reraise the exception,
      skipping the rest of the code in this method.
  <ul>
  <li>Checks every parameter that has an annotation
  <p>
  <li>Call the decorated function to compute its returned result (and save it).
  <p>
  <li>If <b>'return'</b> is in the dictionary of annotions:
     (a) add the result as the value associated with the key <b>_return</b> in
          the dictionary of parameter and argument bindings; (b) check the
          annotation for <b>return</b>
  <p>
  <li>Return the result.    
  </ul>
</ul>
<p>

</br></br>
The <b>check</b> method has the following header
<b><pre>  def check(self,param,annot,value,check_history=''):</pre></b>
where
<ul>
<li><b>self</b>  is an instance of the <b>Check_Annotation</b> class
<li><b>param</b> is a string that specifies the name of the parameter being
        checked (or <b>'_return'</b> for checking the returned value</b>)
<li><b>annot</b> is a data structure that specifies the annotation
<li><b>value</b> is the value of <b>param</b> that the annotation should be
        checked against (to ensure it is legal)
<li><b>check_history</b> is a string that embodies the history of checking the
       annotation for the parameter to here (it is extended by concatenation in
       each recursive call to provide context for any annotation violations to
       be checked later); it is printed after the details of any annotation
       violation, to suppy context for the failure.
</ul>
<p>
