    <table class="menu-bar" border=0 cellspacing="0" cellpadding="0">
     <tr height=35 class="menu-bar">
     % menu_sections = menu_data[0]
     % for section in menu_sections:
       <td class="menu-toggler menu-h1 hosting" data-targetclass={{section[2]}}><a href={{section[3]}} class="menu-h1">{{section[1]}}</a></td>
     % end
     </tr>
    </table>
    
    <div id="menu-context">
      %#% menu_element = menu_data[1][0]
      %#{{menu_element}}
         <div class="cellsBlock menu-toggler-target hosting">
	   <table width="800" border="0" cellspacing="0" cellpadding="0">
             <tr>
             % for menu_content in menu_data[1][0]:
               <td><h2 class="menu-text-h2">{{menu_content['title']}}</h2></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][0]:
               <td><p class="menu-text">{{menu_content['description']}}</p></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][0]:
               <td class="menu-td"><p class="menu-text2">{{menu_content['price']}}</p></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][0]:
               <td class="menu-td2"><a href={{menu_content['link']}}>Заказать</a></td>
               <td width=10></td>
             % end
             </tr>
             <tr height=10></tr>
	   </table>
         </div>
    
         <div class="cellsBlock menu-toggler-target vps">
           <table width="800" border="0" cellspacing="0" cellpadding="0">
             <tr>
             % for menu_content in menu_data[1][1]:
               <td><h2 class="menu-text-h2">{{menu_content['title']}}</h2></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][1]:
               <td><p class="menu-text">{{menu_content['description']}}</p></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][1]:
               <td class="menu-td"><p class="menu-text2">{{menu_content['price']}}</p></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][1]:
               <td class="menu-td2"><a href={{menu_content['link']}}>Заказать</a></td>
               <td width=10></td>
             % end
             </tr>
             <tr height=10></tr>
           </table>
         </div>

	 <div class="cellsBlock menu-toggler-target domain"> 
           <table width="800" border="0" cellspacing="0" cellpadding="0">
             <tr>
             % for menu_content in menu_data[1][2]:
               <td><h2 class="menu-text-h2">{{menu_content['title']}}</h2></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][2]:
               <td><p class="menu-text">{{menu_content['description']}}</p></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][2]:
               <td class="menu-td"><p class="menu-text2">{{menu_content['price']}}</p></td>
               <td width=10></td>
             % end
             </tr>
             <tr>
             % for menu_content in menu_data[1][2]:
               <td class="menu-td2"><a href={{menu_content['link']}}>Заказать</a></td>
               <td width=10></td>
             % end
             </tr>
             <tr height=10></tr>
           </table>
	</div>
    </div>

