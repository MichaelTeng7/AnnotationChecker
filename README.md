# AnnotationChecker
In Python, developers are able to annotate their functions. For example: def f(x : [int]): pass. This annotation checker program takes in a function that has been called and checks whether or not the parameter(s)/return value(s) are correct before returning the function's result.
</br>The Check_Annotation class has a call method that intercepts each call to the decorated function and decides whether to check the annotation, and if so implements annotation checking, both for parameters and returned results, if they are specified; if annotation checking succeeds, this method computes/returns the result of calling the decorated function. The check method (specified in more detail below) that does the annotation checking: it either succeeds silently or raises an AssertionError exception with useful information
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
