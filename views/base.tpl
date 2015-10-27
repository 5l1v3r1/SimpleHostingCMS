<!doctype html >
<html>
  <head>
    <meta charset="UTF-8">
    <link href="/static/css/style.css" rel="stylesheet">
  </head>
  <body>
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/app.js"></script>

    <!-- EVERYTHING -->
    <div class="everything"> 
    <table id=top border=0	>
     <tr>
      <td class="logo"><a href="/"><img src={{settings['logo_path']}} width={{settings['logo_width']}} height={{settings['logo_height']}}></a></td>
      <td width=400 align=right>
	%include('login_form.tpl')
      </td>
      <td class="top-right"><img src="/static/images/asterisk_top_right.gif" height=100></td>
     </tr>
    </table>

    <!-- MENU -->
    %include('menu.tpl')
    <!-- EVERYTHING -->
    <div id="footer"><img style="border-radius:6px" src="/static/images/asterisk_pic.jpg"></div>
    %include
    <div>
	<img width=800 src="/static/images/asterisk_footer.png">
    </div>
  </body>
</html>
