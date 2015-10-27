Hi<br> 
You are visiting {{name}}! <br>
Response code: {{response}}<br>
%from pprint import pprint
%if response == None:
    %pprint('NULL')
%else:
    {{response}}

%rebase base
